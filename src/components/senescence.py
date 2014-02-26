import operator

import component

# From Latin: senescere, meaning "to grow old".
class Senescence(component.Component):
  def __init__(self):
    self.age_etapes = {1: "young", 1500: "adult", 6000: "old", 8000: "dead"}
    self.attributes = [("age", 0), ("age_etape", "newborn")]
    self.handlers = [("update", self.update_handler)]

  def update_handler(self, e, p):
    e.update_attribute("age", 1, operator.add)
    if e.attribute("age") in self.age_etapes:
      new_etape = self.age_etapes[e.attribute("age")]
      e.update_attribute("age_etape", new_etape)
      if new_etape == "dead":
        e.message("died", {"reason": "senescence"})
      else:  
        e.message("grown", {"new_etape": new_etape})

