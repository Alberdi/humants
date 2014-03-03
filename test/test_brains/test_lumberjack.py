import unittest

import entityfactory
import world

class TestLumberjack(unittest.TestCase):
  def setUp(self):
    self.e = entityfactory.lumberjack()
    world.entities.append(self.e)
    self.t1 = entityfactory.tree()
    self.t1.message("moved", {"new_position": (2,2)})
    world.entities.append(self.t1)
    self.t2 = entityfactory.tree()
    self.t2.message("moved", {"new_position": (3,0)})
    world.entities.append(self.t2)

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

  def test_all_closed(self):
    block = entityfactory.block()
    block.message("moved", {"new_position": (2,2)})
    block = entityfactory.block()
    block.message("moved", {"new_position": (3,0)})
    for i in range(5):
      self.e.update()
    self.assertEqual(self.e.attribute("position"), (0,0))

  def test_recollection(self):
    for i in range(100):
      self.e.update()
    self.assertEqual(len(filter(lambda e: e.attribute("type") == "log",
                            world.positions[(0,0)])), 2)

if __name__ == "__main__":
  unittest.main()
