def validate_endpoint_args(func):
    """
    This functions makes sure that arguments comming from a endpoint does not contain
    unallowed values.

    For this validator to work as expected, the function arguments needs to be given as kwargs:
        e.g. func(collection=collection)
    """

    def wrapper_func(*args, **kwargs):
        not_allowed_collection_names = ["About", "about"]
        if "collection" in kwargs:
            if kwargs["collection"] in not_allowed_collection_names:
                raise Exception("Usage of unallowed collection name")
        func(*args, **kwargs)

    return wrapper_func
