import json
from pipeline import main, PreferenceMatch

product_fixture = 'product_data.json'

with open(product_fixture) as f:
    product_data = json.load(f)


def test_main_empty_inputs():
    test_items = []
    result_items = main(product_data, [], [])
    assert test_items == result_items


def test_main_single_include_arg():
    test_items = [
        PreferenceMatch(product_name='T-Shirt', product_codes=["A21313"])
    ]
    result_items = main(product_data, ["red"], [])
    assert test_items == result_items


def test_main_multiple_include_arg():
    test_items = [
        PreferenceMatch(product_name='T-Shirt', product_codes=["A21313","A21311"])
    ]
    result_items = main(product_data, ["red", "black"], [])
    assert test_items == result_items


def test_main_multiple_include_arg_additional_products():
    test_items = [
        PreferenceMatch(product_name='T-Shirt', product_codes=["A21312"]),
        PreferenceMatch(product_name='Pants', product_codes=["A21455"]),
        PreferenceMatch(product_name='Socks', product_codes=["A21412"])
    ]
    result_items = main(product_data, ["green"], [])
    assert test_items == result_items


def test_main_single_exclude_arg():
    test_items = []
    result_items = main(product_data, [], ["large"])
    assert test_items == result_items


def test_main_multiple_exclude_arg():
    test_items = []
    result_items = main(product_data, [], ["medium", "large"])
    assert test_items == result_items


def test_main_include_exclude_arg():
    test_items = [
        PreferenceMatch(product_name='T-Shirt', product_codes=["A21312"]),
        PreferenceMatch(product_name='Pants', product_codes=["A21455"])
    ]
    result_items = main(product_data, ["red", "green"], ["large"])
    assert test_items == result_items


def test_main_include_exclude_multiple_arg():
    test_items = [
        PreferenceMatch(product_name='T-Shirt', product_codes=["A21312", "A21311"]),
        PreferenceMatch(product_name='Pants', product_codes=["A21455"]),
        PreferenceMatch(product_name='Socks', product_codes=["A21412"])
    ]
    result_items = main(product_data, ["medium", "large"], ["red", "blue"])
    assert test_items == result_items
