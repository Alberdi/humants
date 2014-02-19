import component
import world

class GoToTarget2D(component.Component):
  def __init__(self):
    self.attributes = [("path_to_target", [])]
    self.handlers = [("can_move", self.can_move_handler)]

  def can_move_handler(self, e, p):
    if (not e.attribute("can_move") or not e.attribute("target") or
        e.attribute("target") == (e.attribute("x"), e.attribute("y"))):
      return
    path = e.attribute("path_to_target")
    if path and self.is_passable(path[0]):
      e.update_attribute("can_move", False)
      e.message("moved", {"new_x": path[0][0], "new_y": path[0][1]})
      path.pop(0)
    elif self.get_new_path(e):
      print e.attribute("path_to_target")
      self.can_move_handler(e, p) 

  def is_passable(self, pos):
    for e in world.positions[pos]:
      if e.attribute("blocks_movement"):
        return False
    return True

  def get_new_path(self, e):
    # Using the A* algorithm
    came_from = {}
    closedset = []
    openset = [(e.attribute("x"), e.attribute("y"))]
    g_score = {openset[0]: 0}
    f_score = {openset[0]: self.heuristic(openset[0], e.attribute("target"))}
    while openset:
      best = min([(f_score[x], x)
                 for x in filter(lambda y: y in openset, f_score)])[1]
      if best == e.attribute("target"):
        e.update_attribute("path_to_target",
                           self.reconstruct_path(best, came_from))
        return True
      openset.remove(best)
      closedset.append(best)
      for n in filter(lambda y: y not in closedset, self.get_neighbours(best)):
        if n not in openset or g_score[best] + 1 < g_score[n]:
          came_from[n] = best
          g_score[n] = g_score[best] + 1
          f_score[n] = g_score[n] + self.heuristic(n, e.attribute("target"))
          if n not in openset:
            openset.append(n)
    return False

  def get_neighbours(self, position):
    return filter(lambda p: p != position and self.is_passable(p),
                 [(position[0]+a, position[1]+b)
                 for a in range(-1,2) for b in range(-1,2)])

  def heuristic(self, origin, target):
    return max(abs(target[0]-origin[0]), abs(target[1]-origin[1]))

  def reconstruct_path(self, position, came_from):
    p = []
    if position in came_from:
      p = self.reconstruct_path(came_from[position], came_from)
      p.append(position)
    return p
