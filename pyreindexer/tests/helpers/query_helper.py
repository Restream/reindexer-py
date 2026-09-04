def call(q, name):
    r = getattr(q, name)()
    return r if r is not None else q
