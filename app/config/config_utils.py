class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__( *args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
