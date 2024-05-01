# Simple pygame program

# Import and initialize the pygame library
from copy import deepcopy
from dataclasses import dataclass
from math import sqrt
from random import random

import pygame as game
import pygame.draw as pyg_draw
from pygame import Surface, display, time

from py_physics.sim import (
    Body,
    Simulation,
    handle_boundry_colision,
    handle_coliding_bodies,
)
from py_physics.vectors import (
    Vec2,
    add_vectors,
    dot_product,
    scale_vec,
    subtract_vectors,
)

game.init()


# Set up the drawing window
simulation_boundries = Vec2(500, 500)
# TODO: have margin around the boundries in the window
# window_size >> simulation_boundries
surface = display.set_mode(simulation_boundries.as_tuple())

clock = time.Clock()

dt = 0
init_y = 50
init_v = 0
# This doesn't have much meaning without some kind of scale,
# But at least this will remind me of what the term is for
g = 9.8 / 2
t = 0
scale = 100

WHITE = (255, 255, 255)
DARK_GRAY = (25, 25, 25)
GRAVITY = Vec2(0, 9.8)


# TODO: multiply random weights by current_sim.boundaries.x|y
# NOTE: I assume random locations need to be checked to prevent overlaps?
def setup_simulation(body_count=10):
    current_sim = Simulation(
        GRAVITY, 0.0, simulation_boundries, surface, False, [], 0.85
    )
    current_sim.bodies = [
        Body(
            radius=30 * random(),
            mass=10,
            pos=Vec2(
                current_sim.boundaries.x * random(), current_sim.boundaries.y * random()
            ),
            vel=Vec2(10*random(), 10*random()),
        )
        for _ in range(body_count)
    ]
    return current_sim


def draw(surface: Surface, current_sim: Simulation):
    surface.fill((255, 255, 255))
    for body in current_sim.bodies:
        # Fill the background with white
        pyg_draw.circle(
            surface=surface,
            color=DARK_GRAY,
            center=body.pos.as_tuple(),
            radius=body.radius,
        )


def simulate(current_sim: Simulation):
    for i, body in enumerate(current_sim.bodies):
        body.update(current_sim.dt, current_sim.gravity)
        for j in range(i + 1, len(current_sim.bodies)):
            body_2 = current_sim.bodies[j]
            handle_coliding_bodies(body, body_2, current_sim.restitution)
        handle_boundry_colision(body, current_sim.boundaries)


if __name__ == "__main__":

    simulation = setup_simulation()
    running = True
    while running:

        # Did the user click the window close button?
        for event in game.event.get():
            if event.type == game.QUIT:
                running = False

        simulate(simulation)

        draw(surface, simulation)

        # Flip the display
        display.flip()

        simulation.dt = clock.tick(60) / scale
        print(simulation.bodies[0].pos)

    # Done! Time to quit.
    game.quit()

    # Run until the user asks to quit
