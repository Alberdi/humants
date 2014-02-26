import unittest

import components.senescence
import entity

class TestMortal(unittest.TestCase):
  def setUp(self):
    self.e = entity.Entity()
    self.s = components.senescence.Senescence()
    self.s.age_etapes = {1: "young", 3: "adult", 5: "old", 6: "dead"}
    self.e.add_component(self.s)

  def test_age_etapes(self):
    for i in range(7):
      if i in self.s.age_etapes:
        comparator = self.s.age_etapes[i]
      elif i == 0:
        comparator = "newborn"
      elif i == 2:
        comparator = "young"
      elif i == 4:
        comparator = "adult"
      self.assertEqual(self.e.attribute("age_etape"), comparator)
      self.e.update()

  def test_grown_messages(self):
    self.e.add_handler("grown", lambda e,p:
                        e.add_attribute("test", p["new_etape"]))
    for i in range(6):
      if i in self.s.age_etapes:
        self.assertEqual(self.e.attribute("test"), self.s.age_etapes[i])
      self.e.update()

if __name__ == "__main__":
  unittest.main()
