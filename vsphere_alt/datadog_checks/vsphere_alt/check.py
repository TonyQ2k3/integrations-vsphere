from __future__ import division

import datetime as dt
import logging
from collections import defaultdict
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Set, Type, cast  # noqa: F401

from pyVmomi import vim, vmodl


SERVICE_CHECK_NAME = 'can_connect'


class VsphereAltCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'vsphere_alt'

    def __init__(self, name, init_config, instances):
        super(VsphereAltCheck, self).__init__(name, init_config, instances)
        self.service_check("can_connect", AgentCheck.CRITICAL)
