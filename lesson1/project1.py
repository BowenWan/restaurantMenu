from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route ('/restaurants/<int:id>/')
def HelloWorld(id):
    items = session.query(MenuItem).filter_by(restaurant_id=id)
    output = '<h1>Restaurant ID: %s</h1> <br>' % id
    for i in items:
        output += i.name + '<br>'
        output += i.price + '<br>'
        output += i.description + '<br><br>'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
