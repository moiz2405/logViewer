"""
Configuration module for sharing runtime settings across services.
"""
import threading

class Config:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Config, cls).__new__(cls)
                cls._instance._bad_ratio = 2  # Default bad_ratio value
                cls._instance._callbacks = []  # Callbacks to notify when bad_ratio changes
        return cls._instance
    
    @property
    def bad_ratio(self):
        return self._bad_ratio
    
    @bad_ratio.setter
    def bad_ratio(self, value):
        if not isinstance(value, int) or not (0 <= value <= 10):
            raise ValueError("bad_ratio must be an integer between 0 and 10")
        
        self._bad_ratio = value
        
        # Notify all registered callbacks
        for callback in self._callbacks:
            callback(value)
    
    def register_callback(self, callback):
        """Register a callback to be notified when bad_ratio changes."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def unregister_callback(self, callback):
        """Unregister a callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

# Create a global config instance
config = Config()
