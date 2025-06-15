class GameTimer:
    def __init__(self):
        self.time = 0
        self.paused = False

    def update(self, dt):
        if not self.paused:
            self.time += dt

    def reset(self):
        self.time = 0

    def get_time(self):
        return self.time

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
