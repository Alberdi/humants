import operator

import component

class Woundable(component.Component):
  def __init__(self, max_wounds=10):
    self.attributes = [("healable", True), ("woundable", True),
                       ("wounds", 0), ("max_wounds", max_wounds)]
    self.handlers = [("healed", self.healed_handler),
                     ("wounded", self.wounded_handler)]

  def healed_handler(self, e, p):
    if e.attribute("healable"):
      amount = p["amount"] if "amount" in p else 1
      e.update_attribute("wounds", amount, lambda x,y: max(x-y, 0))
      if e.attribute("wounds") == e.attribute("max_wounds")-1:
        e.message("revived", {"reason": "heal"})

  def wounded_handler(self, e, p):
    if e.attribute("woundable"):
      amount = p["amount"] if "amount" in p else 1
      e.update_attribute("wounds", amount, operator.add)
      if e.attribute("wounds") >=  e.attribute("max_wounds"):
        e.message("died", {"reason": "wounds"})

