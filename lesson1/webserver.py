from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
## import CRUD  Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += "<a href = '/hello' >Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hola'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print (output)
                return

            #
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                '''
                myFirstRestaurant = Restaurant(name = "Pizza Palace")
                session.add(myFirstRestaurant)
                cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
                session.add(cheesepizza)
                session.commit()
                '''
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<a href = '/restaurants/new' >Make a New Restaurant Here</a>"
                output += "<br>"
                output += "<html><body>"
                output += "<h2>Restaurant Lists</h2>"
                for restaurant in restaurants:
                    output += restaurant.name + "<br />"
                    output += "<a href = '/restaurants/%s/edit' >Edit</a> <br>" % restaurant.id
                    output += "<a href = '/restaurants/%s/delete' >Delete</a> <br>" % restaurant.id
                    output += "<br>"

                output += "</body></html>"
                self.wfile.write(output)
                #print(output)
                return

            if self.path.endswith("/edit"):
                #query item by id
                ID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=ID).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    #ask for information
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Give a New Restaurant Name<h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit' >" % ID
                    output += "<input name ='newRestaurantName' type='text' placeholder='%s'>" % restaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return

            if self.path.endswith("delete"):
                ID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=ID).one()
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete' >" % ID
                    output += "<h1>Are you sure you want to delete %s<h1>" %restaurant.name
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body><html>"
                    self.wfile.write(output)



            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'></form>"

                output += "</body></html>"
                self.wfile.write(output)
                #print(output)
                return

            #
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/hello") or self.path.endswith("hola"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print (output)

            if self.path.endswith("/restaurants/new"):
                #it must be 301 state code for redirct, 201 will fail
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    #Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

            if self.path.endswith("/edit"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    ID = self.path.split("/")[2]
                    #grab the restaurant entry
                    restaurant = session.query(Restaurant).filter_by(id = ID).one()
                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()

            if self.path.endswith('/delete'):
                ID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id=ID).one()
                if restaurant:
                    #redirct
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    session.delete(restaurant)
                    session.commit()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print 'Web server running on port %s' %port
        server.serve_forever()

    except KeyboardInterrupt:
        print ("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()
