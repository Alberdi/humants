import random
import unittest

import component
import entity

class TestEntityAttribute(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()

  def test_add_attribute(self):
    self.assertTrue(self.e.add_attribute("test"))

  def test_add_attribute_multiple(self):
    self.e.add_attribute("test1")
    self.assertTrue(self.e.add_attribute("test2"))

  def test_attribute(self):
    self.e.add_attribute("test")
    self.assertTrue(self.e.attribute("test"))

  def test_attribute_multiple(self):
    self.e.add_attribute("test1")
    self.e.add_attribute("test2")
    self.assertTrue(self.e.attribute("test1"))
    self.assertTrue(self.e.attribute("test2"))

  def test_not_attribute(self):
    self.assertIsNone(self.e.attribute("test"))

  def test_add_attribute_value(self):
    self.assertTrue(self.e.add_attribute("test", "value"))

  def test_add_attribute_value_int(self):
    self.assertTrue(self.e.add_attribute("test", 5))

  def test_attribute_value(self):
    self.e.add_attribute("test", "value")
    self.assertEquals(self.e.attribute("test"), "value")

  def test_attribute_value_int(self):
    self.e.add_attribute("test", 5)
    self.assertTrue(self.e.attribute("test"), 5)

  def test_remove_attribute(self):
    self.e.add_attribute("test")
    self.assertTrue(self.e.remove_attribute("test"))
    self.assertIsNone(self.e.attribute("test"))

  def test_remove_attribute_nonexistent(self):
    self.assertFalse(self.e.remove_attribute("test"))

class TestEntityMessage(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.test_function1 = lambda e,p: e.add_attribute("t1")
    self.test_function2 = lambda e,p: e.add_attribute("t2")
    self.test_function3 = lambda e,p: e.add_attribute(p[0])

  def test_add_handler(self):
    self.assertTrue(self.e.add_handler("test", self.test_function1))

  def test_add_handler_multiple(self):
    self.e.add_handler("test", self.test_function1)
    self.assertTrue(self.e.add_handler("test", self.test_function1))

  def test_message(self):
    self.e.add_handler("test", self.test_function1)
    self.e.message("test")
    self.assertTrue(self.e.attribute("t1"))

  def test_message_parameters(self):
    self.e.add_handler("test", self.test_function3)
    self.e.message("test", ["t3"])
    self.assertTrue(self.e.attribute("t3"))

  def test_message_multiple_handle(self):
    self.e.add_handler("test", self.test_function1)
    self.e.add_handler("test", self.test_function2)
    self.e.message("test")
    self.assertTrue(self.e.attribute("t1"))
    self.assertTrue(self.e.attribute("t2"))

  def test_message_no_handler(self):
    self.e.message("test")
    self.assertIsNone(self.e.attribute("t1"))

  def test_remove_handler(self):
    self.e.add_handler("test", self.test_function1)
    self.assertTrue(self.e.remove_handler("test"))
    self.e.message("test")
    self.assertIsNone(self.e.attribute("t1"))

  def test_remove_handler_multiple(self):
    self.e.add_handler("test", self.test_function1)
    self.e.add_handler("test", self.test_function2)
    self.assertTrue(self.e.remove_handler("test"))
    self.e.message("test")
    self.assertIsNone(self.e.attribute("t1"))
    self.assertIsNone(self.e.attribute("t2"))

  def test_remove_handler_unique(self):
    self.e.add_handler("test", self.test_function1)
    self.e.add_handler("test", self.test_function2)
    self.assertTrue(self.e.remove_handler("test", self.test_function1))
    self.e.message("test")
    self.assertIsNone(self.e.attribute("t1"))
    self.assertTrue(self.e.attribute("t2"))

  def test_remove_handler_nonexistent(self):
    self.assertFalse(self.e.remove_handler("test"))

class TestEntityComponent(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.c = component.Component()
    self.c.got_added = lambda e: e.add_attribute("added")
    self.c.got_removed = lambda e: e.add_attribute("removed")
    self.c.update = lambda e,p: e.add_attribute("updated")

  def test_add_component(self):
    self.assertTrue(self.e.add_component(self.c))
    self.assertTrue(self.e.attribute("added"))

  def test_remove_component(self):
    self.e.add_component(self.c)
    self.assertTrue(self.e.remove_component(self.c))
    self.assertTrue(self.e.attribute("added"))
    self.assertTrue(self.e.attribute("removed"))

  def test_remove_component_nonexistant(self):
    self.assertFalse(self.e.remove_component(self.c))
    self.assertIsNone(self.e.attribute("removed"))

  def test_update_component(self):
    self.e.add_component(self.c)
    self.e.add_handler("update", self.c.update)
    self.e.update()
    self.assertTrue(self.e.attribute("updated"))

if __name__ == '__main__':
  unittest.main()
