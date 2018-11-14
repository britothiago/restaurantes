from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                rest = session.query(Restaurant).all()
                saida = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                saida += "<html><body>"
                saida += "<a href='/restaurants/new'>Novo restaurante</a><br><br>"
                for r in rest:
                    saida += r.name + "<br><a href='" + str(r.id) + "/edit'>Editar" \
                                    "</a><br><a href='" + str(r.id) + "/delete'>Apagar</a><br><br><br>"
                saida += "</body></html>"
                self.wfile.write(saida)
                return
            if self.path.endswith("/restaurants/new"):
                saida = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                saida += "<html><body>"
                saida += """
                            <form action='/restaurants/new' method='post' enctype='multipart/form-data'>
                                <input type='text' name='restaurant'>
                                <input type='submit' value='Salvar'>
                            </form>
                         """
                saida += "</body></html>"
                self.wfile.write(saida)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurante = fields.get('restaurant')

            novorestaurante = Restaurant(name=restaurante[0])
            session.add(novorestaurante)
            session.commit()

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            saida = "<html><body>"
            saida += "Restaurante cadastrado com sucesso<br><br>"
            saida += "<a href='/restaurants'>Ver restaurantes cadastrado</a>"
            saida += "</body></html>"

            """ REDIRECIONAMENTO
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', '/restaurants')
            self.end_headers()
            """

            self.wfile.write(saida)
            print(saida)



        except:
            print("erro")

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print
        "Web Server rodando na porta %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print
        " ^C pressionado, parando web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
