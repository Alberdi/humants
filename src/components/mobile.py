import operator

import component

class Mobile(component.Component):
  def __init__(self):
    atts = [("next_movement", 100), ("speed", 50), ("can_move", False)]
    self.attributes = atts;
    self.handlers = [("update", self.update_handler)]

  def update_handler(self, e, p):
    if e.attribute("next_movement") <= 0:
      if not e.attribute("can_move"):
        e.message("can_move")
        e.update_attribute("can_move", True)
        e.update_attribute("next_movement", 100)
    else:
      e.update_attribute("next_movement", e.attribute("speed"), operator.sub)
