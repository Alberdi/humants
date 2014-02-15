import random
import unittest

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
    self.test_function1 = lambda e: e.add_attribute("t1")
    self.test_function2 = lambda e: e.add_attribute("t2")

  def test_add_handler(self):
    self.assertTrue(self.e.add_handler("test", self.test_function1))

  def test_add_handler_multiple(self):
    self.e.add_handler("test", self.test_function1)
    self.assertTrue(self.e.add_handler("test", self.test_function1))

  def test_message(self):
    self.e.add_handler("test", self.test_function1)
    self.e.message("test")
    self.assertTrue(self.e.attribute("t1"))

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

class TestEntityCarry(unittest.TestCase):
  def setUp(self):
    self.e1 = entity.Entity()
    self.e2 = entity.Entity()
    self.e3 = entity.Entity()
    self.e1.add_attribute("carrier")
    self.e2.add_attribute("carrier")
    self.e2.add_attribute("carriable")
    self.e3.add_attribute("carriable")

  def test_carry(self):
    self.assertTrue(self.e1.carry(self.e2))
    self.assertIn(self.e2, self.e1.carries())

  def test_carry_entities(self):
    self.e1.carry_entity(self.e2)
    self.assertTrue(self.e1.carry(self.e3))
    self.assertIn(self.e2, self.e1.carries())
    self.assertIn(self.e3, self.e1.carries())

  def test_carry_noncarrier(self):
    self.assertFalse(self.e3.carry(self.e2))
    self.assertNotIn(self.e2, self.e3.carries())
    
  def test_carry_noncarriable(self):
    self.e2.remove_attribute("carriable")
    self.assertFalse(self.e1.carry(self.e2))
    self.assertNotIn(self.e2, self.e1.carries())

  def test_carry_chain(self):
    self.e2.carry(self.e3)
    self.assertTrue(self.e1.carry(self.e2))
    self.assertIn(self.e3, self.e2.carries())
    self.assertIn(self.e2, self.e1.carries())
    self.assertNotIn(self.e3, self.e1.carries())

  def test_carry_not_self(self):
    self.assertFalse(self.e2.carry(self.e2))

  def test_carry_not_carried(self):
    self.e1.carry(self.e3)
    self.assertFalse(self.e2.carry(self.e3))
    self.assertIn(self.e3, self.e1.carries())
    self.assertNotIn(self.e3, self.e2.carries())

if __name__ == '__main__':
  unittest.main()
