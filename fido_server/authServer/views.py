#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from authServer.models import UserPub, Policy, PolicyAlgs, PolicyScheme, AuthMeta, AuthAlgorithm, Scheme
from forms.userForms import LoginForm
from django.utils.safestring import SafeString

import time

import json
from base64 import urlsafe_b64encode
from os import urandom


def getMainPage(request):
    fails = False
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            userData = loginform.cleaned_data
            user = authenticate(username = userData['username'], password = userData['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/meta/')
            else:
                fails = True
                loginform = LoginForm()
                return render(request, 'login.html', locals())
    loginform = LoginForm()
    return render(request, 'login.html', locals())

def getuserpub(request):
    if request.user.is_authenticated():
        userpub = UserPub.objects.all()
        return render(request, 'userpub.html', locals())
    else:
        loginform = LoginForm()
        return render(request, 'login.html', locals())


def getpolicy(request):
    if request.user.is_authenticated():
        policies = Policy.objects.all()
        algorithmNum = ""
        schemeNum = ""
        newPolicies = []
        for policy in policies:
            paRelations = PolicyAlgs.objects.filter(pid=policy.pid)
            if paRelations is not None:
                for parelation in paRelations:
                    algorithmNum += "(" + str(parelation.alid) + ") "
            policy.algorithm = algorithmNum
            psRelations = PolicyScheme.objects.filter(pid=policy.pid)
            if psRelations is not None:
                for psrelation in psRelations:
                    schemeNum += "(" + str(psrelation.ssid) + ") "
            policy.scheme = schemeNum
            newPolicies.append(policy)
        return render(request, 'policy.html', locals())
    else:
        loginform = LoginForm()
        return render(request, 'login.html', locals())


def getAuthenticatorMeta(request):
    if request.user.is_authenticated():
        authMeta = AuthMeta.objects.all()
        return render(request, 'authmeta.html', locals())
    else:
        loginform = LoginForm()
        return render(request, 'login.html', locals())


def getAlgsAndScheme(request):
    if request.user.is_authenticated():
        algs = AuthAlgorithm.objects.all()
        schemes = Scheme.objects.all()
        return render(request, 'algsSch.html', locals())
    else:
        loginform = LoginForm()
        return render(request, 'login.html', locals())


def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/index/')


def validated(request):
    json_value = request.GET['value']
    set_validated = bool(int(request.GET['setValidated']))
    data = json.loads(json_value)
    upid = int(data['upid'])
    userpub = UserPub.objects.filter(upid=upid)[0]
    userpub.isValidate = set_validated
    userpub.save()
    return HttpResponse(upid)


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
    policy = generatePolicy(appid)
    chanllenge   = generateChanllenge()

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
    policy = generatePolicy(appid)
    
    chanllenge   = generateChanllenge()

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

