
from threading import Lock


class MetaSingleton(type):
    """This is a thread-safe implementation of Singleton.

    Attributes
    ----------
    _instances
        Dictionary with the keys containing the classes and the values containing the instances of each class.
    _lock
        Lock used to synchronize threads.

    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """Create one and only one instance of a Class."""
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
