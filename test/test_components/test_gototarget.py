import unittest

import components.gototarget
import components.position
import entity
import world

class TestGoToTarget(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.gototarget.GoToTarget(max_tries=50))
    self.e.add_attribute("can_move")

  def tearDown(self):
    world.reset()

  def allow_move(self, e):
    e.update_attribute("can_move", True)
    e.message("can_move")

  def put_block(self, position, dimensions=2):
    block = entity.Entity()
    block.add_component(components.position.Position(dimensions=dimensions))
    block.add_attribute("blocks_movement")
    block.message("moved", {"new_position": position})

  def test_move_adjacent1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (1,))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,))

  def test_move_multiple1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    for i in range(5):
      self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (5,))
  
  def test_move_denied1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    self.put_block((-1,), 1)
    self.put_block((1,), 1)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,))

  def test_unreachable_open1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    self.put_block((3,), 1)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,))

  def test_adapt_path_midway1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    self.allow_move(self.e)
    self.put_block((0,), 1)
    self.put_block((2,), 1)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,))

  def test_move_adjacent2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (1,0))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,0))

  def test_move_diagonal2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (1,1))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,1))

  def test_move_multiple2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (5,8))
    for i in range(8):
      self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (5,8))
  
  def test_move_denied2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (5,8))
    for a in range(-1,2):
      for b in range(-1,2):
        self.put_block((a,b), 2)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_unreachable_open2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (5,8))
    for a in range(-1,2):
      for b in range(-1,2):
        self.put_block((5+a,8+b), 2)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_move_around2d(self):
    #.....
    #..x..
    #.exg. 4 movements needed to get to g
    #..x..
    #.....
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (2,0))
    for i in range(-1,2):
      self.put_block((1,i), 2)
    for i in range(3):
      self.allow_move(self.e)
    self.assertNotEqual(self.e.attribute("position"), (2,0))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (2,0))

  def test_adapt_path_midway2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (3,0))
    self.allow_move(self.e)
    position = self.e.attribute("position")
    for i in range(-1,2):
      self.put_block((position[0]+1, position[1]+i), 2)
    for i in range(2):
      self.allow_move(self.e)
    self.assertNotEqual(self.e.attribute("position"), (3,0))
    self.allow_move(self.e)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (3,0))

if __name__ == "__main__":
  unittest.main()
