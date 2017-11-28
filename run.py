#!/usr/bin/env python3

import sys
from simulator import Simulator

def main():
    if len(sys.argv) < 2:
        sim = Simulator('c')
    else:
        sim = Simulator(sys.argv[1])
    print(sim.run())

if __name__ == "__main__":
    main()
