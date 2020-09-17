def multiple_filter(filters, tuples):
    for f in filters:
        tuples = filter(f, tuples)
    return tuples
