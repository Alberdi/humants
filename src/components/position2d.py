import component
import world

class Position2D(component.Component):
  def __init__(self):
    pass

  def got_added(self, e):
    world.positions[(0, 0)].append(e)
    e.add_attribute("x", 0)
    e.add_attribute("y", 0)
    e.add_handler("moved", self.moved_handler)
  
  def got_removed(self, e):
    world.positions[(e.attribute("x"), e.attribute("y"))].remove(e)
    e.remove_attribute("x")
    e.remove_attribute("y")
    e.remove_handler("moved", self.moved_handler)

  def moved_handler(self, e, p):
    world.positions[(p["previous_x"], p["previous_y"])].remove(e)
    e.update_attribute("x", p["new_x"])
    e.update_attribute("y", p["new_y"])
    world.positions[(p["new_x"], p["new_y"])].append(e)
    
