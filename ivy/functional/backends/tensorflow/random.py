"""Collection of TensorFlow random functions, wrapped to fit Ivy syntax and
signature.
"""

# global
import tensorflow as tf
from typing import Optional, Union, Sequence

# local
import ivy
from ivy.functional.ivy.device import default_device


# Extra #
# ------#


def random_uniform(
    low: Union[float, tf.Tensor, tf.Variable] = 0.0,
    high: Union[float, tf.Tensor, tf.Variable] = 1.0,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    *,
    device: str,
    dtype: tf.dtypes.DType,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    low = tf.cast(low, dtype)
    high = tf.cast(high, dtype)
    if isinstance(shape, tf.Tensor):
        shape = list(shape)
    with tf.device(default_device(device)):
        return tf.random.uniform(shape if shape else (), low, high, dtype=dtype)


random_uniform.unsupported_dtypes = ("int8", "int16", "uint8",
                                        "uint16", "uint32", "uint64",)


def random_normal(
    mean: Union[float, tf.Tensor, tf.Variable] = 0.0,
    std: Union[float, tf.Tensor, tf.Variable] = 1.0,
    shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    *,
    device: str,
    dtype: tf.dtypes.DType,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    mean = tf.cast(mean, dtype)
    std = tf.cast(std, dtype)
    with tf.device(default_device(device)):
        return tf.random.normal(shape if shape else (), mean if mean else 0.0, std if std else 1.0, dtype=dtype)


def multinomial(
    population_size: int,
    num_samples: int,
    batch_size: int = 1,
    probs: Optional[Union[tf.Tensor, tf.Variable]] = None,
    replace: bool = True,
    *,
    device: str,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    if not replace:
        raise Exception("TensorFlow does not support multinomial without replacement")
    device = default_device(device)
    with tf.device("/" + device.upper()):
        if probs is None:
            probs = (
                tf.ones(
                    (
                        batch_size,
                        population_size,
                    )
                )
                / population_size
            )
        return tf.random.categorical(tf.math.log(probs), num_samples)


def randint(
    low: int,
    high: int,
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    device: str,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    device = default_device(device)
    low = tf.cast(low, "int64")
    high = tf.cast(high, "int64")
    with tf.device("/" + device.upper()):
        return tf.random.uniform(shape=shape, minval=low, maxval=high, dtype=tf.int64)


def seed(
    seed_value: int = 0,
) -> None:
    tf.random.set_seed(seed_value)


def shuffle(
    x: Union[tf.Tensor, tf.Variable],
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.random.shuffle(x)
