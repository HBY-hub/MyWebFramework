from werkzeug.serving import run_simple
from werkzeug.wrappers import Response, Request
from flask import Flask,Blueprint
from framework.template import Template
from framework.webapp import render_template


@Request.application
def app(request):
    # print(request.method)
    return Response("hello world")



con = {"url":"kkkkk","content":"knknknk"}
print(con["url"])
print(render_template('index.html', {'title': '题目', "names": ["bob", "alice"],"items":[{"url":"kkkkk","content":"knknknk"},{"url":"kkk","content":"knknk"}]}))

