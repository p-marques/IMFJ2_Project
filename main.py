import pygame
import time

from physical_object import Physical_Object
from vector2 import Vector2

def main():
  # Initialize pygame, with the default parameters
  pygame.init()

  # Define the size/resolution of our window
  res = (640, 480)

  # Create a window and a display surface
  screen = pygame.display.set_mode(res)

  # Fixed delta time
  fixed_delta_time = 0.02

  # Create object
  obj = Physical_Object(Vector2(20, 20), 55, 35)

  while (True):
    pygame.event.set_grab(True)

    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
        return

    screen.fill((255, 255, 255))

    obj.calculate_trajectory(fixed_delta_time, res[0], res[1])

    obj.display(screen)

    pygame.display.flip()

    pygame.event.set_grab(False)

    user_input = ""
    while user_input == "":
      user_input = input("> ")

      words = [s.strip().lower() for s in user_input.split()]
      words_count = len(words)

      if words_count == 0:
        continue

      try:
        if words[0] == "exit" or words[0] == "quit":
          return
        elif words[0] == "set":
          if words_count != 3:
            print("Incorrect format. It's \"set <parameter> <value>\"")
            user_input = ""
            continue

          value = float(words[2])
          if value <= 0:
              print("Error! Value must be bigger than 0.")
              user_input = ""
              continue

          if words[1] == "velocity":
            obj.set_launch_speed(value)
          elif words[1] == "angle":
            obj.set_angle(value)
          elif words[1] == "mass":
            obj.set_mass(value)
          elif words[1] == "gravity":
            obj.set_gravity(value)
          elif words[1] == "viscosity":
            obj.set_viscosity(value)
          else:
            print("Unknown command \"" + words[1] + "\"")
            user_input = ""
        elif words[0] == "forces":
          if words_count == 1:
            obj.print_forces()
            user_input = ""
          elif words[1] == "add":
            if words_count != 4:
              print("Incorrect format. It's \"forces add <x value> <y value>\"")
              user_input = ""
              continue

            value = Vector2(float(words[2]), float(words[3]))
            obj.add_force(value)

          elif words[1] == "remove":
            if words_count != 3:
              print("Incorrect format. It's \"forces remove <index>\"")
              user_input = ""
              continue

            value = int(words[2])

            if value >= len(obj.forces) or value < 0:
              print("Error! There is no force #" + words[2])
              user_input = ""
              continue

            obj.remove_force(value)
          else:
            print("Unknown command \"" + words[1] + "\"")
            user_input = ""

        else:
          print("Unknown command \"" + words[0] + "\"")
          user_input = ""
      except ValueError:
        print("Error! Please insert a number.")
        user_input = ""

# RUN
main()
