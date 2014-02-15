from collections import defaultdict

class Entity:
  def __init__(self):
    self.attributes = defaultdict(lambda: None)

  """ Attributes """
  def attribute(self, attribute):
    return self.attributes[attribute]

  def add_attribute(self, attribute, value=True):
    self.attributes[attribute] = value
    return True

  def remove_attribute(self, attribute):
    if attribute in self.attributes:
      del self.attributes[attribute]
      return True
    return False
