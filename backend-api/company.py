# ========== Imports all of the packages needed ==========
from flask import request
from flask_restful import Resource


# ========== Imports all of the functions needed to have the route working ==========
from db.funcs_company import *

# The Company class used for route api functions
class Company(Resource):
	# GET Method - /<string:company>
	def get(self, company):
		# Makes sure database is initialized
		c_initdb()

		# Checks if the user wants a list of all companies or just an individual company
		if (company == "getall"):
			return c_message("companies", c_getall()), 200

		# If the company exists, then we can grab information about the company
		if (c_exists(company)):
			return c_message(company, c_get(company)), 200

		# Else we return that the company does not exist
		return c_message(company, company + " does not exist."), 400


	# POST Method - /<string:company>
	def post(self, company):
		# getall is reserved for getting a list of all companies
		if (company == "getall"):
			return c_message("getall", "cannot be named to this."), 400

		# Makes sure database is initialized
		c_initdb()

		# If the company already exists, then the post method fails
		if (c_exists(company)):
			return c_message(company, company + " already exists."), 400

		# Else we create the company
		return c_post(company), 201


	# PUT Method - /<string:company>
	# QUERY STRING - /<string:company>?rename=string
	# JSON DATA - { rename: "string" }
	def put(self, company):
		# getall is reserved for getting a list of all companies
		if (company == "getall"):
			return c_message("getall", "cannot be named to this."), 400

		# Makes sure database is initialized
		c_initdb()

		# The table does not exist,
		#		then we just create the table
		if (not c_exists(company)):
			return c_post(company), 201

		# Prioritize query strings over json data
		data = request.args.to_dict()
		# If there is no query string
		if not data:
			# Checks if there is any json data being sent in
			data = request.get_json(silent=True)

			# If there is no data by the very end of this,
			#		then that means theres nothing we can do to rename
			if not data:
				# If the company exists and there is no rename variable
				#		being sent in, then that means we have an error
				return c_message(company, "nothing to rename."), 400


		# Make sure we have the correct data that we want.
		try:
			if (c_exists(data["rename"])):
				return c_message(data["rename"], "rename failed, cannot rename to existing company."), 400
		except:
			return c_message("key error", "key must be 'rename' and value must be a string."), 400


		# getall is reserved for getting a list of all companies
		if (data["rename"] == "getall"):
			return c_message("getall", "cannot be named to this."), 400

		# In this case, if there is data being sent in and the company name
		#		already exists, then all we have to do is just rename the
		#		existing company as long as the user isnt trying to rename
		#		the company to itself.
		if (c_exists(company)):
			if (company == data["rename"]):
				return c_message(company, "cannot rename to " + data["rename"] + "."), 400
			# If it is not trying to rename itself to it's old name, then that
			#		we can rename it properly now
			return c_rename(company, data["rename"]), 201

		# If it is not a rename, then we can create the new company
		return c_post(company), 201


	# DELETE Method - /<string:company>
	def delete(self, company):
		c_initdb()
		# If it already exists, then that means we can try to delete it
		if (c_exists(company)):
			return c_delete(company), 200

		# Else we return that the company does not exist
		return c_message(company, company + " does not exist."), 400
