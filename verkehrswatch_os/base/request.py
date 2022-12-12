#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry



def send_request(url):
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.2,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    return http.get(url)
