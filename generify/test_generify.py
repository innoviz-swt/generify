from collections import namedtuple
from enum import Enum

from generify import generify

import numpy as np
import pandas as pd


class EnumA(Enum):
    A1 = "a1_val"
    B1 = 3


GEN_A1 = ("A1", "a1_val", "EnumA")

NamedT = namedtuple("NamedT", "aa bb cc")


class Scalar:
    def __init__(self) -> None:
        self.val_int = 3
        self.val_float = 10.0
        self.val_str = "jhon"
        self.val_bool = True
        self.val_enum = EnumA.A1
        self.val_np_scalar = np.float128(30)
        self.val_dtype = np.dtype("float")

    def __eq__(self, other: dict):
        return (
            len(other) == 7
            and self.val_int == other["val_int"]
            and self.val_float == other["val_float"]
            and self.val_str == other["val_str"]
            and self.val_bool == other["val_bool"]
            and GEN_A1 == other["val_enum"]
            and self.val_np_scalar == other["val_np_scalar"]
            and other["val_np_scalar"].dtype == np.float128
            and self.val_dtype == other["val_dtype"]
            and self.val_bool == other["val_bool"]
        )


class Nested:
    def __init__(self) -> None:
        self.a = 3
        self.scalar = Scalar()

    def __eq__(self, other: dict):
        return self.a == other["a"] and self.scalar == other["scalar"]


class NumpyArray:
    def __init__(self) -> None:
        self.val_numpy_arr = np.array([1, 2, 3])
        self.val_2d_numpy_arr = np.array([[1, 2, 3], [4, 5, 6]])


class Dataframe:
    def __init__(self) -> None:
        self.val_simple_df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": ["a1", "b3", "b4"],
            }
        )
        self.val_test_objects = pd.DataFrame(
            {
                "rot": [a, b],
                "float": [0.2, 3.5],
            }
        )
        self.val_test_simple_header = pd.DataFrame(
            {
                1: ["one", "two"],
                3.5: [0.2, 3.5],
            }
        )
        self.val_test_nested = pd.DataFrame(
            {
                "hard": [["one", "two"], [a, b]],
                "easy": [0.2, 3.5],
            }
        )


class Mix:
    def __init__(self) -> None:
        self.val = {
            "v1": [1, Nested()],
            "v2": [1, "2", True],
            "v_np1": np.array([1, 2, 3]),
            "v_df1": pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, 30]}),
            "v_sc": Scalar(),
            "v_mix1": [5, Scalar(), set([2, "a"])],
        }


def assert_dict_a(ret):
    assert ret[1] == 3
    assert ret["2"] == 4
    assert ret[(1, 2)] == 10


# self.val_nested = [[1, 2], Scalar(), [1, 2, 3], [[5, Scalar(), 7], [2]]]


def test_scalar():
    ret = generify(Scalar())
    assert ret == Scalar()


def test_enum():
    ret = generify(EnumA.A1)
    assert ret == GEN_A1


def test_list():
    ret = generify([1, 2, 3])
    assert ret == [1, 2, 3]

    val = [1, Scalar(), 10.3, {1: 3, "2": 4, (1, 2): 10}]
    ret = generify(val)
    assert ret == [*val]


def test_tuples():
    ret = generify((1, 2, 3))
    assert ret == (1, 2, 3)

    val = (1, Scalar(), 10.3, {1: Scalar(), "2": 4, (1, 2): 10})
    ret = generify(val)
    assert ret == tuple([*val])


def test_namedtuple():
    val_named = NamedT(0.5, (1, 2), Scalar())

    ret = generify(val_named)
    assert ret == {"aa": 0.5, "bb": (1, 2), "cc": Scalar()}


def test_dictionary():
    ret = generify(
        {
            "a": 2,
            "b": [1, 20.2, "dan", Scalar()],
            1: 500,
            EnumA.A1: 30,
        }
    )
    assert ret == {
        "a": 2,
        "b": [1, 20.2, "dan", Scalar()],
        1: 500,
        GEN_A1: 30,
    }


def test_numpy_arr():
    ret = generify(np.array([1, 2, 3]))
    assert np.array_equal(ret, [1, 2, 3])
    assert isinstance(ret, np.ndarray)

    ret = generify(np.array([[1, 2, 3], [4, 5, 6]]))
    assert np.array_equal(ret, [[1, 2, 3], [4, 5, 6]])
    assert isinstance(ret, np.ndarray)


def test_dataframe():
    val = pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, "30"]})
    ret = generify(val)
    assert pd.DataFrame.equals(val, ret)
    assert isinstance(ret, pd.DataFrame)


def test_nested_object():
    ret = generify(Nested())
    assert ret == Nested()


def test_mix():
    ret = generify(Mix())
    assert len(ret) == 1
    assert ret["val"]["v1"] == [1, Nested()]
    assert ret["val"]["v2"] == [1, "2", True]
    assert np.array_equal(ret["val"]["v_np1"], np.array([1, 2, 3]))
    assert pd.DataFrame.equals(ret["val"]["v_df1"], pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, 30]}))
    assert ret["val"]["v_sc"] == Scalar()
    assert ret["val"]["v_mix1"] == [5, Scalar(), set(["a", 2])]


if __name__ == "__main__":
    ret = generify(
        pd.DataFrame({"col1": [1, 2, 3], "col2": [10, 20, "30"]}),
        log=print,
    )
    print(ret)
