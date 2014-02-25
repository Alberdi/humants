import unittest

import components.carrier
import components.position
import entity
import world

class TestCarrier(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.carrier.Carrier())
    self.carriable = entity.Entity()
    self.carriable.add_attribute("carriable")

  def test_gripped(self):
    self.e.message("gripped", {"gripped": self.carriable})
    self.assertIn(self.carriable, self.e.attribute("carries"))
    self.assertEqual(self.carriable.attribute("carried_by"), self.e)

  def test_gripped_uncarriable(self):
    self.carriable.remove_attribute("carriable")
    self.e.message("gripped", {"gripped": self.carriable})
    self.assertNotIn(self.carriable, self.e.attribute("carries"))
    self.assertIsNone(self.carriable.attribute("carried_by"))

  def test_gripped_position(self):
    self.carriable.add_component(components.position.Position())
    self.e.message("gripped", {"gripped": self.carriable})
    self.assertNotIn(self.carriable, world.positions[(0,0)])

  def test_gripped_position_uncarriable(self):
    self.carriable.remove_attribute("carriable")
    self.carriable.add_component(components.position.Position())
    self.e.message("gripped", {"gripped": self.carriable})
    self.assertIn(self.carriable, world.positions[(0,0)])

  def test_released(self):
    self.e.message("gripped", {"gripped": self.carriable})
    self.e.message("released", {"released": self.carriable})

  def test_released_position(self):
    self.carriable.add_component(components.position.Position())
    self.e.message("gripped", {"gripped": self.carriable})
    self.e.add_attribute("position", (3,3))
    self.e.message("released", {"released": self.carriable})
    self.assertIn(self.carriable, world.positions[(3,3)])

  def test_released_position_not_carried(self):
    self.carriable.add_component(components.position.Position())
    self.e.add_attribute("position", (3,3))
    self.e.message("released", {"released": self.carriable})
    self.assertIn(self.carriable, world.positions[(0,0)])

if __name__ == "__main__":
  unittest.main()
