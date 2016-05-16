# coding=utf-8
'''
            view.py
'''
import hashlib

from flask import Flask,render_template,url_for,redirect,request,\
    flash,session, g, abort,make_response
import xml.etree.ElementTree as ET
import time
from app import app
from tools import *

help = "智程 v0.1 命令详解：\n天气：获取当前德阳的天气。\n帮助：命令详细列表"
subscribe = '欢迎使用 智程 v0.1 \n详细用法请直接回复  帮助'
reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

app.config.from_object('config')

@app.route('/',methods=['GET','POST'])
def wechat_auth():
    #消息有效性验证
    if request.method == 'GET':
        token = 'dyoo'
        query = request.args
        signature = query.get('signature','')
        timestamp = query.get('timestamp','')
        nonce = query.get('nonce','')
        echostr = query.get('echostr','')

        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    #获取消息XML
    xml_recv = ET.fromstring(request.data)
    ToUserName = xml_recv.find('ToUserName').text
    FromUserName = xml_recv.find('FromUserName').text
    MsgType = xml_recv.find('MsgType').text
    Content = '你刚才发送的什么指令，能在说一遍么，我给忘了。'
    if MsgType == 'text': #文字消息
        Content = xml_recv.find('Content').text
        # reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        Content = tool(Content)
    elif MsgType == 'image':
        # PicUrl = xml_recv.find('PicUrl').text
        Content = '我现在还小，还读不懂图片的。能等我大一点么?\n也许到 V1.0我就能读懂了。'
    elif MsgType == 'event': #关注事件
        Event = xml_recv.find('Event').text
        if Event == 'subscribe': #subscribe(订阅)、unsubscribe(取消订阅)
            Content = subscribe

    response = make_response(reply %(FromUserName,ToUserName,str(int(time.time())),Content))
    response.content_type = 'application/xml'
    return response
def tool(name):

    if name is None:
        return
    zc = Zhicheng()
    if name == u'天气':
        return  zc.tianqi('deyang')
    elif name == u'帮助':
        return help
@app.route('/index')
def index():
    return 'Hello!'



