#!/usr/bin/env python

import re
import matplotlib.pyplot as pl
from argparse import ArgumentParser

HR = 0.03       # high ratio alter level
LR = -0.05      # low ratio alter level

POLL = 100000.00    # total chips
HAND = 0.3          # per deal hand

def read_data(data_file = "./data_file"):
    with open(data_file) as f:
        row = [re.split(r' ', line.strip()) for line in f if line.strip()]

    return [map(float, r) for r in row]

def calc_a(data, hr, lr, hand, p):
    l,h,c = data[0]

    hold = int(p/2/c)
    poll = p - hold * c

    trend = []
    wealth = []

    for L,H,C in data[1:]:
        trend.append(c)
        wealth.append(poll + hold * c)

        h_ratio = (H - c) / c
        l_ratio = (c - L) / c
        if (h_ratio >= hr):
            hold = hold - int(hold * hand)
            poll = poll + (hold * hand) * (1 + hr) * c
        else:
            pass

        if (l_ratio <= lr):
            poll = poll - poll * hand
            hold = hold + int((poll * hand) / ((1 - lr) * c))
        else:
            pass

        c = C

    pl.subplot(212)
    pl.plot(trend)
    pl.subplot(211)
    pl.plot(wealth)

    pl.show()

def main():
    parser = ArgumentParser(
        description="Calc history data to make a more valuable strategy.")
    parser.add_argument("-H", dest="h_ratio",
                        default=HR,
                        help="high level selling triger ratio. range from 0~0.10")
    parser.add_argument("-L", dest="l_ratio",
                        default=LR,
                        help="Low level buying triger ratio. range from 0~(-0.10)")
    parser.add_argument("-D", dest="hand",
                        default=HAND,
                        help="Every buy or sell persent.")
    parser.add_argument("-P", dest="poll",
                        default=POLL,
                        help="Total chips set at very begining.")
    parser.add_argument("-f", dest="fname", default="./data_file",
                        help="Data file. Should be a txt format file within 3 columns seperated by space.\
                        ie. low high close.")
    args = parser.parse_args()

    d = read_data(args.fname)
    calc_a(d, float(args.h_ratio), float(args.l_ratio), float(args.hand), args.poll)


if __name__ == "__main__":
    main()