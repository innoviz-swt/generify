from collections.abc import Iterable
from enum import Enum
from typing import List

import numpy as np
import pandas as pd


class TestException:
    pass


class GenerifyException(Exception):
    pass


class GenerifyGetAttrException(Exception):
    pass


class GenerifyEncoder:
    def __init__(self, log=None, raise_exception=False, raise_getattr_exception=False):
        self._log = log
        self._circular_ids = set()
        self._cache = dict()
        self._raise_exception = raise_exception
        self._raise_getattr_exception = raise_getattr_exception

    def df_handler(self, df, path):
        is_index_obj = not np.issctype(df.index.dtype)

        is_col_obj = False
        for dtype in df.dtypes.tolist():
            if not np.issctype(dtype):
                is_col_obj = True
                break

        if not is_col_obj and not is_index_obj:
            return df

        df_ret = df.copy()
        if is_index_obj:
            df_ret.index = self.default(df_ret.index.to_list(), path + ["df_index"])
        if is_col_obj:
            for column in df_ret.columns:
                if np.issctype(df_ret[column].dtypes):
                    if self._log:
                        self._log(f"generify {path + [column]}: {df_ret[column].dtypes}")
                    continue
                row_list = []
                for i, row in enumerate(df_ret.index):
                    res = self.default(df_ret[column][row], path + [column, i])
                    row_list.append(res)
                df_ret[column] = row_list

        return df_ret

    def default(self, obj, path: List[str]):
        oid = id(obj)
        # check if item was previously generified
        if oid in self._cache:
            return self._cache[oid]

        unsupported = False
        is_rec = False

        # protect against circular dependency
        if oid in self._circular_ids:
            return f"oid-{oid}"
        self._circular_ids.add(oid)

        # handle obj type
        try:
            if obj is None:
                ret = obj
            elif isinstance(obj, pd.DataFrame):
                ret = self.df_handler(obj, path)
            elif isinstance(obj, dict):
                is_rec = True
                ret = dict()
                for k in obj.keys():
                    kk = self.default(k, path + [f"key->{k}"])
                    v = obj[k]
                    if callable(v):
                        continue
                    ret_val = self.default(v, path + [k])
                    ret[kk] = ret_val
            elif isinstance(obj, list):
                is_rec = True
                ret = [None] * len(obj)
                for i in range(len(obj)):
                    ret[i] = self.default(obj[i], path + [i])
            elif (
                isinstance(obj, tuple) and hasattr(obj, "_asdict") and hasattr(obj, "_fields")
            ):  # checking if it is a namedtuple
                is_rec = True
                ret = [None] * len(obj)
                for i in range(len(obj)):
                    ret[i] = self.default(obj[i], path + [i])
                ret = ("NamedTuple", obj._fields, tuple(ret))
            elif isinstance(obj, tuple):
                is_rec = True
                ret = [None] * len(obj)
                for i in range(len(obj)):
                    ret[i] = self.default(obj[i], path + [i])
                ret = tuple(ret)
            elif isinstance(obj, set):
                is_rec = True
                ret = set()
                l = len(obj)
                for i in range(l):
                    k = obj.pop()
                    k = self.default(k, path + [i])
                    ret.add(k)
                pass
            elif isinstance(obj, np.dtype):
                ret = obj
            elif isinstance(obj, np.ndarray):
                if obj.dtype.kind == "O":
                    raise RuntimeError(f"Unsupported numpy array, dtype=object, path: {path}.")
                ret = obj
            elif np.isscalar(obj):
                ret = obj
            elif isinstance(obj, Enum):
                # enum is converted to hashable type tuple
                ret = ("Enum", obj.name, obj.value)
            elif isinstance(obj, Iterable):
                is_rec = False
                ret = self.default(list(obj), path)
            elif isinstance(obj, TestException):
                raise Exception("test exception")
            elif hasattr(obj, "__class__"):  # custom class, turn it into a dict
                is_rec = True
                keys = [k for k in dir(obj) if not (k.startswith("__") and k.endswith("__"))]
                ret = dict()
                for k in keys:
                    kk = self.default(k, path + [f"key->{k}"])
                    try:
                        v = getattr(obj, k)
                    except Exception as ex:
                        if self._raise_getattr_exception:
                            raise GenerifyGetAttrException(f"Failed getattr {path + [k]}") from ex
                        v = f"Failed getattr, {ex.__class__.__name__}: {ex}"
                    if callable(v):
                        continue
                    ret_val = self.default(v, path + [k])
                    ret[kk] = ret_val
            else:
                unsupported = True
        except Exception as ex:
            # if getattr exception was raise keep perculating it
            if isinstance(ex, GenerifyGetAttrException):
                raise ex

            if self._raise_exception:
                # recursive exception catch
                if isinstance(ex, GenerifyException):
                    raise ex
                raise GenerifyException(f"Failed generify '{type(obj).__name__}', path: {path}") from ex
            ret = f"Failed generify, {ex.__class__.__name__}: {ex}"

        if unsupported:
            raise RuntimeError(f"Unsupported type '{type(obj)}', path: {path}.")

        if not is_rec and self._log:
            self._log(f"generify {path}: {ret}")

        # protect against circular dependency
        self._circular_ids.remove(oid)

        self._cache[oid] = ret

        return ret


def generify(obj, path=None, log=None, raise_exception=False, raise_getattr_exception=False, cls=GenerifyEncoder):
    if path is None:
        path = []

    ret = cls(log=log, raise_exception=raise_exception, raise_getattr_exception=raise_getattr_exception).default(
        obj, path
    )
    return ret
