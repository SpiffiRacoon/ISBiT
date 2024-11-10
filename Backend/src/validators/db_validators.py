def validate_endpoint_args(func):
    """
    This functions makes sure that arguments comming from a endpoint does not contain
    unallowed values.

    For this validator to work as expected, the function arguments needs to be given as kwargs:
        e.g. func(collection=collection)
    """

    def wrapper_func(*args, **kwargs):
        not_allowed_collection_names = ["About", "about", "Labels", "labels"]
        for collection_name in ["collection", "dataset_name"]:
            if collection_name in kwargs:
                if kwargs[collection_name] in not_allowed_collection_names:
                    raise Exception(f"Usage of unallowed {collection_name} name")

        func(*args, **kwargs)

    return wrapper_func
