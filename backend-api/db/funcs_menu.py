# funcs_menu.py

# imports packages needed
import sqlite3, json

def m_get(company):
	# Create a connection to the database
	connection = sqlite3.connect("database.db")
	cursor = connection.cursor()

	# Query to select the menu from the specific company
	menu_db = "SELECT * FROM " + company + "menu"
	menu_list = cursor.execute(menu_db)

	# Empty list to store a list of all the items in the menu
	menu_details = {}
	# Iterate through all the company details and store it in a company dictionary
	counter = 1
	for detail in menu_list:
		menu_details.update({detail[0]: detail[1]})
		counter += 1

	# Close the connection
	connection.close()

	# Return the list of company details we found
	return menu_details

def m_post():
	pass
