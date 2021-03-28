# Zookeeper-Watcher

Watches a designated node in Zookeeper for data or member changes. 
Implements a Watch class which can be used as a decorator to trigger functions when changes are detected on a specified node in Zookeeper.

[![Latest Version](https://img.shields.io/pypi/v/Zookeeper-Watcher.svg)]
(https://pypi.python.org/pypi/Zookeeper-Watcher/)
[![Downloads](https://img.shields.io/pypi/dm/Zookeeper-Watcher.svg)]
(https://pypi.python.org/pypi/Zookeeper-Watcher/)
[![Download format](https://img.shields.io/pypi/format/Zookeeper-Watcher.svg)]
(https://pypi.python.org/pypi/Zookeeper-Watcher/)
[![License](https://img.shields.io/pypi/l/Zookeeper-Watcher.svg)]
(https://pypi.python.org/pypi/Zookeeper-Watcher/)


## Supported Platforms

* OSX and Linux.
* Python 2.7

Probably works with other versions as well.

## Quickstart

Install:
```bash
pip install Zookeeper-Watcher
```

Example:
```python
from zookeeper_watcher import ZookeeperWatcher

#instantiate the watcher object by passing it the Zookeeper server address and a optional logger.
watcher = ZookeperWatcher('zookeeper_host:port') #can receive also a custom logger by adding logger=some_logger.

#start the async connection with the Zookeeper server
watcher.start()

#decorate a function that will be triggered once at runtime and on every detected event
@watcher.Watch('/zookeeper/path/to/the/node/that/we/want/to/watch')
def test_function(children, data):
  """decorated function that receives a list of children nodes of the given path 
  and a list of data objects (dictionaries) that are read from each child node"""
  print "list of children nodes", children
  print "list of data objects", data

```

## Changelog

#### 0.1.4

* Fixed some logging bugs.

#### 0.1.3

* Added custom logging.

#### 0.1.2

* Fixed some logging errors.

#### 0.1.1

* Fixed some distribution packaging bug.

#### 0.1.0

* Initial release.

