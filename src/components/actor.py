import operator

import component

class Actor(component.Component):
  def __init__(self):
    atts = [("next_action", 100), ("speed", 50), ("can_act", False)]
    self.attributes = atts;
    self.handlers = [("update", self.update_handler)]

  def update_handler(self, e, p):
    if e.attribute("next_action") <= 0:
      if not e.attribute("can_act"):
        e.update_attribute("can_act", True)
        e.message("can_act")
        e.update_attribute("next_action", 100)
    else:
      e.update_attribute("next_action", e.attribute("speed"), operator.sub)
