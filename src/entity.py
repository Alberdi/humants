from collections import defaultdict

class Entity:
  def __init__(self):
    self.attributes = defaultdict(lambda: None)
    self.message_handlers = defaultdict(list)
    self.components = []

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

  """ Components """
  def add_component(self, component):
    self.components.append(component)
    component.got_added(self)
    return True

  def remove_component(self, component):
    if component in self.components:
      self.components.remove(component)      
      component.got_removed(self)
      return True
    return False

  def update(self):
    for component in self.components:
      component.update(self)

  """ Messages """
  def message(self, message, parameters=[]):
    for handler in self.message_handlers[message]:
      handler(self, parameters)

  def add_handler(self, message, function):
    self.message_handlers[message].append(function)
    return True

  def remove_handler(self, message, function=None):
    if message not in self.message_handlers:
      return False
    if function:
      self.message_handlers[message].remove(function)
    else:
      del self.message_handlers[message]
    return True
      
