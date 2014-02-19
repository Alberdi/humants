import component
import world

class Position(component.Component):
  def __init__(self, dimensions=2):
    self.attributes = [("position", (0,)*dimensions)]
    self.handlers = [("moved", self.moved_handler)]

  def got_added(self, e):
    super(Position, self).got_added(e)
    world.positions[e.attribute("position")].append(e)
  
  def got_removed(self, e):
    world.positions[e.attribute("position")].remove(e)
    super(Position, self).got_removed(e)
 
  def moved_handler(self, e, p):
    world.positions[e.attribute("position")].remove(e)
    e.update_attribute("position", p["new_position"])
    world.positions[p["new_position"]].append(e)
    
