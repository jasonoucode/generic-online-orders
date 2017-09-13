# ========== Imports all of the packages needed ==========
from flask import request
from flask_restful import Resource


# ========== Imports all of the functions needed to have the route working ==========
from db.funcs_company import *
from db.funcs_menu import *


# The Menu class used for route api functions
class Menu(Resource):
	# GET Method - /<string:company>/menu
	def get(self, company):
		# If the company exists, then we can grab the menu of that company
		if (c_exists(company)):
			return c_message(company, c_message("Menu", m_get(company))), 200

		# Else we return that the company does not exist
		return c_message(company, company + " does not exist."), 400


	def post(self, company):
		pass


	def put(self, company):
		pass


	def delete(self, company):
		pass
