import argparse
import json


def parse_datafile(path: str):
    with open(path) as f:
        data = json.load(f)
    return data


def init_parser():
    parser = argparse.ArgumentParser(
        prog="UglyPlotter",
        description="I will generate some ugly plots",
    )
    parser.add_argument("filename", help="Path to data file")  # positional argument
    parser.add_argument("--name", default="plot.png", help="Plot's name")
    return parser
