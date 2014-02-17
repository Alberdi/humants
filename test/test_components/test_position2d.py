import unittest

import components.position2d
import entity
import world

class TestPosition2D(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.pos = components.position2d.Position2D()

  def test_got_added(self):
    self.assertTrue(self.e.add_component(self.pos))
    x = self.e.attribute("x")
    y = self.e.attribute("y")
    self.assertIsNotNone(x)
    self.assertIsNotNone(y)
    self.assertIn(self.e, world.positions[(x, y)])

  def test_got_removed(self):
    self.e.add_component(self.pos)
    x = self.e.attribute("x")
    y = self.e.attribute("y")
    self.e.remove_component(self.pos)
    self.assertIsNone(self.e.attribute("x"))
    self.assertIsNone(self.e.attribute("y"))
    self.assertNotIn(self.e, world.positions[(x, y)])

  def test_moved(self):
    self.e.add_component(self.pos)
    parameters = {"new_x": 4, "new_y": 5}
    prev_x = parameters["previous_x"] = self.e.attribute("x")
    prev_y = parameters["previous_y"] = self.e.attribute("y")
    self.e.message("moved", parameters)
    self.assertEqual(self.e.attribute("x"), 4)
    self.assertEqual(self.e.attribute("y"), 5)
    self.assertIn(self.e, world.positions[(4, 5)])
    self.assertNotIn(self.e, world.positions[(prev_x, prev_y)])

if __name__ == "__main__":
  unittest.main()
