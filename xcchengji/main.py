import web
import getjwxt
render = web.template.render('templates/')  

urls = (
    '/login', 'login',
    '/logout', 'logout',
    '/score', 'score'

        )


class logout(object):  
    def GET(self):  
        return render.index_logout()

class login(object):  
    def GET(self):  
        return render.index_login()

class score(object):
    def GET(self):
        self.POST()
    def POST(self):
        inputall =web.input(logname=None,logpass=None)
        name= inputall.logname
        pwd= inputall.logpass
        print name,pwd
        li = getjwxt.start(name,pwd)
        if li == -1:
        	return render.index_logout()
        else:
        	return render.bg(li)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()