#!/usr/bin/python3

import yaml

import monkey
import monkey_toolkit
from game import settings

monkey_toolkit.init(settings)
with open("assets/models.yaml", "r") as stream:
    try:
        settings.models = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

a = monkey.engine()

a.start()
a.run()
a.shutdown()

