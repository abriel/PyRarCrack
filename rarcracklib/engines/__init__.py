try:
    from .subprocess import give_a_try
except ModuleNotFoundError:
    pass

try:
    from .unrar import give_a_try
except ModuleNotFoundError:
    pass

try:
    from .unrardll import give_a_try
except ModuleNotFoundError:
    pass
