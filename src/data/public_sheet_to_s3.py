import gspread, os.path, boto3, json
from datetime import datetime
from itertools import islice
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# need to create a .env file with these variables. ask thomas for key
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', '')
SHEET_ID = os.environ.get('SHEET_ID_2', '')
KEYFILE = os.environ.get('JSON_KEY', '')

# switch function to parse spaces out of category string
def switch(i):
    switcher = {
        "Arts":'arts',
        "Business": 'business',
        "Concert": "concert",
        "Farms/Farmers Markets": "farm",
        "Government": "gov",
        "Grocery Store": 'grocery',
        "Mall": "mall",
        "Pharmacy": "pharm",
        "Restaurant": "restaurant",
        "School (K-12)": "k12_school",
        "School (University/college)": "college",
        "Sports": "sports",
        "Volunteering": "volunteer",
        "Other": "other"
    }
    return switcher.get(i, "")

def location_switch(i):
    switcher = {
        "Twin Cities": 'tc',
        "Greater Minnesota": 'greater_mn',
        "Wisconsin": 'wisc'
    }
    return switcher.get(i, "")

# function to turn gsheet data to dictionary. row positions are hardcoded which is less than ideal
def sheet_to_json(obj, filename):
    cancel_json = []
    for row in islice(obj, 1, None):
        timestamp = row[0]
        name = row[1]
        location = location_switch(row[2])
        city = row[3]
        status = row[4]
        category = switch(row[5])
        url = row[6]
        description = row[7]
        publish = row[8]
        last_update = datetime.now().strftime("%b %d, %I:%M %p")

        if not row[0]:
            continue
        else:
            obj_props = {
                "timestamp": timestamp,
                "last_update": last_update,
                "event_name": name,
                "city": city,
                "location": location,
                "category": category,
                "status": status,
                "url": url,
                "desc": description,
                "publish": publish
            }
            cancel_json.append(obj_props)

    with open(filename, 'w') as f:
        json.dump(cancel_json, f)

    return

# hook up gspread credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scope)
gc = gspread.authorize(credentials)

# open sheet
sheet = gc.open_by_key(SHEET_ID).get_worksheet(0)
sheet_array = sheet.get_all_values()

sheet_to_json(sheet_array, './public_cancellations.json')

# push json to static
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3_path = 'news/projects/all/202003-cancellations/'
output = s3_path + 'public_cancellations.json'

s3.upload_file('./public_cancellations.json', AWS_S3_BUCKET, output)
