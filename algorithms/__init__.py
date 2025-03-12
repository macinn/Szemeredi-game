registry = {}
def register_algorithm(name):
    def decorator(func):
        registry[name.lower()] = func
        return func
    return decorator

from . import random_ai
