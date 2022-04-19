import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""

    # VERSION 1: Iterative selection and filtering
    #    selected_products = []
    #
    #    # Filter for include_tags
    #    if include_tags:
    #        for product in product_data:
    #            if any(tag in product["tags"] for tag in include_tags):
    #                selected_products.append(product)
    #
    #    # Filter for exclude_tags
    #    if exclude_tags:
    #        for product in selected_products:
    #            if any(tag in product["tags"] for tag in exclude_tags):
    #                selected_products.remove(product)
    # -------------------------------------------------------------------

    # VERSION 2: Lazy generator expression for larger JSON files
    #    selected_products = (product for product in product_data if
    #                         any(tag in product["tags"] for tag in include_tags) and all(
    #                             tag not in product["tags"] for tag in exclude_tags))
    # -------------------------------------------------------------------

    # VERSION 3: Search optimisation with a dictionary

    # Create tag dict
    product_dict = {}
    for product in product_data:
        for tag in product["tags"]:
            if tag not in product_dict.keys():
                product_dict[tag] = []

            product_dict[tag].append((product["name"], product["code"]))

    # Get included products
    included_products = []
    for tag in include_tags:
        if tag in product_dict.keys():
            for prod in product_dict[tag]:
                included_products.append(prod)

    # Get excluded products
    excluded_products = []
    for tag in exclude_tags:
        if tag in product_dict.keys():
            for prod in product_dict[tag]:
                excluded_products.append(prod)

    # Get included - excluded products
    selected_products = [product for product in included_products if product not in excluded_products]

    # Package result
    result = {}
    for product in selected_products:
        if product[0] not in result.keys():
            result[product[0]] = [product[1]]
        else:
            if product[1] not in result[product[0]]:
                result[product[0]].append(product[1])

    output = []
    for key in result.keys():
        match = PreferenceMatch(product_name=key, product_codes=result[key])
        output.append(match)

    return output


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
