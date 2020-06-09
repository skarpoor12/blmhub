import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from apiclient.discovery import build

from flask import *
from functools import wraps
import sqlite3




app = Flask(__name__)

@app.route('/home/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('blmvolunteer.json', scope)
		client = gspread.authorize(creds)
		service = build('sheets', 'v4', credentials=creds)
		sheet = service.spreadsheets()

		data = request.form.getlist('data')

		data_new = []

		for i in data:
			data_new.append([i])

		body = {
			"majorDimension": 'COLUMNS',
			"values": data_new
		}

		spreadsheetId = "1irAr74XtTMnrjuC3UVK-XIDtbjPDllJZypDgjOXE4go"
		range = "Sheet1!A:F";
		sheet.values().append(
			spreadsheetId=spreadsheetId,
			range=range,
			body=body,
			valueInputOption="USER_ENTERED"
		).execute()

	return render_template('index.html')

@app.route('/learn/')
def learn():
	return render_template('learn.html')


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
	def make_clickable(link):
	    # target _blank to open new window
	    # extract clickable text to display for your link

	    return f'<a href="{link}" style="color: #272725">Go To This Resource</a>'

	
	df['Links'] = df['Links'].apply(make_clickable)

	if request.method == 'GET':
		
		return render_template('resources.html',  tables=[df.to_html(escape=False)])

	if request.method == 'POST':
		filters = request.form.getlist('filters')
		results = df.loc[df['Type'].isin(filters)]
		return render_template('resources.html', tables=[results.to_html(escape=False)])
	


@app.route('/volunteer/', methods=['GET', 'POST'])
def volunteer():
	if request.method == 'POST':

		#open google sheets
		scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		creds = ServiceAccountCredentials.from_json_keyfile_name('blmvolunteer.json', scope)
		client = gspread.authorize(creds)
		service = build('sheets', 'v4', credentials=creds)
		sheet = service.spreadsheets()

		data = request.form.getlist('data')

		data_new = []

		for i in data:
			data_new.append([i])


		body = {
		  "majorDimension": 'COLUMNS',
		  "values": data_new
		}


		spreadsheetId = "1aCSRz0nTQ8o8SsaYvZs-hvDjHj7WVhC2GXhhCXSW--Q"
		range = "Sheet1!A:E";
		sheet.values().append(
		  spreadsheetId=spreadsheetId,
		  range=range,
		  body=body,
		  valueInputOption="USER_ENTERED"
		).execute()
				

	return render_template('volunteer.html')



@app.route('/aboutus/')
def aboutus():
	return render_template('aboutus.html')

# @app.route('/faq/')
# def volunteer():
# 	return render_template('faq.html')

if __name__ == "__main__":
	app.run()


