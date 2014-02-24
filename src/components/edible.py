import component

class Edible(component.Component):
  def __init__(self):
    self.attributes = [("edible", True), ("calories", 100)]
    self.handlers = [("got_eaten", self.got_eaten_handler)]

  def got_eaten_handler(self, e, p):
    e.message("died", {"reason": "got_eaten"})
