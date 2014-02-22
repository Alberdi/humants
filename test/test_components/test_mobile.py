import unittest

import components.mobile
import entity

class TestMobile(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.mobile.Mobile())

  def test_can_move_attribute(self):
    self.assertFalse(self.e.attribute("can_move"))
    self.e.update()
    self.e.update()
    self.assertFalse(self.e.attribute("can_move"))
    self.e.update()
    self.assertTrue(self.e.attribute("can_move"))

  def test_can_move_handler(self):
    self.e.add_handler("can_move", lambda e,p: e.add_attribute("test"))
    self.e.update()
    self.e.update()
    self.assertIsNone(self.e.attribute("test"))
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

  def test_can_move_cant_accumulate(self):
    for i in range(4):
      self.e.update()
    self.e.update_attribute("can_move", False)
    self.e.add_handler("can_move", lambda e,p: e.add_attribute("test"))
    self.e.update()
    self.assertFalse(self.e.attribute("test"))
    self.e.update()
    self.e.update()
    self.assertTrue(self.e.attribute("test"))

if __name__ == "__main__":
  unittest.main()
