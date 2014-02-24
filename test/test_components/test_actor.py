import unittest

import components.actor
import entity

class TestActor(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.actor.Actor())

  def test_can_act_attribute(self):
    self.assertFalse(self.e.attribute("can_act"))
    self.e.update()
    self.e.update()
    self.assertFalse(self.e.attribute("can_act"))
    self.e.update()
    self.assertTrue(self.e.attribute("can_act"))

  def test_can_act_handler(self):
    self.e.add_handler("can_act", lambda e,p: e.add_attribute("test"))
    self.e.update()
    self.e.update()
    self.assertIsNone(self.e.attribute("test"))
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

  def test_can_act_cant_accumulate(self):
    for i in range(4):
      self.e.update()
    self.e.update_attribute("can_act", False)
    self.e.add_handler("can_act", lambda e,p: e.add_attribute("test"))
    self.e.update()
    self.assertFalse(self.e.attribute("test"))
    self.e.update()
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

if __name__ == "__main__":
  unittest.main()
