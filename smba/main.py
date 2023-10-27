#!/usr/bin/python3

import yaml

import monkey
import monkey_toolkit
from game import settings


def read_yaml(file):
    with open(file, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)


monkey_toolkit.init(settings)
settings.models = read_yaml('assets/models.yaml')
settings.rooms = read_yaml('assets/rooms.yaml')

a = monkey.engine()

a.start()
a.run()
a.shutdown()

