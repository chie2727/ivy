"""Collection of tests for unified reduction functions."""

# global
import numpy as np
from hypothesis import given, strategies as st

# local
import ivy
import ivy.functional.backends.numpy as ivy_np
import ivy_tests.test_ivy.helpers as helpers


# random_uniform
@given(
    dtype_and_x=helpers.dtype_and_values(ivy_np.valid_float_dtypes, 2, max_num_dims=1),
    #data=st.data(),
    #input_dtype=st.sampled_from(ivy_np.valid_float_dtypes),
    #as_variable=st.booleans(),
    as_variable=helpers.list_of_length(st.booleans(), 2),
    # shape=helpers.get_shape(),
    with_out=st.booleans(),
    # num_positional_args=st.integers(0, 1),
    num_positional_args=helpers.num_positional_args(fn_name="random_uniform"),
    # num_positional_args=st.shared(st.integers(1, 6), key="random_uniform"),
    #native_array=st.booleans(),
    native_array=helpers.list_of_length(st.booleans(), 2),
    #container=st.booleans(),
    container=helpers.list_of_length(st.booleans(), 2),
    instance_method=st.booleans(),
    # shape = st.sampled_from(ivy_np.valid_int_dtypes),
    # shape = st.integers(1, 3),
)
def test_random_uniform(
    dtype_and_x,
    #data,
    #input_dtype,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    fw,
    # shape,
    device,
):
    input_dtype, x = dtype_and_x
    low = np.asarray(x[0], dtype=input_dtype[0])
    high = np.asarray(x[1], dtype=input_dtype[1])

    #num_positional_args = data.draw(
    #    helpers.num_positional_args(fn_name="random_uniform")
    #)
    #shape = data.draw(helpers.get_shape(min_num_dims=1))
    #shape = data.draw(helpers.get_shape(min_dim_size=1, max_dim_size=2))


    #low, high = data.draw(helpers.array_values(dtype=input_dtype, shape=shape))
    #low, high = data.draw(helpers.get_bounds(input_dtype))

    # values = data.draw(helpers.none_or_list_of_floats(input_dtype, 2, 1, 10, no_none=True))
    #values = data.draw(helpers.array_values(dtype=input_dtype, shape=2, min_value=0))
    #if values[0] is not None and values[1] is not None:
    #    low, high = min(values), max(values)
    #else:
    #    low, high = values[0], values[1]

    # low, high = helpers.get_bounds(data, dtype=input_dtype)
    # if type(low) == float:
    #    low = int(low)
    # if type(high) == float:
    #    high = int(high)

    # shape = helpers.get_shape()
    # shape = data.draw(helpers.get_shape())
    # shape = st.draw(st.shared(helpers.get_shape(), key="shape"))

    #x = data.draw(
    #    helpers.nph.arrays(shape=array_shape, dtype=input_dtype).filter(
    #        lambda x: not np.any(np.isnan(x))
    #    )
    #)

    """
    # smoke test
    if as_variable and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        return
    low_tnsr = ivy.array(low, dtype=input_dtype, device=device) if low is not None else None
    high_tnsr = (
        ivy.array(high, dtype=input_dtype, device=device) if high is not None else None
    )
    if as_variable and (low is not None):
        low_tnsr = ivy.variable(low_tnsr)
    if as_variable and (high is not None):
        high_tnsr = ivy.variable(high_tnsr)
    kwargs = {
        k: v for k, v in zip(["low", "high"], [low_tnsr, high_tnsr]) if v is not None
    }
    if shape is not None:
        kwargs["shape"] = shape
    ret = ivy.random_uniform(**kwargs, device=device)
    """

    helpers.test_function(
        input_dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "random_uniform",
        low=low,
        high=high,
        #shape=shape,
        device=device,
        #dtype=input_dtype,
    )

    """
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    if shape is None:
        assert ret.shape == ()
    else:
        assert ret.shape == shape
    # value test
    ret_np = call(ivy.random_uniform, **kwargs, device=device)
    assert np.min((ret_np < (high if high else 1.0)).astype(np.int32)) == 1
    assert np.min((ret_np >= (low if low else 0.0)).astype(np.int32)) == 1
    """


# random_normal
@given(
    data=st.data(),
    shape=helpers.get_shape(),
    dtype=st.sampled_from(ivy_np.valid_float_dtypes),
    as_variable=st.booleans(),
)
def test_random_normal(data, shape, dtype, as_variable, device, call):
    mean, std = data.draw(helpers.get_mean_std(dtype))
    ivy.seed(0)
    # smoke test
    if as_variable and call is helpers.mx_call:
        # mxnet does not support 0-dimensional variables
        return
    mean_tnsr = (
        ivy.array(mean, dtype=dtype, device=device) if mean is not None else None
    )
    std_tnsr = ivy.array(std, dtype=dtype, device=device) if std is not None else None
    if as_variable and (mean is not None):
        mean_tnsr = ivy.variable(mean_tnsr)
    if as_variable and (std is not None):
        std_tnsr = ivy.variable(std_tnsr)
    kwargs = {
        k: v for k, v in zip(["mean", "std"], [mean_tnsr, std_tnsr]) if v is not None
    }
    if shape is not None:
        kwargs["shape"] = shape
    ret = ivy.random_normal(**kwargs, device=device)
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    if shape is None:
        assert ret.shape == ()
    else:
        assert ret.shape == shape


# multinomial
@given(
    data=st.data(),
    num_samples=st.integers(1, 2),
    replace=st.booleans(),
    dtype=st.sampled_from(ivy_np.valid_float_dtypes),
    tensor_fn=st.sampled_from([ivy.array]),
)
def test_multinomial(data, num_samples, replace, dtype, tensor_fn, device, call):
    probs, population_size = data.draw(helpers.get_probs(dtype))
    if (
        call in [helpers.mx_call, helpers.tf_call, helpers.tf_graph_call]
        and not replace
        or dtype == "float64"
    ):
        # mxnet and tenosorflow do not support multinomial without replacement
        return
    # smoke test
    probs = tensor_fn(probs, dtype=dtype, device=device) if probs is not None else probs
    batch_size = probs.shape[0] if probs is not None else 2
    ret = ivy.multinomial(population_size, num_samples, batch_size, probs, replace)
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    assert ret.shape == tuple([batch_size] + [num_samples])


# randint
@given(
    data=st.data(),
    shape=helpers.get_shape(allow_none=False, min_num_dims=1, min_dim_size=1),
    dtype=st.sampled_from(ivy_np.valid_int_dtypes),
    as_variable=st.booleans(),
    with_out=st.booleans(),
    #num_positional_args=helpers.num_positional_args(fn_name="randint"),
    num_positional_args=st.integers(3, 3),
    native_array=st.booleans(),
    container=st.booleans(),
    instance_method=st.booleans(),
)
def test_randint(
    data,
    shape,
    dtype,
    as_variable,
    with_out,
    num_positional_args,
    native_array,
    container,
    instance_method,
    device,
    #call,
    fw,
):
    #NEXT: ret_from_np and ret: x and y
    if type(shape) == tuple:
        shape = list(shape)
        #shape = shape[0]
    #else:
    #    shape = list(shape)

    val = data.draw(
        helpers.array_values(dtype, (2,), min_value=0)
    )

    #val2 = data.draw(helpers.array_values(dtype, arr_shape, min_value=0))
    if val[1] > val[0]:
        low = val[0]
        high = val[1]
    elif val[1] < val[0]:
        low = val[1]
        high = val[0]
    elif val[1] == val[0]:
        low = val[0]
        high = val[1]+1


    # PyTorch and MXNet do not support non-float variables
    if fw == "torch" and dtype in ["int8", "int16", "int32", "int64"]:
        return
    if dtype[0] == "u":
        return

    '''
    low, high = tuple(data.draw(helpers.get_bounds(dtype)))
    
    low_tnsr = ivy.array(low, dtype=dtype, device=device)
    high_tnsr = ivy.array(high, dtype=dtype, device=device)
    if as_variable:
        low_tnsr, high_tnsr = ivy.variable(low_tnsr), ivy.variable(high_tnsr)
    kwargs = {
        k: v for k, v in zip(["low", "high"], [low_tnsr, high_tnsr]) if v is not None
    }
    kwargs["shape"] = shape
    ret = ivy.randint(**kwargs, device=device)
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    assert ret.shape == shape
    # value test
    #ret_np = call(ivy.randint, **kwargs, device=device)
    #assert np.min((ret_np < high).astype(np.int64)) == 1
    #assert np.min((ret_np >= low).astype(np.int64)) == 1
    '''

    helpers.test_function(
        dtype,
        as_variable,
        with_out,
        num_positional_args,
        native_array,
        container,
        instance_method,
        fw,
        "randint",
        low=low,
        high=high,
        #low=np.asarray(low, dtype=dtype),
        #high=np.asarray(high, dtype=dtype),
        shape=shape,
        device=device,
    )


# seed
@given(
    seed_val=st.integers(min_value=0, max_value=2147483647),
)
def test_seed(seed_val):
    # smoke test
    ivy.seed(seed_val)


# shuffle
@given(
    data=st.data(),
    dtype=st.sampled_from(ivy_np.valid_float_dtypes),
    as_variable=st.booleans(),
)
def test_shuffle(data, dtype, as_variable, device, call):
    # smoke test
    shape = data.draw(helpers.get_shape(min_num_dims=1))
    x = data.draw(helpers.array_values(dtype, shape))
    x = ivy.array(x, dtype=dtype, device=device)
    if as_variable:
        x = ivy.variable(x)
    ret = ivy.shuffle(x)
    # type test
    assert ivy.is_ivy_array(ret)
    # cardinality test
    assert ret.shape == x.shape
    # value test
    ivy.seed(0)
    first_shuffle = call(ivy.shuffle, x)
    ivy.seed(0)
    second_shuffle = call(ivy.shuffle, x)
    assert np.array_equal(first_shuffle, second_shuffle)
