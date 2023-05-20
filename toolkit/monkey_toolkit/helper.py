import monkey


jj = dict()


def get_quad(batch, **kwargs):
    global jj
    key = frozenset(kwargs.items())
    if key in jj:
        return jj[key]
    b = monkey.models.quad(batch, **kwargs)
    jj[key] = b
    return b
