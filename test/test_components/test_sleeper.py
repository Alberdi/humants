import unittest

import components.position
import components.sleeper
import entity
import entityfactory
import world

class TestSleeper(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.sleeper.Sleeper())
    self.e.add_component(components.position.Position())
    self.e.update_attribute("max_sleepiness", 10)

  def tearDown(self):
    world.reset()

  def test_sleeping(self):
    for i in range(3):
      self.e.update()
    self.e.message("sleeping")
    self.assertEqual(self.e.attribute("sleepiness"), 1)

  def test_sleeping_bed(self):
    entityfactory.bed()
    for i in range(5):
      self.e.update()
    self.e.message("sleeping")
    self.assertEqual(self.e.attribute("sleepiness"), 1)

  def test_sleepiness_positive(self):
    self.e.update()
    self.assertNotEqual(self.e.attribute("sleepiness"), 0)
    self.e.message("sleeping")
    self.assertEqual(self.e.attribute("sleepiness"), 0)

  def test_sleep_deprived_handler(self):
    self.e.add_handler("sleep_deprived", lambda e,p: e.add_attribute("test"))
    for i in range(7):
      self.e.update()
    self.assertIsNone(self.e.attribute("test"))
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

  def test_sleep_deprived(self):
    for i in range(7):
      self.e.update()
    self.assertFalse(self.e.attribute("sleep_deprived"))
    self.e.update()
    self.assertTrue(self.e.attribute("sleep_deprived"))

  def test_sleep_deprived_slept(self):
    for i in range(8):
      self.e.update()
    self.e.message("sleeping")
    self.assertFalse(self.e.attribute("sleep_deprived"))

  def test_sleep_deprived_slept_still(self):
    for i in range(10):
      self.e.update()
    self.e.message("sleeping")
    self.assertTrue(self.e.attribute("sleep_deprived"))
 
  def test_died_handler(self):
    self.e.add_handler("died", lambda e,p:
                                      e.add_attribute("died_"+p["reason"]))
    for i in range(9):
      self.e.update()
    self.assertIsNone(self.e.attribute("died_sleep_deprivation"))
    self.e.update()
    self.assertTrue(self.e.attribute("died_sleep_deprivation"))

if __name__ == "__main__":
  unittest.main()
