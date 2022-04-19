import json
from pipeline import main

product_fixture = 'product_data.json'

with open(product_fixture) as f:
    product_data = json.load(f)


def test_main_include():
    import types
    test_items = [
        types.SimpleNamespace(product_name="test_name_1", product_codes=["100", "200"]),
        types.SimpleNamespace(product_name="test_name_2", product_codes=["300", "400"])
    ]
    result_items = main(product_data, ["red", "large"], [])
    assert test_items == result_items
