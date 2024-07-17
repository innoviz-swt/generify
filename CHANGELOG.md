# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
### Added
### Changed
### Fixed

## 0.1.1
### Added
- GenerifyJSONEncouder. usage:
    ```
    from generify import generify, GenerifyJSONEncoder
    ...
    generic_obj = generify(obj)
    json.dumps(generic_obj, cls=GenerifyJSONEncoder)
    ...
    ```
### Changed
### Fixed
- fix handling namedtuples, keeping generified result as named tuples.

# 0.1.0 - first release
### Added
generifies python classes to generic dict containing only python internals, numpy arrays and panda lists.
Usage example:
```
from generify import generify
...
generic_obj = generify(obj)
...
```

### Changed
### Fixed
