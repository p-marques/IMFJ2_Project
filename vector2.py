class Vector2:

  def __init__(self, x = 0, y = 0):
    self.x = x
    self.y = y

  def to_tuple(self):
    return (self.x, self.y)

  def __add__(self, delta):
    if not isinstance(delta, Vector2):
      raise TypeError("Can only sum Vector2 with another Vector2!")

    return Vector2(self.x + delta.x, self.y + delta.y)

  def __sub__(self, delta):
    if not isinstance(delta, Vector2):
      raise TypeError("Can only subtract Vector2 with another Vector2!")

    return Vector2(self.x - delta.x, self.y - delta.y)

  def __truediv__(self, value):
    if not isinstance(value, int) and not isinstance(value, float):
      raise TypeError("Can only divide Vector2 with integer or float!")

    return Vector2(self.x / value, self.y / value)

  def __str__(self):
    return str(self.x) + ', ' + str(self.y)