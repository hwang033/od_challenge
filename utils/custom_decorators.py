"""
This module defines customized decorators
"""

def add_header(name, value):
    """view decorator that sets a response header.

    Example:
        @add_header('Content-Type', 'application/json')
        def view_func(request, ...):
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            response[name] = value
            return response
        return inner
    return decorator
