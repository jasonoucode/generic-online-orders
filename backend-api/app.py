# ========== Imports all of the packages needed ==========
from flask import Flask
from flask_restful import Api


# imports all of the classes needed to have working routes
#		with various api functionality
from company import Company
from menu import Menu
#from menuitem import MenuItem
#from orders import Orders


#  ========== Setting up flask ==========
app = Flask(__name__)
api = Api(app)


# ========== Adding routes ==========
# Company Route - /<string:company>
api.add_resource(Company, '/<string:company>')
# Menu Route - /<string:company>/menu
api.add_resource(Menu, '/<string:company>/menu')
# Menu Item Route - /<string:company>/menu/<string:item>
#api.add_resource(MenuItem, '/<string:company>/menu/<string:item>')
# Orders Route - /<string:company>/orders
#api.add_resource(Orders, '/<string:company>/orders')


# Setting up the base url
if __name__ == '__main__':
	app.run(port=5000, debug=True)
