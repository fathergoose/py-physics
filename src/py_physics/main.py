# Simple pygame program

# Import and initialize the pygame library
import math
from random import random

import pygame as game
import pygame.draw as pyg_draw
import pygame_gui
from pygame import Surface, display, time

from py_physics.sim import (
    Body,
    Simulation,
    handle_boundry_colision,
    handle_coliding_bodies,
)
from py_physics.vectors import (
    Vec2,
)

game.init()


# Set up the drawing window
simulation_boundries = Vec2(500, 500)
window_boundries = (700, 500)
# TODO: have margin around the boundries in the window
# window_size >> simulation_boundries
window_surface = display.set_mode(window_boundries)

background = game.Surface((200, 500))
background.fill(game.Color("#e3e3e3"))

clock = time.Clock()


WHITE = (255, 255, 255)
BG_GRAY = (227, 227, 227)
DARK_GRAY = (25, 25, 25)
GRAVITY = Vec2(0, 9.8)
DENSITY = 1.0

manager = pygame_gui.UIManager(window_boundries)

restart_button = pygame_gui.elements.UIButton(
    relative_rect=game.Rect((550, 60), (100, 50)), text="restart", manager=manager
)


def setup_simulation(body_count=10):
    current_sim = Simulation(
        GRAVITY, 0.0, simulation_boundries, window_surface, False, [], 0.85
    )
    current_sim.bodies = [
        Body(
            (radius := 30 * random()),
            (DENSITY * (math.pi * 4 / 3 * radius**3)),
            pos=Vec2(
                current_sim.boundaries.x * random(), current_sim.boundaries.y * random()
            ),
            vel=Vec2(10 * random(), 10 * random()),
        )
        for _ in range(body_count)
    ]
    return current_sim


def draw(surface: Surface, current_sim: Simulation):
    surface.fill((255, 255, 255))
    for body in current_sim.bodies:
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



def main():
    simulation = setup_simulation()
    running = True
    while running:

        # Did the user click the window close button?
        for event in game.event.get():
            if event.type == game.QUIT:
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    print("hi alex!!!")
            manager.process_events(event)

        simulate(simulation)
        draw(window_surface, simulation)

        simulation.dt = clock.tick(60) / 100.0
        manager.update(simulation.dt)
        window_surface.blit(background, (500, 0))

        manager.draw_ui(window_surface)

        display.update()

    # Done! Time to quit.
    game.quit()

if __name__ == "__main__":
    main()