#!/usr/bin/python3

import monkey
import game


print(monkey.__file__)




a = monkey.engine()
a.load(game)
a.start()
a.shutdown()
