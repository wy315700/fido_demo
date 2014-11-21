#!/usr/bin/python  
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
import time

import json
import requests
from base64 import urlsafe_b64encode
from os import urandom


def getBindRequest(request):
    username = request.GET['username']
    appid    = request.GET['appid']
    header = {
        "op" : "Reg",
        "upv": {
            "mj" : 1,
            "mn" : 0
        },
        "appid" : appid
    }
    policy = {
        'accepted' : [[{
            "authenticationFactor": 0x00000000000001ff,
            "keyProtection": 0x000000000000000e,
            "attachment": 0x00000000000000ff,
            "secureDisplay": 0x000000000000001e,
            "supportedSchemes": "UAFV1TLV",
        }]],
        'disallowed' : {
            "aaid": "1234#5678"
        }
    }
    random_bytes = urandom(64)
    chanllenge   = urlsafe_b64encode(random_bytes)

    request = {
        'header' : header,
        'chanllenge' : chanllenge,
        'policy' : policy,
        'username' : username
    }
    return HttpResponse(json.dumps(request))

def getAuthRequest(request):
    username = request.GET['username']
    appid    = request.GET['appid']
    header = {
        "op" : "Auth",
        "upv": {
            "mj" : 1,
            "mn" : 0
        },
        "appid" : appid
    }
    policy = {
        'accepted' : [[{
            "authenticationFactor": 0x00000000000001ff,
            "keyProtection": 0x000000000000000e,
            "attachment": 0x00000000000000ff,
            "secureDisplay": 0x000000000000001e,
            "supportedSchemes": "UAFV1TLV",
        }]],
        'disallowed' : {
            "aaid": "1234#5678"
        }
    }
    random_bytes = urandom(64)
    chanllenge   = urlsafe_b64encode(random_bytes)
    transaction = {
        'contentType' : 'text/plain',
        'content' : 'hello world'
    }
    request = {
        'header' : header,
        'chanllenge' : chanllenge,
        'policy' : policy,
        'transaction' : transaction
    }
    return HttpResponse(json.dumps(request))



