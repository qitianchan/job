__author__ = 'qitian'


from . import strategies

default_strategy = 'fixed'

def set_store_value(*arg, **kwargs):

    strategy = kwargs.pop('strategy', default_strategy)
    strategy = strategies.strategies[strategy]
    return strategy.set_store_value(*arg, **kwargs)

__all__ = (
    'set_store_value',
)

