
def has_perm(lst):
    def decorator(f):
        def wrapped(request, *args, **kwargs):
            return f(request, *args, **kwargs)
        return wrapped
    return decorator
