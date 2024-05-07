from dataclasses import dataclass

from pygame import Surface

from py_physics.vectors import (
    Vec2,
    add_vectors,
    dot_product,
    scale_vec,
    subtract_vectors,
)


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

def handle_coliding_bodies(body_1: Body, body_2: Body, restitution: float):
    direction = subtract_vectors(body_2.pos, body_1.pos)
    direction_length = direction.length()
    if direction_length == 0.0 or direction_length > body_1.radius + body_2.radius:
        return

    normalized_direction = scale_vec(direction, 1 / direction_length)
    correction_vector = (body_1.radius + body_2.radius - direction_length) / 2.0
    body_1.pos = add_vectors(body_1.pos, normalized_direction, -correction_vector)
    body_2.pos = add_vectors(body_2.pos, normalized_direction, correction_vector)
    v1 = dot_product(body_1.vel, normalized_direction)
    v2 = dot_product(body_2.vel, normalized_direction)

    m1 = body_1.mass
    m2 = body_2.mass

    v1_prime = (m1 * v1 + m2 * v2 - m2 * (v1 - v2) * restitution) / (m1 + m2)
    v2_prime = (m1 * v1 + m2 * v2 - m1 * (v2 - v1) * restitution) / (m1 + m2)

    body_1.vel = add_vectors(body_1.vel, normalized_direction, v1_prime - v1)
    body_2.vel = add_vectors(body_2.vel, normalized_direction, v2_prime - v2)


def handle_boundry_colision(body: Body, sim_boundries: Vec2):
    # Left | Min x
    if body.pos.x < body.radius:
        body.pos = Vec2(body.radius, body.pos.y)
        body.vel = Vec2(-body.vel.x, body.vel.y)
    # Right | Max x
    if body.pos.x > sim_boundries.x - body.radius:
        body.pos = Vec2(sim_boundries.x - body.radius, body.pos.y)
        body.vel = Vec2(-body.vel.x, body.vel.y)
    # Bottom | Min y
    if body.pos.y < body.radius:
        body.pos = Vec2(body.pos.x, body.radius)
        body.vel = Vec2(body.vel.x, -body.vel.y)
    # Top | Max y
    if body.pos.y > sim_boundries.y - body.radius:
        body.pos = Vec2(body.pos.x, sim_boundries.y - body.radius)
        body.vel = Vec2(body.vel.x, -body.vel.y)
