import operator

import component
import world

class Sleeper(component.Component):
  DEFAULT_CONFORT = 2
  def __init__(self):
    self.attributes = [("sleepiness", 0), ("max_sleepiness", 4000),
                       ("sleep_deprived", False), ("sleeping", False)]
    self.handlers = [("sleeping", self.sleeping_handler),
                     ("update", self.update_handler),
                     ("woke_up", self.woke_up_handler)]

  def sleeping_handler(self, e, p):
    room = world.positions[e.attribute("position")]
    confort = Sleeper.DEFAULT_CONFORT
    for entity in room:
      if entity.attribute("sleep_confort") > confort:
        confort = entity.attribute("sleep_confort")
    e.update_attribute("sleepiness", confort, operator.sub)
    if e.attribute("sleepiness") <= 0:
      e.update_attribute("sleepiness", 0)
      e.message("woke_up")
    else:
      ratio = e.attribute("sleepiness")*4/e.attribute("max_sleepiness")
      if ratio < 3:
        e.update_attribute("sleep_deprived", False)

  def update_handler(self, e, p):
    if e.attribute("sleeping"):
      e.message("sleeping")
      return
    ratio_before = e.attribute("sleepiness")*4/e.attribute("max_sleepiness")
    e.update_attribute("sleepiness", 1, operator.add)
    ratio_after = e.attribute("sleepiness")*4/e.attribute("max_sleepiness")
    if ratio_after > ratio_before:
      if ratio_after == 3:
        # Entity needs to sleep.
        e.update_attribute("sleep_deprived", True)
        e.message("sleep_deprived")
      elif ratio_after == 4:
        e.message("died", {"reason": "sleep_deprivation"})

  def woke_up_handler(self, e, p):
    e.update_attribute("sleeping", False)
