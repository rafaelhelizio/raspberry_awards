from functools import lru_cache
from .environment import Environment


@lru_cache()
def get_environment():
    """Helper function to get env with lru cache"""
    return Environment()
