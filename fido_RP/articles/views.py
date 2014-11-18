#!/usr/bin/python  
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse 
from forms.userForms import LoginForm, RegistForm
from forms.articleForms import ArticleForm, CommentForm
from django.contrib.auth.models import User, Group
from articles.models import Essay, Tag, tagEssayRelation, Comment, supportCommentRelation, FacetIDs
from django.core.exceptions import ObjectDoesNotExist
import time

import json

# Create your views here.
def getMainPage(request):
    fails = False
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            userData = loginform.cleaned_data
            user = authenticate( username = userData['username'], password = userData['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                fails = True
                return render_to_response('login.html', locals(), context_instance = RequestContext(request))

    else:
        loginform = LoginForm()
    essays = Essay.objects.filter(essay_status = 'public')
    return render_to_response('index.html', locals(), context_instance = RequestContext(request))

# def userLogin(request):
#     fail = False
#     user = authenticate( username = request.POST['username'], password = request.POST['password'])
#     if user is not None:
#         login(request, user)
#         return HttpResponseRedirect('/index/')
#     else:
#         fail = True
#         return render_to_response('index.html', locals(), context_instance = RequestContext(request))

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/index/')

def userRegister(request):
    if request.method == "POST":
        regForm = RegistForm(request.POST)
        if regForm.is_valid():
            userInfo = regForm.cleaned_data
            user = User.objects.create_user(
                username = userInfo['username'],
                password = userInfo['password'],
                email = userInfo.get('email', 'noreply@example.com'),
                first_name = userInfo['first_name'],
                last_name = userInfo['last_name'],
                )
            newUser = authenticate( username = userInfo['username'], password = userInfo['password'])
            login(request, newUser)
            group = Group.objects.get(name = "normal user")
            group.user_set.add(user)
            return HttpResponseRedirect('/index/')
    else:
        regForm = RegistForm()
    return render_to_response('regist.html', locals(), context_instance = RequestContext(request))


def addComment(request):
    if request.method == "POST":
        commentForm = CommentForm(request.POST)
        print 'hello1'
        if commentForm.is_valid():
            print 'hello2'
            commentInfo = commentForm.cleaned_data
            print 'hello'
            print commentInfo['content']
            print commentInfo['essayId']
    
def editActicle(request):
    essayId = request.GET["essayId"]
    essay = Essay.objects.filter(id = essayId)[0]
    isEdit = essayId
    tagSet = tagEssayRelation.objects.filter(essayId = essay)
    tagStr = ""
    for tagRe in tagSet:
        tag = tagRe.tagId
        tagStr += tag.tag_name + ","
    tagStr = tagStr[ 0 : len(tagStr) - 1 ]
    articleForm = ArticleForm(
        initial = { 'subject' : essay.subject,
                    'content' : essay.content,
                    'isOrigin': essay.type,
                    'category':essay.category,
                    'status' : essay.essay_status,
                    'tag' : tagStr,
        }
    )
    isEdit = essayId
    return render_to_response('addArticle.html', locals(), context_instance = RequestContext(request))

def handleTag(tagStr, newEssay):
    tag_id = 0
    final_tag = Tag()
    tagList = tagStr.split(',')
    for item in tagList:
        essay_tag = item.strip().lower()
        try:
            old_tag = Tag.objects.get(tag_name = essay_tag)
        except ObjectDoesNotExist:
            new_tag = Tag(
                tag_name = essay_tag,
                category = 0,
                )
            new_tag.save()
            final_tag = new_tag
        else:
            final_tag = old_tag
        tagessay_relation = tagEssayRelation(
            essayId = newEssay,
            tagId = final_tag,
            )
        tagessay_relation.save()


def addArticle(request):
    if request.method == "POST":
        articleForm = ArticleForm(request.POST)
        oldEssayId = int(request.GET.get('edit', '0'))
        if articleForm.is_valid():
            articleInfo = articleForm.cleaned_data
            if oldEssayId == 0:
                newEssay = Essay(
                    subject = articleInfo['subject'],
                    type = articleInfo['isOrigin'],
                    category = articleInfo['category'],
                    content = articleInfo['content'],
                    modification_date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                    publish_date = time.strftime('%Y-%m-%d',time.localtime(time.time())),
                    essay_status = articleInfo['status']
                )
                newEssay.save()
                tagStr = articleInfo['tag']
                handleTag(tagStr, newEssay)
            else:
                newEssay = Essay.objects.filter(id = oldEssayId)[0]
                newEssay.subject = articleInfo['subject']
                newEssay.type = articleInfo['isOrigin']
                newEssay.category = articleInfo['category']
                newEssay.content = articleInfo['content']
                newEssay.modification_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                newEssay.status = articleInfo['status']
                newEssay.save()
                tagStr = articleInfo['tag']
                handleTag(tagStr, newEssay)
            return HttpResponseRedirect('/index/')
    else:
        articleForm = ArticleForm()
        isEdit = 0
    return render_to_response('addArticle.html', locals(), context_instance = RequestContext(request))

def showArticle(request):
    isSupported = []
    hi = "hello"
    if request.method == "POST":
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            commentInfo = commentForm.cleaned_data
            user = User.objects.filter(id = commentInfo["publisher"])[0]
            essay = Essay.objects.filter(id = commentInfo["essayId"])[0]
            comment = Comment(
                essay = essay,
                publisher = user,
                tend = commentInfo["tend"],
                content = commentInfo["content"],
                publish_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                support_num = 0,
                )
            comment.save()
            return HttpResponseRedirect('/article/?id=' + str(commentInfo["essayId"]))
    else:
        essay = Essay.objects.filter(id = request.GET.get('id'))[0]
        comments = Comment.objects.filter(essay = request.GET.get('id'))
        for comment in comments:
            if len(supportCommentRelation.objects.filter(userId = request.GET.get('uid'), commentId = comment.id)) != 0:
                comment.isSupported = True
            else:
                comment.isSupported = False
        commentForm = CommentForm()
    return render_to_response('article.html', locals(), context_instance = RequestContext(request))

def getUser(request):
    userInfo = User.objects.filter(id = request.GET.get('userId'))[0]
    return render_to_response('userInfo.html', locals())

def getFaceIdList(request):
    facetIds = FacetIDs.objects.all();
    return render_to_response('facetId.html', locals())

def delComment(request):
    Comment.objects.filter(id = request.GET.get('commentId')).delete()
    return HttpResponseRedirect('/article/?id=' + request.GET.get('essayId'))

def delArticle(request):
    Essay.objects.filter(id = request.GET.get('essayId')).delete()
    return HttpResponseRedirect('/index/')

def showSupport(request):
    commentId = request.GET['commentId']
    userId = request.GET['userId']
    commentSet = Comment.objects.filter(id = commentId)
    supportNum = commentSet[0].support_num
    relationSet = supportCommentRelation.objects.filter(commentId = commentId, userId = userId)
    relationExist = len(relationSet)
    if relationExist != 0 :
        supportNum -= 1
        relationSet.delete()
        commentSet.update(support_num = supportNum)
    else :
        supportNum += 1
        commentSet.update(support_num = supportNum)
        relation = supportCommentRelation(
                commentId = commentSet[0],
                userId = User.objects.filter(id = userId)[0],
            )
        relation.save()
    return HttpResponse(supportNum)

def getTrustedApps(request):
    facetIds = FacetIDs.objects.all();
    version = {
        "mj" : 1,
        "mn" : 0,
    }
    facetIdList = []
    for x in facetIds:
        facetIdList.append(x.facetId)
    TrustedApps = {
        "version" : version,
        "ids"     : facetIdList,
    }
    return HttpResponse(json.dumps(TrustedApps), content_type = "vnd.fi- do.trusted-apps+json")
