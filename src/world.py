from collections import defaultdict

entities = []
positions = defaultdict(list)

def reset():
  global entities, positions
  entities = []
  positions = defaultdict(list)
