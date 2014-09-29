"""
    zookeeper_watcher
    ~~~~~~~~~~~~~~
    Implements a Watch class which can be used as a decorator to trigger 
    functions when changes are detected on a specified node in Zookeeper.

    Example:
    from zookeeper_watcher import ZookeeperWatcher

    watcher = ZookeeperWatcher('zookeeper_host')
    watcher.start()

    @watcher.Watch('/zookeeper/path/to/node/that/we/want/to/watch')
    def test_function(children, data):
      print "List of children nodes", children
      print "List of values for the above children nodes", data    


    The above function gets triggered once when that portion of code is 
    ran and also everytime a change is detected at the end of the path.

    :copyright: 2014 by Bogdan Alexandrescu.
    :license: MIT
"""

import json
import sys
import logging
from functools import partial, wraps

from kazoo.client import KazooClient, KazooState, KazooRetry
from kazoo.exceptions import NoNodeError, KazooException, ConnectionClosedError


__author__ = '@balex'
__license__ = 'MIT'
__version__ = '0.1.1'


class ConnectionError(Exception): pass
class DataError(Exception): pass
class ZookeeperStateWatcherHandlerError(Exception): pass


def _ignore_closed(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ConnectionClosedError:
      pass
  return wrapper


log = logging.getLogger(__name__)


class Watch():

  def __init__(self, client, path, func=None,
                 allow_session_lost=True, send_event=False):

    self._client = client
    self._path = path if '/' not in path[-1] else path[:-1]
    self._func = func
    self._allow_session_lost = allow_session_lost
    self._send_event = send_event
    self._stopped = False
    self._watch_established = False
    self._run_lock = client.handler.lock_object()
    self._prior_children = None
    self._used = False
    self._log = client.logger
    self._retry = KazooRetry(max_tries=None, sleep_func=client.handler.sleep_func)

    # Register our session listener if we're going to resume
    # across session losses
    if func is not None:
      self._used = True
      if allow_session_lost:
        self._client.add_listener(self._session_watcher)
      self._get_data()

  def __call__(self, func):
    """Callable version for use as a decorator

    :param func: Function to call initially and every time the
                 children change. `func` will be called with a
                 single argument, the list of children.
    :type func: callable

    """
    if self._used:
      raise KazooException(
            "A function has already been associated with this "
            "Watch instance.")

    self._func = func

    self._used = True
    if self._allow_session_lost:
      self._client.add_listener(self._session_watcher)
    self._get_data()
    return func


  @_ignore_closed
  def _get_data(self, event=None):
    with self._run_lock:  # Ensure this runs one at a time
      if self._stopped:
        return

      children = self._client.retry(self._client.get_children,
                                    self._path, self._watcher)
      if not self._watch_established:
        self._watch_established = True

        if self._prior_children is not None and self._prior_children == children:
          return

      self._prior_children = children

      data = []
      for child in children:
        try:
          path = self._path + '/' + child
          child_data, _ = self._retry(self._client.get, path, self._watcher)
          data.append(json.loads(child_data))
        except NoNodeError:
          pass

      try:
        result = self._func(children, data)
        if result is False:
          self._stopped = True
      except Exception as exc:
        log.exception(exc)
        raise

  def _watcher(self, event):
    self._get_data(event)

  def _session_watcher(self, state):
    if state in (KazooState.LOST, KazooState.SUSPENDED):
      self._watch_established = False
    elif (state == KazooState.CONNECTED and not self._watch_established and not self._stopped):
      self._client.handler.spawn(self._get_data)


class ZookeeperWatcher(KazooClient):
  """Extended Kazoo Client Class to include the new Watch class in the constructor"""

  def __init__(self, *args, **kwargs):
    super(ZookeeperWatcher, self).__init__(*args, **kwargs)
    self.Watch = partial(Watch, self)
    self.read_only = True