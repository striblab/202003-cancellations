import gspread, os.path, boto3, json
from itertools import islice
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# need to create a .env file with these variables. ask thomas for key
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', '')
SHEET_ID = os.environ.get('SHEET_ID', '')
KEYFILE = os.environ.get('JSON_KEY', '')

# switch function to parse spaces out of category string
def switch(i):
    switcher = {
        "Arts":'arts',
        "Business": 'business',
        "Concert": "concert",
        "Free service": "free",
        "Government": "gov",
        "Religious": "religious",
        "Restaurant": "restaurant",
        "School (K-12)": "k12_school",
        "School (University/college)": "college",
        "Sports": "sports",
        "Other event": "other"
    }
    return switcher.get(i, "")

# function to turn gsheet data to dictionary. row positions are hardcoded which is less than ideal
def sheet_to_json(obj, filename):
    cancel_json = []
    for row in islice(obj, 2, None):
        timestamp = row[0]
        name = row[1]
        status = row[10]
        category = switch(row[2])
        end_date = row[3]
        city = row[4]
        description = row[5]
        cancel_date = row[6]
        venue = row[7]
        planned_time = row[8]
        planned_end_time = row[9]

        if not row:
            continue
        else:
            obj_props = {
                "timestamp": timestamp,
                "event_name": name,
                "category": category,
                "status": status,
                "city": city,
                "cancel_date": cancel_date,
                "planned_time": planned_time,
                "end_date": end_date,
                "planned_end_time": planned_end_time,
                "venue": venue,
                "desc": description
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
sheet = gc.open_by_key('1bVb5PvL8uWxOGD60luDFOLalWICwKkF9ycko5imsCjE').get_worksheet(0)
sheet_array = sheet.get_all_values()

sheet_to_json(sheet_array, './cancellations.json')

# push json to static
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3_path = 'news/projects/all/202003-cancellations/'
output = s3_path + 'cancellations.json'

s3.upload_file('./cancellations.json', AWS_S3_BUCKET, output)
