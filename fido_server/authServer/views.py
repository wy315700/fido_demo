#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
from authServer.models import UserPub, Policy, PolicyAlgs, PolicyScheme, AuthMeta, AuthAlgorithm, Scheme
from forms.userForms import LoginForm
from django.utils.safestring import SafeString


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



