from framework.webapp import MyResponse,myRedirect,WebApp, View,render_template
from framework.orm import DB

db = DB(host="localhost",user="root",password="root",db="m_blog")

class Index(View):
    def GET(self, request,response):
        blogs = db.query("blog")
        print(blogs)
        text =render_template("index.html",{"blogs":blogs})
        response = MyResponse(response=text,mimetype="text/HTML")
        print(response.data)
        return response

    def POST(self, request):
        print(request.method)
        return "post"



class Logout(View):
    def GET(self,request,response):
        response.delete_cookie(key="userName")
        print("logout")
        print(request.cookies.to_dict())
        return myRedirect("/")



class Blog(View):
    def GET(self,request,response):
        print("???????????")
        print(request.args.to_dict()["p"])
        blogs = db.query("blog",{"id":request.args.to_dict()["p"]})
        print(blogs[0])
        print("blog")
        temp = render_template("blog.html",{"blogs":blogs})
        response = MyResponse(temp,mimetype="text/HTML")
        return response


class Login(View):
    def GET(self,resquest,response):
        response = MyResponse(render_template('login.html'),mimetype="text/HTML")
        return response
    def POST(self,request,response):
        print(request)
        # return MyResponse(render_template('login.html'),mimetype="text/HTML")
        for i in request.form:
            print(type(i))
            print(i)
        form = request.form.to_dict()
        print("??????")
        print(form)
        userName = form["userName"]
        pwd = form["pwd"]
        print(userName)
        print(pwd)
        try:
            user = db.query("user",{"name":userName})
            print(user)
            user = user[0]
            if user["pwd"]!=pwd:
                return render_template("login.html")

        except:
            print("except")
            return render_template("login.html")
        response = MyResponse(render_template('login.html'),mimetype="text/HTML")
        response.set_cookie("userName","hby")
        return response


class Add(View):
    def GET(self,request,rseponse):
        cookie = request.cookies.to_dict()
        print(cookie)
        print(cookie["userName"])
        print("userName")
        if cookie["userName"] == None:
            return myRedirect('/')
        print(request.cookies)
        response = MyResponse(render_template("add.html"),mimetype="text/HTML")
        return response
    def POST(self,request,response):
        form = request.form.to_dict()
        content = form["content"]
        title = form["title"]
        cookie = request.cookies.to_dict()
        author = cookie["userName"]
        db.insert("blog",{"title":title,"content":content,"author":author})
        response = MyResponse(render_template("login.html"),mimetype="text/HTML")
        return myRedirect('/')


class Test(View):
    def GET(self, request,response):

        result = db.query("user")
        print(result)
        return response


class Cookie(View):
    def GET(self):
        # x = SecureCookie.unserialize(value, "deadbeef")
        pass

urls = [

    {
        'url': '/',
        'view': Index
    },
    {
        'url':'/blog',
        'view':Blog
    },
    {
        'url': '/test',
        'view': Test
    },
    {
        'url':'/logout',
        "view":Logout
    },
    {
        'url':'/login',
        'view':Login
    },
    {
        'url':'/add',
        'view':Add
    }

]

app = WebApp()

app.add_url_rule(urls)

app.run()
