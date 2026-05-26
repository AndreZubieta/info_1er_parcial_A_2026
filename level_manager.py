import pymunk

from game_object import Bird, Pig, Column, YellowBird, BlueBird
from game_logic import ImpulseVector
from levels.level_1 import LEVEL as LEVEL_1


LEVELS = [
    LEVEL_1,
]

# -----------------------------
# Level Manager
# -----------------------------

class LevelManager:
    def __init__(self, app):
        """
        app = reference to main App (Arcade View)
        """
        self.app = app
        self.current_level_index = 0

    # -------------------------
    # PUBLIC API
    # -------------------------

    def load_level(self, index: int):
        """Loads a level from LEVELS list."""
        if index >= len(LEVELS):
            print("No more levels!")
            return

        self.clear_level()

        level_data = LEVELS[index]

        self.spawn_columns(level_data.get("columns", []))
        self.spawn_pigs(level_data.get("pigs", []))

        # You can later use this to decide starting birds
        self.setup_birds(level_data.get("birds", []))

        self.current_level_index = index

    def next_level(self):
        """Switch to next level."""
        self.load_level(self.current_level_index + 1)

    def reset_level(self):
        """Reload current level."""
        self.load_level(self.current_level_index)

    # -------------------------
    # CLEARING WORLD
    # -------------------------

    def clear_level(self):

        for obj in self.app.world:

            # remove physics objects
            if hasattr(obj, "body") and hasattr(obj, "shape"):
                self.app.space.remove(obj.body, obj.shape)

            # remove sprite
            obj.remove_from_sprite_lists()

        self.app.world.clear()
        self.app.birds.clear()

        self.app.active_bird = None

    def spawn_pigs(self, pigs_data):
        for p in pigs_data:
            pig = Pig(p["x"], p["y"], self.app.space)
            self.app.sprites.append(pig)
            self.app.world.append(pig)

    def spawn_columns(self, columns_data):
        for c in columns_data:
            column = Column(c["x"], c["y"], self.app.space)
            self.app.sprites.append(column)
            self.app.world.append(column)

    def setup_birds(self, bird_list):
        """
        Creates the bird queue for this level.
        """
        self.app.bird_queue = list(bird_list)

        # set first active bird type
        if len(self.app.bird_queue) > 0:
            self.app.active_bird_type = self.app.bird_queue[0]
        else:
            self.app.active_bird_type = None

    def consume_next_bird(self):
        """
        Called AFTER a bird is launched.
        Moves queue forward.
        """

        if not hasattr(self.app, "bird_queue"):
            return

        if len(self.app.bird_queue) > 0:
            self.app.bird_queue.pop(0)

        if len(self.app.bird_queue) > 0:
            self.app.active_bird_type = self.app.bird_queue[0]
        else:
            self.app.active_bird_type = None    

    # -------------------------
    # BIRD FACTORY (future use)
    # -------------------------

    def create_bird(self, bird_type, impulse_vector, x, y):
        """
        Centralized bird creation system.
        This avoids if/else logic in main.py.
        """

        if bird_type == "yellow":
            return YellowBird(impulse_vector, x, y, self.app.space)

        if bird_type == "blue":
            return BlueBird(impulse_vector, x, y, self.app.space)

        # default bird
        return Bird(impulse_vector, x, y, self.app.space)