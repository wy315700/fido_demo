#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from authServer.models import UserPub, Policy, PolicyAlgs, PolicyScheme
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import json
from base64 import urlsafe_b64encode,urlsafe_b64decode
from os import urandom


def userRegisteration(username, publickey, keyid, extension=None):
    userpub = UserPub(
        username=username,
        publicKey=publickey,
        keyid=keyid,
        extension=extension
    )
    userpub.save()


def signatureVerification(publickey, content, signature):
    fullPub = '-----BEGIN PUBLIC KEY-----\n' + publickey.strip() + '\n-----END PUBLIC KEY-----'
    hashContent = MD5.new(content).digest()
    public = RSA.importKey(fullPub)
    return public.verify(hashContent, signature)


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
            for x in policy_scheme:
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
    chanllenge = str(chanllenge)
    if chanllenge not in GLOBAL_CHANLLENGE_SET:
        return False

    GLOBAL_CHANLLENGE_SET.remove(chanllenge)

    return True

def base64AddPadding(b64_string):
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    return b64_string

GLOBAL_CHANLLENGE_SET = set('54698zhfdksjgh876ujhghj7')

def verifyHeaders(header):
    upv = header['upv']

    mj = upv['mj']
    mn = upv['mn']

    if mj != 1 or mn != 0:
        return False

    op = header['op']

    if op != 'Reg' and op != 'Auth':
        return False

    return op


def verifyFcParams(fcParams):
    print type(fcParams)
    fcp = urlsafe_b64decode(base64AddPadding(str(fcParams)))
    fcp = json.loads(fcp)
    appid = fcp['appID']
    challenge = fcp['challenge']
    facetID = fcp['facetID']
    tlsData = fcp['tlsData']

    if not verifyChanllenge(challenge):
        return False

    # TODO:verify appid && facetID

    return True


def veryfiRegAssertion(assertion):
    pass

def veryfiAuthAssertion(assertion):
    pass

