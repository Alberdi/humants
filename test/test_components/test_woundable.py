import unittest

import components.woundable
import entity

class TestWoundable(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.woundable.Woundable())

  def test_healed(self):
    self.e.update_attribute("wounds", 2)
    self.e.message("healed", {"healer": entity.Entity()})
    self.assertEqual(self.e.attribute("wounds"), 1)

  def test_healed_amount(self):
    self.e.update_attribute("wounds", 2)
    self.e.message("healed", {"healer": entity.Entity(), "amount": 3})
    self.assertEqual(self.e.attribute("wounds"), 0)

  def test_healed_unhealable(self):
    self.e.update_attribute("wounds", 2)
    self.e.update_attribute("healable", False)
    self.e.message("healed", {"healer": entity.Entity()})
    self.assertEqual(self.e.attribute("wounds"), 2)

  def test_revived_message(self):
    self.e.update_attribute("wounds", 10)
    self.e.add_handler("revived", lambda e,p: e.add_attribute("test"))
    self.e.message("healed", {"healer": entity.Entity()})
    self.assertTrue(self.e.attribute("test"))

  def test_wounded(self):
    self.e.message("wounded", {"attacker": entity.Entity()})
    self.assertEqual(self.e.attribute("wounds"), 1)

  def test_wounded_amount(self):
    self.e.message("wounded", {"attacker": entity.Entity(), "amount": 3})
    self.assertEqual(self.e.attribute("wounds"), 3)

  def test_wounded_unwoundable(self):
    self.e.update_attribute("woundable", False)
    self.e.message("wounded", {"attacker": entity.Entity()})
    self.assertEqual(self.e.attribute("wounds"), 0)

  def test_died_message(self):
    self.e.add_handler("died", lambda e,p: e.add_attribute("test"))
    self.e.update_attribute("max_wounds", 1)
    self.e.message("wounded", {"attacker": entity.Entity()})
    self.assertTrue(self.e.attribute("test"))

if __name__ == "__main__":
  unittest.main()
