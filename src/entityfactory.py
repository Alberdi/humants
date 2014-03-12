import brains.lumberjack
import components.actor
import components.carrier
import components.gototarget
import components.hunger
import components.mortal
import components.position
import components.senescence
import components.woundable
import entity

def block():
  block = entity.Entity()
  block.add_component(components.position.Position())
  block.add_attribute("blocks_movement")
  return block

def canteen():
  canteen = entity.Entity()
  canteen.add_component(components.position.Position())
  canteen.add_attribute("type", "canteen")
  return canteen

def tree():
  tree = entity.Entity()
  tree.add_component(components.mortal.Mortal())
  tree.add_component(components.position.Position())
  tree.add_component(components.senescence.Senescence())
  tree.add_component(components.woundable.Woundable())
  tree.add_attribute("type", "tree")
  return tree

def log():
  log = entity.Entity()
  log.add_attribute("type", "log")
  return log

def lumberjack():
  lumberjack = entity.Entity()
  lumberjack.add_component(brains.lumberjack.Lumberjack())
  lumberjack.add_component(components.actor.Actor())
  lumberjack.add_component(components.carrier.Carrier())
  lumberjack.add_component(components.gototarget.GoToTarget())
  lumberjack.add_component(components.hunger.Hunger())
  lumberjack.add_component(components.position.Position())
  lumberjack.add_attribute("workplace", (0,0))
  lumberjack.add_attribute("wandering_distance", 10)
  return lumberjack
