import pygame
import math

from vector2 import *

GRAVITY = -9.80665

class Physical_Object:

  def __init__(self, initial_pos, in_angle, launch_speed):
    self.pos = initial_pos
    self.radius = 1
    self.trajectory_color = (255, 0, 0)
    self.angle = in_angle
    self.launch_speed = launch_speed
    self.trajectory = []
    self.viscosity = 0.2
    self.forces = []
    self.mass = 5
    self.gravity = GRAVITY
    self.max_height = 0

  def add_force(self, in_force):
    if not isinstance(in_force, Vector2):
      raise TypeError("Force to add must be a Vector2!")

    self.forces.append(in_force)

  def remove_force(self, index):
    if not isinstance(index, int):
      raise TypeError("Index must be an integer!")

    self.forces.pop(index)

  def set_launch_speed(self, new_speed):
    self.launch_speed = new_speed

  def set_angle(self, new_angle):
    self.angle = new_angle

  def set_mass(self, new_mass):
    self.mass = new_mass

  def set_gravity(self, new_gravity):
    self.gravity = new_gravity * -1

  def set_viscosity(self, new_viscosity):
    self.viscosity = new_viscosity

  def get_viscocity_acceleration(self, velocity):
    a = Vector2(0, 0)
    velocity_magnitude = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
    velocity_unit = velocity / velocity_magnitude

    force = Vector2(0, 0)
    force.x = self.viscosity * velocity_unit.x * (velocity_magnitude * velocity_magnitude)
    force.y = self.viscosity * velocity_unit.y * (velocity_magnitude * velocity_magnitude)

    a.x = force.x / self.mass
    a.y = force.y / self.mass

    return a

  def get_constant_acceleration(self):
    acceleration = Vector2(0, 0)

    for force in self.forces:
      a = Vector2(0, 0)
      a.x = force.x / self.mass
      a.y = force.y / self.mass

      acceleration += a

    # Add gravity
    acceleration.y += self.gravity

    return acceleration

  def get_position(self, angle, velocity, acceleration, delta_time):
    position = Vector2(self.pos.x, self.pos.y)

    position.x = self.pos.x + velocity.x * delta_time
    position.y = self.pos.y + velocity.y * delta_time + 0.5 * acceleration.y * (delta_time ** 2)

    return position

  def calculate_trajectory(self, fixed_delta_time, screen_width, screen_height):
    self.print_current_parameters()

    self.trajectory = []

    position = Vector2(self.pos.x, self.pos.y)

    angle_rads = math.radians(self.angle)

    velocity = Vector2(self.launch_speed * math.cos(angle_rads), self.launch_speed * math.sin(angle_rads))

    constant_acceleration = self.get_constant_acceleration()

    delta_time = 0

    while (position.y >= self.pos.y and position.y < screen_height and position.x < screen_width and position.x > 0):
      viscosity_acc = self.get_viscocity_acceleration(velocity)
      total_acceleration = constant_acceleration - viscosity_acc

      position.x += velocity.x * fixed_delta_time
      position.y += velocity.y * fixed_delta_time

      if position.y > self.max_height:
        self.max_height = position.y

      self.trajectory.append(Vector2(position.x, position.y))

      velocity.x += total_acceleration.x * fixed_delta_time
      velocity.y += total_acceleration.y * fixed_delta_time

      delta_time += fixed_delta_time

  def print_current_parameters(self):
    print("══════════════════════")
    print("Parameters")
    print("══════════════════════")
    print("Velocity: " + str(self.launch_speed))
    print("Angle: " + str(self.angle))
    print("Mass: " + str(self.mass))
    print("Gravity: " + str(self.gravity * -1))
    print("Viscosity: " + str(self.viscosity))
    print("# of extra forces: " + str(len(self.forces)))

  def print_forces(self):
    forces_count = len(self.forces)

    if forces_count == 0:
      print("No forces to show.")
      return

    for i in range(0, forces_count):
      print(str(i) + ". (" + str(self.forces[i].x) + ", " + str(self.forces[i].y) + ")")


  def display(self, screen):
    screen_size = screen.get_size()
    factor = 1

    # Finds an appropriate scale factor
    for i in range(10, 0, -1):
      if self.trajectory[-1].x * i <= screen_size[0] and self.max_height * i <= screen_size[1]:
        factor = i
        break

    for point in self.trajectory:
      pos = (round(point.x * factor), round(screen_size[1] - point.y * factor))

      pygame.draw.circle(screen, self.trajectory_color, pos, self.radius)
