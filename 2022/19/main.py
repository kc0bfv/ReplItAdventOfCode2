#!/usr/bin/env python3

class Situation:
  def __init__(self, sit=None, timeleft=None, blueprint=None):
    assert(sit is not None or (timeleft is not None and blueprint is not None))
    self.ore_bots = sit.ore_bots if sit else 1
    self.clay_bots = sit.clay_bots if sit else 0
    self.obs_bots = sit.obs_bots if sit else 0
    self.geo_bots = sit.geo_bots if sit else 0
    self.time_left = sit.time_left if sit else timeleft
    self.blueprint = sit.blueprint if sit else blueprint
    self.ore = sit.ore if sit else 0
    self.clay = sit.clay if sit else 0
    self.obs = sit.obs if sit else 0
    self.geo = sit.geo if sit else 0

  def dec_time(self):
    new_sit = Situation(self)
    new_sit.time_left -= 1
    return new_sit
  
  def make_clay_bot(self):
    if self.ore < self.blueprint.clay_bot_ore:
      return None
    new_sit = self.dec_time()
    new_sit.collect()
    new_sit.clay_bots += 1
    new_sit.ore -= self.blueprint.clay_bot_ore
    return new_sit
    
  def make_obs_bot(self):
    if self.ore < self.blueprint.obs_bot_ore or self.clay < self.blueprint.obs_bot_clay:
      return None
    new_sit = self.dec_time()
    new_sit.collect()
    new_sit.obs_bots += 1
    new_sit.ore -= self.blueprint.obs_bot_ore
    new_sit.clay -= self.blueprint.obs_bot_clay
    return new_sit
    
  def make_geo_bot(self):
    if self.ore < self.blueprint.geo_bot_ore or self.obs < self.blueprint.geo_bot_obs:
      return None
    new_sit = self.dec_time()
    new_sit.collect()
    new_sit.geo_bots += 1
    new_sit.ore -= self.blueprint.geo_bot_ore
    new_sit.obs -= self.blueprint.geo_bot_obs
    return new_sit
    
  def make_ore_bot(self):
    if self.ore < self.blueprint.ore_bot_ore:
      return None
    new_sit = self.dec_time()
    new_sit.collect()
    new_sit.ore_bots += 1
    new_sit.ore -= self.blueprint.ore_bot_ore
    return new_sit

  def make_nothing(self):
    new_sit = self.dec_time()
    new_sit.collect()
    return new_sit
    
  def collect(self):
    self.ore += self.ore_bots
    self.clay += self.clay_bots
    self.obs += self.obs_bots
    self.geo += self.geo_bots

  def __hash__(self):
    return hash((self.ore_bots, self.clay_bots, self.obs_bots, self.geo_bots, self.time_left, self.ore, self.clay, self.obs, self.geo))
  def __eq__(self, oth):
    return hash(self) == hash(oth)

class Blueprint:
  def __init__(self, line):
    words = line.split(" ")
    self.num = int(words[1].strip(":"))
    self.ore_bot_ore = int(words[6])
    self.clay_bot_ore = int(words[12])
    self.obs_bot_ore = int(words[18])
    self.obs_bot_clay = int(words[21])
    self.geo_bot_ore = int(words[27])
    self.geo_bot_obs = int(words[30])

def gen_all_next_steps(sit, timeleft):
  assert(sit.time_left == timeleft + 1)
  ret_sits = set()
  ret_sits.add(sit.make_ore_bot())
  ret_sits.add(sit.make_clay_bot())
  ret_sits.add(sit.make_obs_bot())
  ret_sits.add(sit.make_geo_bot())
  ret_sits.add(sit.make_nothing())
  if None in ret_sits:
    ret_sits.remove(None)
  return ret_sits

def bfs(bp, endtime):
  frontier = set([Situation(timeleft=endtime+1, blueprint=bp)])

  for curtime in range(endtime):
    print(curtime)
    new_frontier = set()
    for cursit in frontier:
      new_frontier.update(gen_all_next_steps(cursit, endtime - curtime))
    frontier = new_frontier

  best = None
  for cursit in frontier:
    if best is None or cursit.geo > best.geo:
      best = cursit

  return best  

def main(filename):
  with open(filename, "r") as f:
    bps = [Blueprint(line) for line in f]

  bests = [bfs(bp, 24) for bp in bps]

  print([best.geo for best in bests])
  
if __name__ == "__main__":
  main("samp")
  #main("input.txt")