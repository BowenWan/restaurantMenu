from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()





#The following four only involves restaurant excluding menuItems

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    items = session.query(Restaurant).all()
    return render_template('restaurants.html', items=items)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
    if request.method=='POST':
        newItem = Restaurant(name = request.form['name'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

#edit an existing restaurant name with a specific id
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    item = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method=='POST':
        #in case the menu item becomes nameless and will not show in the meni list in the individual restaurant page
        if request.form['name']:
            item.name = request.form['name']
            session.add(item)
            session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        # the variables for the template could be different from the corresponding function
        return render_template('editrestaurant.html', item=item)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    item = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', i=item)

#The order of the functions in python scripts matters
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
