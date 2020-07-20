from pprint import pprint

template_performance = [
    (
        "e79aa26b-c57e-490b-bca4-c45e1c542ec4",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "7554a0ae-8d6b-44e5-9fd8-d33c7bf93e26",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "10f67f99-96de-4759-b608-15100561c0ea",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "af75a601-da59-4845-b552-39610bbd9b3b",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "9b2139e1-68a5-4a4c-8c0b-c3e72baee36a",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "7066e8fc-c5d7-4b4e-8426-12a3c76f614e",
        {
            "clicked_ratio": None,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
    (
        "40b2e6a4-6394-4586-be3d-bfe2d09471c3",
        {
            "clicked_ratio": 10,
            "opened_ratio": None,
            "reported_ratio": None,
            "submitted_ratio": None,
        },
    ),
]

pprint(sorted(template_performance, key=lambda x: x[1], reverse=True))
print(type(template_performance))
