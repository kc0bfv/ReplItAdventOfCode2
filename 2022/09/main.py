#!/usr/bin/env python3

class Rope:
  def __init__(self):
    self.head = (0,0)
    self.tail = self.head
    self.head_pos = list()
    self.tail_pos = list()

  def move_head(self, dir, dist):
    pass

  def update_tail(self):
    pos0_dist = self.head[0] - self.tail[0]
    pos1_dist = self.head[1] - self.tail[1]

    if abs(pos0_dist) > 1 and abs(pos1_dist) <= 1:
      new0 = self.tail[0] + pos0_dist - 1
    

def main(filename):
  with open(filename, "r") as f:
    lines = [l.strip() for l in f]

  print(lines[0])

if __name__ == "__main__":
  main("samp")
  #main("input.txt")