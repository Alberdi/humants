import unittest

import components.mortal
import component
import entity

class TestMortal(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.mortal.Mortal())
    c = component.Component()
    c.attributes = [("test", True)]
    c.handlers = [("handler", lambda e,p: e.add_attribute("handled"))]
    self.e.add_component(c)

  def test_died_handler(self):
    self.e.message("died")
    self.assertIsNone(self.e.attribute("test"))
    self.e.message("handler")
    self.assertIsNone(self.e.attribute("handled"))

if __name__ == "__main__":
  unittest.main()
