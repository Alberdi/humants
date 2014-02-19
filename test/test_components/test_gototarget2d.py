import unittest

import components.gototarget2d
import components.position2d
import entity
import world

class TestGoToTarget2D(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.position2d.Position2D())
    self.e.add_component(components.gototarget2d.GoToTarget2D())
    self.e.add_attribute("can_move")

  def tearDown(self):
    world.reset()

  def allow_move(self, e):
    e.update_attribute("can_move", True)
    e.message("can_move")

  def put_block(self, position):
    block = entity.Entity()
    block.add_component(components.position2d.Position2D())
    block.add_attribute("blocks_movement")
    block.message("moved", {"new_x": position[0], "new_y": position[1]})

  def test_move_adjacent(self):
    self.e.add_attribute("target", (1,0))
    self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (1,0))

  def test_move_diagonal(self):
    self.e.add_attribute("target", (1,1))
    self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (1,1))

  def test_move_multiple(self):
    self.e.add_attribute("target", (5,8))
    for i in range(8):
      self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (5,8))
  
  def test_move_denied(self):
    self.e.add_attribute("target", (5,8))
    for a in range(-1,2):
      for b in range(-1,2):
        self.put_block((a,b))
    self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (0,0))

  def test_move_around(self):
    #.....
    #..x..
    #.exg. 4 movements needed to get to g
    #..x..
    #.....
    self.e.add_attribute("target", (2,0))
    for i in range(-1,2):
      self.put_block((1,i))
    for i in range(3):
      self.allow_move(self.e)
    self.assertNotEqual((self.e.attribute("x"), self.e.attribute("y")), (2,0))
    self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (2,0))

  def test_adapt_path_midway(self):
    self.e.add_attribute("target", (3,0))
    self.allow_move(self.e)
    for i in range(-1,2):
      self.put_block((self.e.attribute("x")+1, self.e.attribute("y")+i))
    for i in range(2):
      self.allow_move(self.e)
    self.assertNotEqual((self.e.attribute("x"), self.e.attribute("y")), (3,0))
    self.allow_move(self.e)
    self.allow_move(self.e)
    self.assertEqual((self.e.attribute("x"), self.e.attribute("y")), (3,0))

if __name__ == "__main__":
  unittest.main()
