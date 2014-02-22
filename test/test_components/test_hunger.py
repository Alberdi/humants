import unittest

import components.hunger
import entity

class TestHunger(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.hunger.Hunger())
    self.e.update_attribute("max_hunger", 10)
    self.food = entity.Entity()
    self.food.add_attribute("calories", 2)

  def test_eat(self):
    for i in range(3):
      self.e.update()
    self.e.message("eat", {"eaten_entity": self.food})
    self.assertEqual(self.e.attribute("hunger"), 1)

  def test_eat_positive(self):
    self.e.update()
    self.assertNotEqual(self.e.attribute("hunger"), 0)
    self.e.message("eat", {"eaten_entity": self.food})
    self.assertEqual(self.e.attribute("hunger"), 0)

  def test_getting_hungry_handler(self):
    self.e.add_handler("getting_hungry", lambda e,p: e.add_attribute("test"))
    for i in range(4):
      self.e.update()
    self.assertIsNone(self.e.attribute("test"))
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

  def test_starving_handler(self):
    self.e.add_handler("starving", lambda e,p: e.add_attribute("test"))
    for i in range(7):
      self.e.update()
    self.assertIsNone(self.e.attribute("test"))
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

  def test_died_handler(self):
    self.e.add_handler("died", lambda e,p:
                                      e.add_attribute("died_"+p["reason"]))
    for i in range(9):
      self.e.update()
    self.assertIsNone(self.e.attribute("died_hunger"))
    self.e.update()
    self.assertTrue(self.e.attribute("died_hunger"))

if __name__ == "__main__":
  unittest.main()
