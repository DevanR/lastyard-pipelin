import json
from pipeline import main

product_fixture = 'product_data.json'

with open(product_fixture) as f:
    product_data = json.load(f)


def test_main_empty_inputs():
    test_items = {}
    result_items = main(product_data, [], [])
    assert test_items == result_items


def test_main_single_include_arg():
    test_items = {
        'T-Shirt': ["A21313"]
    }
    result_items = main(product_data, ["red"], [])
    assert test_items == result_items


def test_main_multiple_include_arg():
    test_items = {
        'T-Shirt': ["A21313", "A21311"]
    }
    result_items = main(product_data, ["red", "black"], [])
    assert test_items == result_items


def test_main_multiple_include_arg_additional_products():
    test_items = {
        'T-Shirt': ["A21312"],
        'Pants': ["A21455"],
        'Socks': ["A21412"]
    }
    result_items = main(product_data, ["green"], [])
    assert test_items == result_items


def test_main_single_exclude_arg():
    test_items = {
        'T-Shirt': ["A21312"],
        'Pants': ["A21455", "A21317"],
        'Jacket': ["A21501", "A21502"]
    }
    result_items = main(product_data, [], ["large"])
    assert test_items == result_items

