import re


def robot_reader(path):
    robots = set()
    with open(path) as fin:
        for r in fin:
            robots.add(r.strip().lower())

    return [re.compile(pattern) for pattern in robots]
