import random
import unittest

import entity

class TestEntityTrait(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()

  def test_add_trait(self):
    self.assertTrue(self.e.add_trait("test"))

  def test_trait(self):
    self.e.add_trait("test")
    self.assertTrue(self.e.trait("test"))

  def test_not_trait(self):
    self.e1.assertIsNone(self.e.trait("test"))

  def test_add_trait_value(self):
    self.assertTrue(self.e.add_trait("test", "value"))

  def test_add_trait_value_int(self):
    self.assertTrue(self.e.add_trait("test", 5))

  def test_trait_value(self):
    self.e.add_trait("test", "value")
    self.assertEquals(self.e.trait("test"), "value")

  def test_trait_value_int(self):
    self.e.add_trait("test", 5)
    self.assertTrue(self.e.trait("test"), 5)

  def test_remove_trait(self):
    self.e.add_trait("test")
    self.assertTrue(self.e.remove_trait("test"))
    self.assertIsNone(self.e.trait("test"))

  def test_remove_trait_nonexistent(self):
    self.assertFalse(self.e.remove_trait("test"))

class TestEntityCarry(unittest.TestCase):
  def setUp(self):
    self.e1 = entity.Entity()
    self.e2 = entity.Entity()
    self.e3 = entity.Entity()
    self.e1.add_trait("carrier")
    self.e2.add_trait("carrier")
    self.e2.add_trait("carriable")
    self.e3.add_trait("carriable")

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
    self.e2.remove_trait("carriable")
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
