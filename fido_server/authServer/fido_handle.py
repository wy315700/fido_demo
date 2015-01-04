#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from authServer.models import UserPub, Policy, PolicyAlgs, PolicyScheme, AuthMeta, AuthAlgorithm, Scheme, TrustedApps
from Crypto.PublicKey import RSA
from Crypto.Hash import MD5
import json
from base64 import urlsafe_b64encode,urlsafe_b64decode
from os import urandom
import hashlib
import struct

def userRegisteration(username, publickey, keyid, extension=None):
    UserPub.objects.create(username=username, publicKey=publickey, eyid=keyid, extension=extension)


def signatureVerification(publickey, content, signature):
    fullPub = '-----BEGIN PUBLIC KEY-----\n' + publickey.strip() + '\n-----END PUBLIC KEY-----'
    hashContent = MD5.new(content).digest()
    public = RSA.importKey(fullPub)
    return public.verify(hashContent, signature)


def generatePolicy(appid):
    print appid
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
            "aaid": p.aaid,
            "authenticationFactor": p.authFactor,
            "keyProtection": p.keyPro,
            "attachment": p.attachment,
            "secureDisplay": p.securDis,
            "supportedAuthAlgs" :algs,
            "supportedSchemes": schemes,
        }]
        accepted_list.append(accepte)
    policy = {
        'accepted' : accepted_list,
        'disallowed' : [{
            "aaid": "1234#5678"
        }]
    }
    return policy

def generateChanllenge(length = 64):
    global GLOBAL_CHALLENGE_SET
    random_bytes = urandom(length)
    challenge   = urlsafe_b64encode(random_bytes)
    GLOBAL_CHALLENGE_SET.add(challenge)
    print GLOBAL_CHALLENGE_SET
    return challenge

def verifyChallenge(challenge, need_delete = True):
    global GLOBAL_CHALLENGE_SET
    challenge = str(challenge)
    if challenge not in GLOBAL_CHALLENGE_SET:
        return False

    # GLOBAL_CHALLENGE_SET.remove(challenge)

    return True

def base64AddPadding(b64_string):
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    return b64_string

GLOBAL_CHALLENGE_SET = set(['54698zhfdksjgh876ujhghj7'])

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

    if not verifyChallenge(challenge):
        return False

    # TODO:verify appid && facetID
    trusted = TrustedApps.objects.filter(appid=appid)
    if trusted is not None:
        for app in trusted:
            if facetID == app.facetid:
                return True
    return False


def veryfiRegAssertion(assertion, fcParams):
    aaid = assertion['aaid']
    # attestationCert = assertion['attestationCert']
    scheme = assertion['scheme']
    krd = assertion['krd']

    # krd = 'AANLAAgAdGVzdEFBSUQxLjAAAQEAEgB0ZXN0RmluYWxDaGFsbGVuZ2UJAHRlc3RLZXlJRAAAAAAAAAAADQB0ZXN0UHVibGljS2V5AAYNAHRlc3RTaWduYXR1cmU='

    krd = urlsafe_b64decode(str(krd))

    authMeta = AuthMeta.objects.filter(aaid=aaid)

    if not authMeta:
        return False

    hashed_fcParms = hashlib.new('sha256', str(fcParams)).hexdigest()

    krd_tmp = str(krd)
    response = {}
    response['krd'] = {}
    # 1
    krd_tag_response, krd_response_length = struct.unpack('HH', krd_tmp[:4])
    krd_tmp_response = krd_tmp[4:]
    # 1.2
    krd_tag_krd, krd_krd_length = struct.unpack('HH', krd_tmp_response[:4])
    krd_tmp_krd = krd_tmp_response[4:krd_krd_length]
    # 1.3
    krd_tag_signature, krd_signature_size = struct.unpack('HH', krd_tmp_response[krd_krd_length:krd_krd_length + 4])
    krd_tmp_signature = krd_tmp_response[4 + krd_krd_length:krd_krd_length + krd_signature_size + 4]
    # # 1.4
    # krd_tag_certificate, krd_certificate_length = struct.unpack('HH', krd_tmp_response[krd_krd_length + krd_signature_length:krd_krd_length + krd_signature_length + 4])
    # krd_tmp_certificate = krd_tmp_response[4 + krd_krd_length + krd_signature_length:krd_krd_length + krd_signature_length + krd_certificate_length]

    # 1.3.1
    signature_size = krd_signature_size
    # 1.3.2
    response['signature'] = krd_tmp_signature[:signature_size]

    # # 1.4.1
    # certificate_size = struct.unpack('H', krd_tmp_krd[:2])
    # krd_tmp_certificate = krd_tmp_certificate[2:]
    # # 1.4.2
    # response['certificate'] = krd_tmp_certificate[:certificate_size]


    # 1.2.2
    aaid_size, = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.3
    response['krd']['aaid'] = krd_tmp_krd[:aaid_size]
    krd_tmp_krd = krd_tmp_krd[aaid_size:]
    # 1.2.4
    response['krd']['authenticator_version'], = struct.unpack('B', krd_tmp_krd[:1])
    krd_tmp_krd = krd_tmp_krd[1:]
    # 1.2.5
    response['krd']['publickey_alg_and_encoding'], = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.6
    response['krd']['signature_alg_and_encoding'], = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.7
    final_chanllenge_size, = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.8
    response['krd']['final_chanllenge'] = krd_tmp_krd[:final_chanllenge_size]
    krd_tmp_krd = krd_tmp_krd[final_chanllenge_size:]
    # 1.2.9
    keyid_size, = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.10
    response['krd']['keyid'] = krd_tmp_krd[:keyid_size]
    krd_tmp_krd = krd_tmp_krd[keyid_size:]
    # 1.2.11
    response['krd']['reg_count'], = struct.unpack('I', krd_tmp_krd[:4])
    krd_tmp_krd = krd_tmp_krd[4:]
    # 1.2.12
    response['krd']['sign_count'], = struct.unpack('I', krd_tmp_krd[:4])
    krd_tmp_krd = krd_tmp_krd[4:]
    # 1.2.13
    publickey_size, = struct.unpack('H', krd_tmp_krd[:2])
    krd_tmp_krd = krd_tmp_krd[2:]
    # 1.2.14
    response['krd']['public_key'] = krd_tmp_krd[:publickey_size]

    print response


def veryfiAuthAssertion(assertion, fcParams):
    aaid = assertion['aaid']
    keyid = assertion['KeyID']
    scheme = assertion['scheme']
    signed_data = assertion['signedData']

    signed_data = urlsafe_b64decode(base64AddPadding(str(signed_data)))

    authMeta = AuthMeta.objects.filter(aaid=aaid)

    if not authMeta:
        return False

    hashed_fcParms = hashlib.new('sha256', str(fcParams)).hexdigest()

    signed_data_tmp = str(signed_data)
    response = {}
    response['krd'] = {}
    # 1
    signed_data_tag_response, signed_data_response_length = struct.unpack('HH', signed_data_tmp)
    signed_data_tmp_response = signed_data_tmp[4:]
    # 1.2
    signed_data_tag_signed_data, signed_data_signed_data_length = struct.unpack('HH', signed_data_tmp_response)
    signed_data_tmp_signed_data = signed_data_tmp_response[4:signed_data_signed_data_length]
    # 1.3
    signed_data_tag_signature, signed_data_signature_length = struct.unpack('HH', signed_data_tmp_response[signed_data_signed_data_length:])
    signed_data_tmp_signature = signed_data_tmp_response[signed_data_signed_data_length + 4:signed_data_signed_data_length + signed_data_signature_length]

    # 1.3.1
    signature_size = struct.unpack('H', signed_data_tmp_signature)
    signed_data_tmp_signature = signed_data_tmp_signature[2:]
    # 1.3.2 
    response['signature'] = signed_data_tmp_signature[:signature_size]


    # 1.2.2
    response['krd']['authenticator_version'] = struct.unpack('B', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[1:]
    # 1.2.3
    response['krd']['authentication_mode'] = struct.unpack('B', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[1:]
    # 1.2.4
    response['krd']['signature_alg_and_encoding'] = struct.unpack('H', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[2:]
    # 1.2.5
    authnr_nonce_size = struct.unpack('H', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[2:]
    # 1.2.6
    response['krd']['authnr_nonce'] = signed_data_tmp_signed_data[:authnr_nonce_size]
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[authnr_nonce_size:]
    # 1.2.7
    final_chanllenge_size = struct.unpack('H', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[2:]
    # 1.2.8
    response['krd']['final_chanllenge'] = signed_data_tmp_signed_data[:final_chanllenge_size]
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[final_chanllenge_size:]
    # 1.2.9
    tchash_size = struct.unpack('H', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[2:]
    # 1.2.10
    response['krd']['tchash'] = signed_data_tmp_signed_data[:tchash_size]
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[tchash_size:]
    # 1.2.11
    response['krd']['sign_count'] = struct.unpack('I', signed_data_tmp_signed_data)
    signed_data_tmp_signed_data = signed_data_tmp_signed_data[4:]

