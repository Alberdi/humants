import component
import world

class Position2D(component.Component):
  def __init__(self):
    self.attributes = [("x",0), ("y",0)]
    self.handlers = [("moved", self.moved_handler)]

  def got_added(self, e):
    super(Position2D, self).got_added(e)
    world.positions[(0, 0)].append(e)
  
  def got_removed(self, e):
    world.positions[(e.attribute("x"), e.attribute("y"))].remove(e)
    super(Position2D, self).got_removed(e)
 
  def moved_handler(self, e, p):
    world.positions[(p["previous_x"], p["previous_y"])].remove(e)
    e.update_attribute("x", p["new_x"])
    e.update_attribute("y", p["new_y"])
    world.positions[(p["new_x"], p["new_y"])].append(e)
    
