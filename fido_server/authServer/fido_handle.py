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

def verifyChanllenge(chanllenge, need_delete = True):
    global GLOBAL_CHANLLENGE_SET

    random_bytes = urandom(length)
    if chanllenge not in GLOBAL_CHANLLENGE_SET:
        return False

    GLOBAL_CHANLLENGE_SET.remove(chanllenge)

    return True

def base64AddPadding(b64_string):
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    return b64_string

GLOBAL_CHANLLENGE_SET = set()

def verifyHeaders(header):
    return True

def verifyFcParams(fcParams):
    print type(fcParams)
    fcp = urlsafe_b64decode(base64AddPadding(str(fcParams)))
    appid = fcp['appID']
    challenge = fcp['challenge']
    facetID = fcp['facetID']
    tlsData = fcp['tlsData']

    if not verifyChanllenge(chanllenge):
        return False

    # TODO:verify appid && facetID

    return True
