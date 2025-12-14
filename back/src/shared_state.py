class SharedState:
    """Shared state manager to store and retrieve data between agents."""

    _instance = None
    _initialized = False

    def __new__(cls):
        import traceback

        if cls._instance is None:
            print(f"[SharedState] Creating NEW instance")
            print(f"[SharedState] Call stack:")
            for line in traceback.format_stack()[:-1]:
                print(line.strip())
            cls._instance = super(SharedState, cls).__new__(cls)
            cls._instance.image_path = None
            cls._instance.video_path = None
            cls._initialized = True
            print(f"[SharedState] NEW instance created with ID: {id(cls._instance)}")
        else:
            print(f"[SharedState] Returning EXISTING instance ID: {id(cls._instance)}")
        return cls._instance

    def __init__(self):
        # Don't reset attributes - they were initialized in __new__
        print(
            f"[SharedState.__init__] Called on instance ID: {id(self)}, current state: {self.__dict__}"
        )
        pass

    def get_shared_state(self):
        return self._instance

    def close_shared_state(self):
        SharedState._instance = None

    def set_image_path(self, path: str):
        """Store the generated image path."""
        print(f"[SharedState.set_image_path] Called on instance ID: {id(self)}")
        print(f"[SharedState.set_image_path] Before: image_path={self.image_path}")
        self.image_path = path
        print(f"[SharedState.set_image_path] After: image_path={self.image_path}")
        print(f"[SharedState] Image path stored: {path}")

    def get_image_path(self) -> str | None:
        """Retrieve the stored image path."""
        print(f"[SharedState.get_image_path] Called on instance ID: {id(self)}")
        print(f"[SharedState.get_image_path] Returning: {self.image_path}")
        return self.image_path

    def set_video_path(self, path: str):
        """Store the generated video path."""
        self.video_path = path
        print(f"[SharedState] Video path stored: {path}")

    def get_video_path(self) -> str | None:
        """Retrieve the stored video path."""
        return self.video_path

    def clear(self):
        """Clear all stored state."""
        self.image_path = None
        self.video_path = None
        print("[SharedState] State cleared")
