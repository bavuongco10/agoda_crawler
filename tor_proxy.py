#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 23 05:17:02 2020

@author: user
"""
from stem import Signal
from stem.control import Controller
import requests

proxies = {
  'http': 'http://127.0.0.1:8118',
}


def respawn_new_proxy():
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)

  print('new tor proxy')

  # print(requests.get('http://httpbin.org/ip', proxies=proxies).text)