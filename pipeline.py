import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""

    selected_products = []

    # Filter for include_tags
    if include_tags:
        for product in product_data:
            if any(tag in product["tags"] for tag in include_tags):
                selected_products.append(product)

    # Filter for exclude_tags
    if exclude_tags:
        for product in product_data:
            if all(tag not in product["tags"] for tag in exclude_tags):
                selected_products.append(product)


    # Package result
    result = {}
    for product in selected_products:
        if product["name"] in result.keys():
            result[product["name"]].append(product["code"])
        else:
            result[product["name"]] = [product["code"]]

    return result


if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]


    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, "\n".join(item.product_codes)))
