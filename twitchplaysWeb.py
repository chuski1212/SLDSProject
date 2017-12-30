import tornado.ioloop
import tornado.web
import tornado.websocket
import json


nclients = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        nclients.append(self)
    def on_close(self):
        nclients.remove(self)

webapplication = tornado.web.Application([
    (r"/cascade",MainHandler),
    (r"/socket",SocketHandler)
    ])

def send(data):
    msg = json.dumps(data)
    for client in nclients:
        client.write_message(msg)

def init():
    print("Webservice iniciado.")
    webapplication.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


