import unittest

import component
import entity

class TestComponent(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.c = component.Component()

  def test_got_added(self):
    self.c.attributes = [("test", True)]
    self.e.add_component(self.c)
    self.assertTrue(self.e.attribute("test"))

  def test_got_added_multiple(self):
    self.c.attributes = [("t1", True), ("t2", True)]
    self.e.add_component(self.c)
    self.assertTrue(self.e.attribute("t1"))
    self.assertTrue(self.e.attribute("t2"))

  def test_got_removed(self):
    self.c.attributes = [("test", True)]
    self.e.add_component(self.c)
    self.e.remove_component(self.c)
    self.assertIsNone(self.e.attribute("test"))

  def test_got_removed_multiple(self):
    self.c.attributes = [("t1", True), ("t2", True)]
    self.e.add_component(self.c)
    self.e.remove_component(self.c)
    self.assertIsNone(self.e.attribute("t1"))
    self.assertIsNone(self.e.attribute("t2"))

  def test_handler(self):
    self.c.handlers = [("test", lambda e,p: e.add_attribute("t"))]
    self.e.add_component(self.c)
    self.assertIsNone(self.e.attribute("t"))
    self.e.message("test")
    self.assertTrue(self.e.attribute("t"))

  def test_handler_multiple(self):
    self.c.handlers.append(("test1", lambda e,p: e.add_attribute("t1")))
    self.c.handlers.append(("test2", lambda e,p: e.add_attribute("t2")))
    self.e.add_component(self.c)
    self.e.message("test1")
    self.e.message("test2")
    self.assertTrue(self.e.attribute("t1"))
    self.assertTrue(self.e.attribute("t2"))

  def test_handler_removed(self):
    self.c.handlers = [("test", lambda e,p: e.add_attribute("t"))]
    self.e.add_component(self.c)
    self.e.remove_component(self.c)
    self.e.message("test")
    self.assertIsNone(self.e.attribute("t"))

if __name__ == '__main__':
  unittest.main()
