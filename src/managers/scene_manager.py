class SceneManager:
    def __init__(self):
        self._current = None

    def set_scene(self, scene):
        self._current = scene

    def handle_event(self, event):
        if self._current:
            self._current.handle_event(event)

    def update(self):
        if self._current:
            self._current.update()

    def draw(self, screen):
        if self._current:
            self._current.draw(screen)
