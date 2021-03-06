import unittest

import entityfactory
import world

class TestLumberjack(unittest.TestCase):
  def setUp(self):
    self.e = entityfactory.lumberjack()
    world.entities.append(self.e)
    self.t1 = entityfactory.tree()
    self.t1.update_attribute("age", 2000)
    self.t1.update_attribute("age_etape", "adult")
    self.t1.message("moved", {"new_position": (2,2)})
    world.entities.append(self.t1)
    self.t2 = entityfactory.tree()
    self.t2.update_attribute("age", 2000)
    self.t2.update_attribute("age_etape", "adult")
    self.t2.message("moved", {"new_position": (3,0)})
    world.entities.append(self.t2)
    self.c = entityfactory.canteen()
    self.c.message("moved", {"new_position": (0,1)})
    world.entities.append(self.c)

  def tearDown(self):
    world.reset()

  def test_notrees(self):
    self.t1.message("died")
    self.t2.message("died")
    for i in range(10):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_newtree(self):
    self.t1.message("died")
    self.t2.message("died")
    for i in range(10):
      self.e.update()
    t = entityfactory.tree()
    t.update_attribute("age", 2000)
    t.update_attribute("age_etape", "adult")
    t.message("moved", {"new_position": (1,2)})
    world.entities.append(t)
    for i in range(10):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (1,2))
 
  def test_gotocloser(self):
    for i in range(10):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (2,2))

  def test_closer_is_blocked(self):
    block = entityfactory.block()
    block.message("moved", {"new_position": (2,2)})
    for i in range(10):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (3,0))

  def test_closer_got_blocked(self):
    for i in range(4):
      self.e.update()
    block = entityfactory.block()
    block.message("moved", {"new_position": (2,2)})
    for i in range(6):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (3,0))

  def test_all_blocked(self):
    block = entityfactory.block()
    block.message("moved", {"new_position": (2,2)})
    block = entityfactory.block()
    block.message("moved", {"new_position": (3,0)})
    for i in range(5):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_all_far(self):
    self.e.update_attribute("wandering_distance", 1)
    for i in range(5):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_closer_is_young(self):
    self.t1.update_attribute("age", 20)
    self.t1.update_attribute("age_etape", "young")
    for i in range(10):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (3,0))

  def test_all_young(self):
    self.t1.update_attribute("age", 20)
    self.t1.update_attribute("age_etape", "young")
    self.t2.update_attribute("age", 20)
    self.t2.update_attribute("age_etape", "young")
    for i in range(5):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_recollection(self):
    for i in range(100):
      self.e.update()
    self.assertEqual(len(filter(lambda e: e.attribute("type") == "log",
                            world.positions[(0,0)])), 2)

  def test_recollection_new_trees(self):
    for i in range(100):
      self.e.update()
    self.assertEqual(world.positions[(2,2)][0].attribute("age_etape"),
                     "newborn")
    self.assertEqual(world.positions[(3,0)][0].attribute("age_etape"),
                     "newborn")

  def test_hungry(self):
    self.e.update_attribute("hungry", True)
    for i in range(4):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,1))

  def test_hungry_closer_canteen(self):
    c = entityfactory.canteen()
    c.message("moved", {"new_position": (3,1)})
    world.entities.append(c)
    self.e.update_attribute("hungry", True)
    for i in range(4):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,1))

if __name__ == "__main__":
  unittest.main()
