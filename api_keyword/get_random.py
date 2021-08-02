# -*- coding: utf-8 -*-
# @Author  : Joy
# @FileName: get_random.py
import random


def get_random():
    randomres = "202108" + "".join(random.sample("0123456789",5))
    return randomres