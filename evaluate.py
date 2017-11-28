#!/usr/bin/env python3

import sys
import csv
from simulator import Simulator

def main():
    with open('results.csv', 'w+') as out_file:
        wr = csv.writer(out_file)
        wr.writerow(['fish', 'predator', 'iteration', 'ticks', 'score'])
        for pred in ['s']:
            for fish in ['a', 'p', 'c']:
                for i in range(10):
                    print('running iteration {} with fish {} and predator {}'.format(i, fish, pred))
                    if len(sys.argv) > 1 and sys.argv[1] == 'p':
                        sim = Simulator(fish, pred, '{}_{}_{}_cdf.csv'.format(fish, pred, i))
                    else:
                        sim = Simulator(fish, pred)
                    ticks, score = sim.run()
                    wr.writerow([fish, pred, i, ticks, score])

if __name__ == "__main__":
    main()
