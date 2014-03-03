import operator

import component
import entityfactory
import world

class Lumberjack(component.Component):
  def __init__(self):
    self.attributes = []
    self.handlers = [("can_act", self.can_act_handler),
                     ("killed", self.killed_handler),
                     ("update", self.update_handler)]
    self.trees = self.get_trees()

  def can_act_handler(self, e, p):
    if not e.attribute("can_act"):
      return
    if e.attribute("target") == e.attribute("position"):
      if e.attribute("position") == e.attribute("home"):
        if e.attribute("carries"):
          e.message("released", {"released": e.attribute("carries")[0]})
          e.update_attribute("can_act", False)
        self.get_new_target(e)
      else:
        for tree in world.positions[e.attribute("position")]:
          if self.is_valid_tree(tree):
            tree.message("wounded", {"wounder": e})
            e.update_attribute("can_act", False)
            return
        e.remove_attribute("target")
        self.update_handler(e, p)

  def distance(self, origin, target):
   return abs(reduce(lambda a,b: max(abs(a), abs(b)),
                     map(operator.sub, origin, target)))

  def get_closer_canteen(self, e):
    canteens = filter(lambda e: e.attribute("type") == "canteen",
                      world.entities)
    if canteens:
      d = [(self.distance(e.attribute("position"), x.attribute("position")), x)
           for x in canteens]
      return min(d)[1]
    return None

  def get_closer_tree(self, e):
    if not self.trees:
      self.trees = self.get_trees()
    d = [(self.distance(e.attribute("position"), x.attribute("position")), x)
         for x in self.trees]
    d.sort()
    for h,t in d:
      if self.is_valid_tree(t):
        self.trees.remove(t)
        return t
    return None
 
  def get_new_target(self, e):
    if e.attribute("hungry"):
      c = self.get_closer_canteen(e)
      if c:
        e.update_attribute("target", c.attribute("position"))
        return
    if filter(lambda l: l.attribute("type") == "log", e.attribute("carries")):
      e.update_attribute("target", e.attribute("home"))
    else:
      t = self.get_closer_tree(e)
      if t:
        e.update_attribute("target", t.attribute("position"))
     
  def get_trees(self):
    return filter(lambda e: self.is_valid_tree(e), world.entities)
 
  def getting_hungry_handler(self, e, p):
    e.add_attribute("hungry")

  def is_valid_tree(self, t):
    return t.attribute("type") == "tree"

  def killed_handler(self, e, p):
    if self.is_valid_tree(p["killed"]):
      if e.attribute("carries") is not None:
        e.attribute("carries").append(entityfactory.log())

  def update_handler(self, e, p):
    if e.attribute("can_act"):
      self.get_new_target(e)
      e.message("can_act")

