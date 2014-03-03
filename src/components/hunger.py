import operator

import component

class Hunger(component.Component):
  def __init__(self):
    self.attributes = [("hunger", 0), ("max_hunger", 1000),
                       ("hungry", False), ("starving", False)]
    self.handlers = [("ate", self.ate_handler),
                     ("update", self.update_handler)]

  def ate_handler(self, e, p):
    calories = p["eaten_entity"].attribute("calories")
    if calories:
      e.update_attribute("hunger", calories, lambda a,b: max(a-b, 0))
      ratio = e.attribute("hunger")*4/e.attribute("max_hunger")
      if ratio < 3:
        e.update_attribute("starving", False)
        if ratio < 2:
          e.update_attribute("hungry", False)

  def update_handler(self, e, p):
    ratio_before = e.attribute("hunger")*4/e.attribute("max_hunger")
    e.update_attribute("hunger", 1, operator.add)
    ratio_after = e.attribute("hunger")*4/e.attribute("max_hunger")
    if ratio_after > ratio_before:
      if ratio_after == 2:
        e.update_attribute("hungry", True)
        e.message("getting_hungry")
      elif ratio_after == 3:
        # Entity needs food badly
        e.update_attribute("starving", True)
        e.message("starving")
      elif ratio_after == 4:
        e.message("died", {"reason": "hunger"})

