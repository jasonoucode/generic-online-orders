# funcs_company.py

# imports packages needed
import sqlite3, json

# Initializes the companies db
def c_initdb():
	# Create a connection to the databaseconnection = sqlite3.connect("database.db")
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Create a companies table if it does not already exist as we need it to
	#		keep track of the list of all of our companies
	create_companies_table = "CREATE TABLE IF NOT EXISTS companies (name text, unique(name))"
	cursor.execute(create_companies_table)

	# Because we are doing a table altering function, we must commit our changes first
	#		before we close connection.
	connection.commit()
	connection.close()


# Used to see if a company exists
def c_exists(company):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Query to check if the company we want exists in the databse
	check_exists = "SELECT * FROM companies WHERE name=? LIMIT 1"
	company_found = cursor.execute(check_exists, (company,))

	# Changes the query results into a dictionary
	companylist = {}
	for item in company_found:
		companylist.update({item[0]: item[0]})

	# Close the connection
	connection.close()

	# If company_found is empty return false, else return true
	if not companylist:
		return False
	return True


# Gets the entire list of all companies in the database
def c_getall():
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Empty list to store a list of all the companies
	companies = {}
	# Query to select all companies and store the query to be iterated through
	companies_db = "SELECT * FROM companies"
	companies_list = cursor.execute(companies_db)

	# Iterate through all the companies and stores it in a companies dictionary
	# lists the companies in order as well using a counter to label which companies
	#		come first.
	counter = 1
	for company in companies_list:
		companies.update({counter: company[0]})
		counter += 1

	# Close the connection
	connection.close()

	# Return the list of companies we found
	return companies


# Gets the list of all the databases under a specific company
def c_get(company):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Query to select all details from the specific company
	company_db = "SELECT * FROM " + company
	company_list = cursor.execute(company_db)

	# Empty list to store a list of all the company details
	company_details = {}
	# Iterate through all the company details and store it in a company dictionary
	counter = 1
	for detail in company_list:
		company_details.update({counter: detail[0]})
		counter += 1

	# Close the connection
	connection.close()

	# Return the list of company details we found
	return company_details


# Creates a new company database
def c_post(company):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Creates a table for the single company as we need it to keep track of all
	#		other database tables associated with this company
	create_company_table = "CREATE TABLE IF NOT EXISTS " + company + " (name text, unique(name))"
	cursor.execute(create_company_table)

	# Creates a menu table for the company
	create_companymenu_table = "CREATE TABLE " + company + "menu (name text, price real, unique(name))"
	cursor.execute(create_companymenu_table)

	# Creates an orders table for the company
	create_companyorders_table = "CREATE TABLE " + company + "orders (name text, price real, unique(name))"
	cursor.execute(create_companyorders_table)

	# Add the new tables into the company table to keep track of all the tables associated with that company
	add_menu = "INSERT INTO " + company + " (name) VALUES ('" + company + "menu')"
	cursor.execute(add_menu)
	add_orders = "INSERT INTO " + company + " (name) VALUES ('" + company + "orders')"
	cursor.execute(add_orders)

	# We then insert into the companies table the new company that we have added to our
	#		system/db. This way we can keep track of the list of all the companies under our
	#		system.
	add_new_companies = "INSERT INTO companies (name) VALUES (?)"
	cursor.execute(add_new_companies, (company,))

	# Because we are doing a table altering function, we must commit our changes first
	#		before we close connection.
	connection.commit()
	connection.close()

	# We then return the message saying the company has been created
	return c_message(company, company + " has been created.")


# Renames the name of an existing company
def c_rename(name, rename):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# rename the company inside of companies
	alter_companies = "UPDATE companies SET name=? WHERE name=?"
	cursor.execute(alter_companies, (rename, name))

	# rename the tables inside of the company table
	alter_company_menu = "UPDATE " + name + " SET name=? WHERE name=?"
	re_menu = rename + "menu"
	menu = name + "menu"
	cursor.execute(alter_company_menu, (re_menu, menu))

	re_orders = rename + "orders"
	orders = name + "orders"
	alter_company_orders = "UPDATE " + name + " SET name=? WHERE name=?"
	cursor.execute(alter_company_orders, (re_orders, orders))

	# rename the company table
	alter_company = "ALTER TABLE " + name + " RENAME TO " + rename
	cursor.execute(alter_company)

	# rename the company menu table
	alter_menu = "ALTER TABLE " + name + "menu RENAME TO " + rename + "menu"
	cursor.execute(alter_menu)

	# rename the company orders table
	alter_orders = "ALTER TABLE " + name + "orders RENAME TO " + rename + "orders"
	cursor.execute(alter_orders)

	# Because we are doing a table alter function, we must commit our changes first
	#		before we close connection.
	connection.commit()
	connection.close()

	# We then return the message saying the company has been renamed.
	return c_message(rename, name + " has been renamed to " + rename + ".")


# Delete the company specified
def c_delete(company):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Query used to drop tables associated with that company
	# COMPANY MENU
	delete_company_menu = "DROP TABLE " + company + "menu"
	cursor.execute(delete_company_menu)
	#COMPANY ORDERS
	delete_company_orders = "DROP TABLE " + company + "orders"
	cursor.execute(delete_company_orders)

	# Query used to drop the specified company table
	delete_company_table = "DROP TABLE " + company
	cursor.execute(delete_company_table)

	# Query used to remove the speicified company from our list of existing companies
	delete_companies_table = "DELETE FROM companies WHERE name=?"
	cursor.execute(delete_companies_table, (company,))

	# Because we are doing a table altering function, we must commit our changes first
	#		before we close connection.
	connection.commit()
	connection.close()

	# We then return the message saying the company has been deleted
	return c_message(company, company + " has been deleted.")


# Returns a message for the user in the form of a dictionary
def c_message(key, value):
	return {key: value}
