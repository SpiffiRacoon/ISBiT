def validate_endpoint_args(func):
    """
    This functions makes sure that arguments comming from a endpoint does not contain
    unallowed values.

    For this validator to work as expected, the function arguments needs to be given as kwargs:
        e.g. func(collection=collection)
    """

    def wrapper_func(*args, **kwargs):
        reserved_names = ["about", "ml_runs"]
        not_allowed_collection_names = []
        for one_name in reserved_names:
            not_allowed_collection_names.append(one_name)
            not_allowed_collection_names.append(one_name.capitalize())

        if "collection" in kwargs:
            if kwargs["collection"] in not_allowed_collection_names:
                raise Exception("Usage of unallowed collection name")
        func(*args, **kwargs)

    return wrapper_func
