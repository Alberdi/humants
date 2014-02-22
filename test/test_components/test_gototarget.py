import unittest

import components.gototarget
import components.position
import entity
import world

class TestGoToTarget(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.go_to_target = components.gototarget.GoToTarget(max_tries=25)
    self.e.add_component(self.go_to_target)
    self.e.add_attribute("can_move")

  def tearDown(self):
    world.reset()

  def allow_move(self, e):
    e.update_attribute("can_move", True)
    e.message("can_move")

  def place_block(self, position):
      block = entity.Entity()
      pos = components.position.Position(dimensions=len(position))
      block.add_component(pos)
      block.add_attribute("blocks_movement")
      block.message("moved", {"new_position": position})

  def place_blocks_around(self, position):
    pos = components.position.Position(dimensions=len(position))
    for n in self.go_to_target.get_neighbours(position):
      self.place_block(n)

  """ 1 dimensions """
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
    self.place_blocks_around((0,))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,))

  def test_unreachable_open1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    self.place_block((3,))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,))

  def test_adapt_path_midway1d(self):
    self.e.add_component(components.position.Position(dimensions=1))
    self.e.add_attribute("target", (5,))
    self.allow_move(self.e)
    self.place_blocks_around((1,))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,))

  """ 2 dimensions """
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
    self.place_blocks_around((0,0))
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_unreachable_open2d(self):
    self.e.add_component(components.position.Position(dimensions=2))
    self.e.add_attribute("target", (5,8))
    self.place_blocks_around((5,8))
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
      self.place_block((1,i))
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
      self.place_block((position[0]+1, position[1]+i))
    for i in range(2):
      self.allow_move(self.e)
    self.assertNotEqual(self.e.attribute("position"), (3,0))
    self.allow_move(self.e)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (3,0))

  """ N dimensions """
  def test_move_adjacentNd(self):
    self.e.add_component(components.position.Position(dimensions=4))
    target = (0,)*3 + (1,)
    self.e.add_attribute("target", target)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), target)

  def test_move_diagonalNd(self):
    self.e.add_component(components.position.Position(dimensions=4))
    self.e.add_attribute("target", (1,)*4)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (1,)*4)

  def test_move_multipleNd(self):
    self.e.add_component(components.position.Position(dimensions=3))
    self.e.add_attribute("target", (5,)*3)
    for i in range(5):
      self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (5,)*3)
  
  def test_move_deniedNd(self):
    self.e.add_component(components.position.Position(dimensions=5))
    self.e.add_attribute("target", (9,)*5)
    self.place_blocks_around((0,)*5)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,)*5)

  def test_unreachable_openNd(self):
    self.e.add_component(components.position.Position(dimensions=3))
    self.e.add_attribute("target", (4,)*3)
    self.place_blocks_around((4,)*3)
    self.allow_move(self.e)
    self.assertEqual(self.e.attribute("position"), (0,)*3)

  def test_adapt_path_midwayNd(self):
    self.e.add_component(components.position.Position(dimensions=4))
    self.e.add_attribute("target", (3,)*4)
    self.allow_move(self.e)
    self.place_blocks_around((3,)*4)
    self.allow_move(self.e)
    self.allow_move(self.e)
    self.assertNotEqual(self.e.attribute("position"), (3,)*4)
    self.assertEqual(self.e.attribute("position"), (1,)*4)

if __name__ == "__main__":
  unittest.main()
