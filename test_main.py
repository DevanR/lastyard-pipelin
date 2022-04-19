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
