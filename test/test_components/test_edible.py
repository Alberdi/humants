import unittest

import components.edible
import entity

class TestEdible(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.e.add_component(components.edible.Edible())

  def test_got_eaten_handler(self):
    self.e.add_handler("died", lambda e,p:
                                      e.add_attribute("died_"+p["reason"]))
    self.e.message("got_eaten", {"eater": entity.Entity()})
    self.assertTrue(self.e.attribute("died_got_eaten"))

if __name__ == "__main__":
  unittest.main()
