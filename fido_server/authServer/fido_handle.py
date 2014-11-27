#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import json
from base64 import urlsafe_b64encode,urlsafe_b64decode
from os import urandom

def generatePolicy(appid):
    policies = Policy.objects.filter(appid = appid)
    accepted_list = []
    for p in policies:
        policy_algs = PolicyAlgs.objects.filter(pid=p.pid)
        algs = []
        if policy_algs:
            for x in policy_algs:
                algs.append(x.alid)
        policy_scheme = PolicyScheme.objects.filter(pid=p.pid)
        schemes = []
        if policy_scheme:
            for x in policy_schema:
                schemes.append(x.ssid)
        accepte = [{
            "authenticationFactor": p.authFactor,
            "keyProtection": p.keyPro,
            "attachment": p.attachment,
            "secureDisplay": p.secureDisplay,
            "supportedAuthAlgs" :algs,
            "supportedSchemes": schemes,
        }]
        accepted_list.append(accepte)
    policy = {
        'accepted' : accepted_list,
        'disallowed' : {
            "aaid": "1234#5678"
        }
    }
    return policy

def generateChanllenge(length = 64):
    global GLOBAL_CHANLLENGE_SET
    random_bytes = urandom(length)
    chanllenge   = urlsafe_b64encode(random_bytes)
    GLOBAL_CHANLLENGE_SET.add(chanllenge)
    print GLOBAL_CHANLLENGE_SET
    return chanllenge

GLOBAL_CHANLLENGE_SET = set()

def verifyHeaders(header):
    return True

def verifyFcParams(fcParams):
    fcp = urlsafe_b64decode(str(fcParams))
    print fcp