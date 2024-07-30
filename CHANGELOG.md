# ChangeLog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
### Added
### Changed
### Fixed

## 0.1.3
### Added
- Generify custom encoder class
    ```python
    class GenerifyCustomEncoder(GenerifyEncoder):
        def default(self, obj, path):
            if isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return GenerifyEncoder.default(self, obj, path)
    ...
    ret = generify({"a": 1, "b": Scalar()}, cls=GenerifyCustomEncoder)
    ```

### Fixed
- Iterable handling convertion to list.
- pandas DataFrame index with objects handling, handle as iterable

- generify raise_getattr_exception flag, raising GenerifyGetAttrException of failure:
    ```python
    generic_obj = generify(obj, raise_getattr_exception=True)
    ```


## 0.1.2
### Added
- generify raise_exception flag, raising GenerifyException of failure:
    ```python
    generic_obj = generify(obj, raise_exception=True)
    ```
- generify raise_getattr_exception flag, raising GenerifyGetAttrException of failure:
    ```python
    generic_obj = generify(obj, raise_getattr_exception=True)
    ```

### Changed
### Fixed
- fix list inplace change to content.

## 0.1.1
### Added
- GenerifyJSONEncouder. usage:
    ```python
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
```python
from generify import generify
...
generic_obj = generify(obj)
...
```

### Changed
### Fixed
