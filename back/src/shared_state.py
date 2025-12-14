from logging import Logger

logger = Logger("shared_state")


class SharedState:
    """Shared state manager to store and retrieve data between agents."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedState, cls).__new__(cls)
            cls._instance.image_path = None
            cls._instance.video_path = None
            cls._initialized = True
        return cls._instance

    def __init__(self):
        pass

    def get_shared_state(self):
        return self._instance

    def close_shared_state(self):
        SharedState._instance = None

    def set_image_path(self, path: str):
        """Store the generated image path."""
        self.image_path = path
        logger.info(
            f"[SharedState.set_image_path] image path set: image_path={self.image_path}"
        )

    def get_image_path(self) -> str | None:
        """Retrieve the stored image path."""
        return self.image_path

    def set_video_path(self, path: str):
        """Store the generated video path."""
        self.video_path = path
        logger.info(
            f"[SharedState.set_video_path] video path set: video_path={self.video_path}"
        )

    def get_video_path(self) -> str | None:
        """Retrieve the stored video path."""
        return self.video_path

    def clear(self):
        """Clear all stored state."""
        self.image_path = None
        self.video_path = None
