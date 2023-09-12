#!/usr/bin/python3

import monkey
import monkey_toolkit

from game import settings

#monkey_toolkit.scumm.cippo = settings
monkey_toolkit.scumm.sima(settings)
monkey_toolkit.scumm.ciano()

a = monkey.engine()



a.start()
a.run()
a.shutdown()

