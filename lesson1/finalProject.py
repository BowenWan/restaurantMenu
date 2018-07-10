from flask import Flask
app = Flask(__name__)




#The following four only involves restaurant excluding menuItems

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "This page will show all my restaurants"

@app.route('/restaurant/new/')
def newRestaurant():
    return "This page will be for making a new restaurant"

#edit an existing restaurant name with a specific id
@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return "This page will be for editing restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return "This page will be for deleting restaurant %s" % restaurant_id

#The order of the functions in python scripts matters
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
