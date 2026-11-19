class Singleton(type):
    """
    Metaclass ensuring that a class has only one instance.

    All classes that use Singleton as metaclass will have only one
    instance (https://refactoring.guru/fr/design-patterns/singleton).
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Return the unique instance of the class, creating it if needed.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to the constructor.
        **kwargs : dict
            Keyword arguments passed to the constructor.

        Returns
        -------
        object
            Unique instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
