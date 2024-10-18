# (C) Datadog, Inc. 2024-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

HOST_METRICS = {
    'cpu.coreUtilization.avg',
    'cpu.usage.avg',
    'cpu.used.sum',
    'cpu.utilization.avg',
    'mem.active.avg',
    'mem.totalCapacity.avg',
    'mem.unreserved.avg',
    'mem.usage.avg',
}

VM_METRICS = {
    'cpu.coreUtilization.avg',
    'cpu.usage.avg',
    'cpu.used.sum',
    'cpu.utilization.avg',
    'mem.active.avg',
    'mem.totalCapacity.avg',
    'mem.unreserved.avg',
    'mem.usage.avg',
}
RESOURCE_NAME_TO_METRICS = {
    "vm": VM_METRICS,
    "host": HOST_METRICS,
}


REFERENCE_METRIC = "cpu.usage.avg"

# Set of metrics that are emitted as percentages between 0 and 100. For those metrics, we divide the value by 100
# to get a float between 0 and 1.
PERCENT_METRICS = {
    'cpu.coreUtilization.avg',
    'cpu.usage.avg',
    'cpu.utilization.avg',
    'mem.usage.avg',
}
