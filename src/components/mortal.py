import operator

import component
import world

class Mortal(component.Component):
  def __init__(self):
    self.attributes = [("mortal", True)]
    self.handlers = [("died", self.died_handler)]

  def died_handler(self, e, p):
    if e.attribute("mortal"):
      e.add_attribute("dead")
      # This is actually a bit scary, it might have unexpected consecuences.
      # Maybe they don't matter that much because the entity is dead.
      for c in e.components[:]:
        e.remove_component(c)

