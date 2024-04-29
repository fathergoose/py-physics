# Simple pygame program

# Import and initialize the pygame library
import pygame as game
from pygame import Surface, display, time
import pygame.draw as pyg_draw
from math import sqrt
from random import random
from copy import deepcopy
from dataclasses import dataclass

game.init()

# Set up the drawing window
screen = display.set_mode([500, 500])

clock = time.Clock()

dt = 0
init_y = 50
init_v = 0
# This doesn't have much meaning without some kind of scale,
# But at least this will remind me of what the term is for
g = 9.8/2
t = 0
scale = 100

DARK_GRAY = (245, 245, 245)


@dataclass(frozen=True)
class Vec2:
    x: float
    y: float

    def clone(self):
        return deepcopy(self)

    def length(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)


def scale_vec(vec: Vec2, factor: float) -> Vec2:
    return Vec2(vec.x * factor, vec.y * factor)

def add_vectors(a: Vec2, b: Vec2) -> Vec2:
    return Vec2(a.x + b.x, a.y + b.y)

def subtract_vectors(a: Vec2, b: Vec2) -> Vec2:
    return Vec2(a.x - b.x, a.y - b.y)

def dot_product(a: Vec2, b: Vec2) -> float:
    return a.x * b.x + a.y * b.y


@dataclass
class Body:
    radius: float
    mass: float
    pos: Vec2
    vel: Vec2

    def __init__(self, radius: float, mass: float, pos: Vec2, vel: Vec2):
        self.radius = radius
        self.mass = mass
        self.pos = pos.clone()
        self.vel = vel.clone()

    def update(self, dt: float, gravity: Vec2):
        self.vel = add_vectors(self.vel, scale_vec(gravity, dt))
        self.pos = add_vectors(self.pos, scale_vec(self.vel, dt))



@dataclass
class Simulation:
    gravity: Vec2
    dt: float
    boundaries: Vec2
    surface: Surface
    paused: bool
    bodies: list[Body]
    restitution: float


current_sim = Simulation(Vec2(0.0,0.0), 0.0, Vec2(100.0, 200.0), screen, False, [], 1.0)

def setup_simulation():
    body_count = 10
    # TODO: multiply random weights by current_sim.boundaries.x|y 
    # INFO: I assume random locations need to be checked to prevent overlaps?
    current_sim.bodies = [
            Body(10, 10, Vec2(random(), random()), Vec2(random(), random()))
            for _ in range(body_count)]
    
# TODO: The example I'm following has this function handling all the platform specific graphics generation
# Draw the visual representations of your simulatied bodies in this function

# INFO: Parameter docs for pygame.draw.circle()

# circle(
        # surface: Surface, 
        # color: Color|int|Tuple, 
        # ceneter: 2Vector|Tuple[float|int]|List[float|int], 
        # radius: float|int)
# )

def draw():
    for body in current_sim.bodies:
        pyg_draw.circle(surface=screen, color=DARK_GRAY, center=body.pos.as_tuple(), radius=body.radius)
        return False

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))


    t = t + dt
    y = t**2 * g + t * init_v + init_y


    pyg_draw.circle(screen, (0, 25, 25), (250, y), 10)

    # Flip the display
    display.flip()

    dt = clock.tick(60) / scale
    print(t)


# Done! Time to quit.
game.quit()
