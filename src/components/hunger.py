import operator

import component

class Hunger(component.Component):
  def __init__(self):
    self.attributes = [("hunger", 0), ("max_hunger", 1000)]
    self.handlers = [("update", self.update_handler)]

  def update_handler(self, e, p):
    ratio_before = e.attribute("hunger")*4/e.attribute("max_hunger")
    e.update_attribute("hunger", 1, operator.add)
    ratio_after = e.attribute("hunger")*4/e.attribute("max_hunger")
    if ratio_after > ratio_before:
      if ratio_after == 2:
        e.message("getting_hungry")
      elif ratio_after == 3:
        # Entity needs food badly
        e.message("starving")
      elif ratio_after == 4:
        e.message("died", {"reason": "hunger"})

