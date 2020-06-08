import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from flask import *
from functools import wraps
import sqlite3



app = Flask(__name__)

@app.route('/home/')
def home():
	return render_template('index.html')


@app.route('/resources/', methods=['GET', 'POST'])
def resources():
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('blmdata.json', scope)
	client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	sheet = client.open("Resources").sheet1

	# Extract and print all of the values
	list_of_hashes = sheet.get_all_records()

	df = pd.DataFrame.from_dict(list_of_hashes)
	

	if request.method == 'GET':
		pd.set_option('display.max_colwidth', 1)
		return render_template('resources.html',  tables=[df.to_html()])

	if request.method == 'POST':
		print("POST")
		filters = request.form.getlist('filters')
		results = df.loc[df['Type'].isin(filters)]
		return render_template('resources.html', tables=[results.to_html()])
	


@app.route('/volunteer/')
def volunteer():
	return render_template('volunteer.html')

@app.route('/aboutus/')
def aboutus():
	return render_template('aboutus.html')

# @app.route('/faq/')
# def volunteer():
# 	return render_template('faq.html')

if __name__ == "__main__":
	app.run()


