class Component(object):
  def __init__(self):
    self.attributes = []
    self.handlers = []

  def got_added(self, e):
    for k,v in self.attributes:
      e.add_attribute(k, v)
    for k,v in self.handlers:
      e.add_handler(k, v)

  def got_removed(self, e):
    for k,v in self.attributes:
      e.remove_attribute(k)
    for k,v in self.handlers:
      e.remove_handler(k, v)

