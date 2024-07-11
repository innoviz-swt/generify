from collections import namedtuple
from enum import Enum

from generify import generify

import numpy as np
import pandas as pd

DICTA = {1: 3, "2": 4, (1, 2): 10}


class EnumA(Enum):
    A1 = "a1_val"
    B1 = 3


class Scalar:
    def __init__(self) -> None:
        self.val_int = 3
        self.val_float = 10.0
        self.val_str = "jhon"
        self.val_bool = True
        self.val_enum = EnumA.A1

    def __eq__(self, other: dict):
        return (
            len(other) == 5
            and self.val_int == other["val_int"]
            and self.val_float == other["val_float"]
            and self.val_str == other["val_str"]
            and self.val_bool == other["val_bool"]
            and {"name": "A1", "value": "a1_val", "class": "EnumA"} == other["val_enum"]
        )


class List:
    def __init__(self) -> None:
        self.val_a = [1, 2, 3]
        self.val_b = [1, Scalar(), 10.3, DICTA]
        self.val_nested = [[1, 2], Scalar(), [1, "2", True], [[5, Scalar(), 7], [2]]]


class Tuple:
    def __init__(self) -> None:
        self.val_a = (1, 2, 3)
        self.val_b = (1, Scalar(), 10.3, DICTA)
        self.val_nested = ([1, 2], Scalar(), (1, "2", True), [[5, Scalar(), 7], [2]])
        NamedT = namedtuple("NamedT", "aa bb cc")
        self.val_named = NamedT(0.5, (1, 2), Scalar())


class Dictionary:
    def __init__(self) -> None:
        self.val_dict = {
            "a": 2,
            "b": [1, 20.2, "dan"],
            1: 500,
            EnumA.APPLE: 30,
        }
        self.val_nested_dict = {"a": {"a_in": 1, "b_in": 2}, "c": 3}


class NumpyArray:
    def __init__(self) -> None:
        self.val_numpy_arr = np.array([1, 2, 3])
        self.val_2d_numpy_arr = np.array([[1, 2, 3], [4, 5, 6]])
        self.val_numpy_scalar = np.float128(30)
        self.val_dtype = np.dtype("float")


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


def assert_dict_a(ret):
    assert ret[1] == 3
    assert ret["2"] == 4
    assert ret[(1, 2)] == 10


# self.val_nested = [[1, 2], Scalar(), [1, 2, 3], [[5, Scalar(), 7], [2]]]


def test_scalar():
    ret = generify(Scalar())
    assert ret == Scalar()


def test_list():
    ret = generify(List())
    assert len(ret) == 3

    assert ret["val_a"] == [1, 2, 3]

    assert ret["val_b"] == [1, Scalar(), 10.3, {**DICTA}]

    assert len(ret["val_nested"]) == 4
    assert ret["val_nested"][0] == [1, 2]
    assert ret["val_nested"][1] == Scalar()
    assert ret["val_nested"][2] == [1, "2", True]
    assert ret["val_nested"][3][0] == [5, Scalar(), 7]
    assert ret["val_nested"][3][1] == [2]


def test_tuples():
    ret = generify(Tuple())
    assert len(ret) == 4

    assert ret["val_a"] == (1, 2, 3)

    assert ret["val_b"] == (1, Scalar(), 10.3, {**DICTA})

    assert len(ret["val_nested"]) == 4
    assert ret["val_nested"][0] == [1, 2]
    assert ret["val_nested"][1] == Scalar()
    assert ret["val_nested"][2] == (1, "2", True)
    assert ret["val_nested"][3][0] == [5, Scalar(), 7]
    assert ret["val_nested"][3][1] == [2]

    assert ret["val_named"] == {"aa": 0.5, "bb": (1, 2), "cc": Scalar()}


# def test_dictionary():
#     data = TestDictionary()
#     ser_data = generify(data, log=True)


# def test_numpy_arr():
#     data = TestNumpyArray()
#     ser_data = generify(data, log=True)


# def test_dataframe():
#     data = TestDataframe()
#     ser_data = generify(data, log=True)


# def test_nested_object():
#     data = TestGenicifyNested()
#     ser_data = generify(data, log=True)


# def test_numpy_array_with_class_fail():
#     data = np.array([TestDictionary()])
#     ser_data = generify(data, log=True)


if __name__ == "__main__":
    generify(Scalar(), log=print)
