import unittest

import components.position
import entity
import world

class TestPosition(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.pos = components.position.Position()

  def test_got_added(self):
    self.assertTrue(self.e.add_component(self.pos))
    self.assertIsNotNone(self.e.attribute("position"))
    self.assertIn(self.e, world.positions[self.e.attribute("position")])

  def test_got_removed(self):
    self.e.add_component(self.pos)
    self.e.remove_component(self.pos)
    self.assertIsNone(self.e.attribute("position"))
    self.assertNotIn(self.e, world.positions[self.e.attribute("position")])

  def test_moved(self):
    self.e.add_component(self.pos)
    self.e.message("moved", {"new_position": (4,5)})
    self.assertEqual(self.e.attribute("position"), (4,5))
    self.assertIn(self.e, world.positions[(4, 5)])
    self.assertNotIn(self.e, world.positions[(0, 0)])

if __name__ == "__main__":
  unittest.main()
