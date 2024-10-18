import logging
import re
import socket
import ssl
from collections import defaultdict
from urllib.parse import urlparse

import socks
from pyVim import connect
from pyVmomi import vim, vmodl

from datadog_checks.base import AgentCheck, is_affirmative
from datadog_checks.base.utils.common import to_string


def create_connection(address, timeout, source_address, proxy_host, proxy_port):
    return socks.create_connection(address, timeout, source_address, socks.SOCKS5, proxy_host, proxy_port)


class EsxiCheck(AgentCheck):

    # This will be the prefix of every metric and service check the integration sends
    __NAMESPACE__ = 'esxi'

    def __init__(self, name, init_config, instances):
        super(EsxiCheck, self).__init__(name, init_config, instances)
        self.host = self.instance.get("host")
        self.username = self.instance.get("username")
        self.password = self.instance.get("password")
        self.use_guest_hostname = is_affirmative(self.instance.get("use_guest_hostname", False))
        self.use_configured_hostname = is_affirmative(self.instance.get("use_configured_hostname", False))
        self.excluded_host_tags = self._validate_excluded_host_tags(self.instance.get("excluded_host_tags", []))
        self.collect_per_instance_filters = self._parse_metric_regex_filters(
            self.instance.get("collect_per_instance_filters", {})
        )
        self.resource_filters = self._parse_resource_filters(self.instance.get("resource_filters", []))
        self.metric_filters = self._parse_metric_regex_filters(self.instance.get("metric_filters", {}))
        self.ssl_verify = is_affirmative(self.instance.get('ssl_verify', True))
        self.ssl_capath = self.instance.get("ssl_capath")
        self.ssl_cafile = self.instance.get("ssl_cafile")
        self.tags = [f"esxi_url:{self.host}"]
        self.proxy_host = None
        self.proxy_port = None
        proxy = self.instance.get('proxy', init_config.get('proxy'))
        if proxy:
            parsed_proxy = urlparse(proxy)
            proxy_scheme = parsed_proxy.scheme
            if proxy_scheme != 'socks5':
                self.log.warning('Proxy scheme %s not supported; ignoring', proxy_scheme)
            else:
                self.proxy_host = parsed_proxy.hostname
                self.proxy_port = parsed_proxy.port
        self.conn = None
        self.content = None
        self.check_initializations.append(self.initiate_api_connection)


    def check(self, _):
        self.service_check("can_connect", AgentCheck.CRITICAL)
