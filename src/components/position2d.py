import component
import world

class Position2D(component.Component):
  def __init__(self):
    pass

  def got_added(self, entity):
    entity.add_attribute("x", 0)
    entity.add_attribute("y", 0)
    entity.add_handler("moved", self.moved_handler)
    world.positions[(0, 0)].append(entity)
  
  def got_removed(self, entity):
    x = entity.attribute("x")
    y = entity.attribute("y")
    entity.remove_attribute("x")
    entity.remove_attribute("y")
    world.positions[(x, y)].remove(entity)

  def moved_handler(self, entity, parameters):
    prev_x = parameters["previous_x"]
    prev_y = parameters["previous_y"]
    world.positions[(prev_x, prev_y)].remove(entity)
    new_x = parameters["new_x"]
    new_y = parameters["new_y"]
    entity.update_attribute("x", new_x)
    entity.update_attribute("y", new_y)
    world.positions[(new_x, new_y)].append(entity)
    
