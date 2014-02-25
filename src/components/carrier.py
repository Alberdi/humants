import component
import world

class Carrier(component.Component):
  def __init__(self):
    self.attributes = [("carrier", True), ("carries", [])]
    self.handlers = [("gripped", self.gripped_handler),
                     ("released", self.released_handler)]

  def gripped_handler(self, e, p):
    gripped = p["gripped"]
    if e.attribute("carrier") and gripped.attribute("carriable"):
      e.update_attribute("carries", [gripped], lambda x,y: x+y)
      gripped.add_attribute("carried_by", e)
      if gripped.attribute("position"):
        world.positions[gripped.attribute("position")].remove(gripped)

  def released_handler(self, e, p):
    released = p["released"]
    if released in e.attribute("carries"):
      e.update_attribute("carries", released,
                         lambda x,y: [a for a in x if a != y])
      released.remove_attribute("carried_by")
      if e.attribute("position"):
        world.positions[e.attribute("position")].append(released)

