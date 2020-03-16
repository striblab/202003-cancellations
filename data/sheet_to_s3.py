import gspread, os.path, boto3, json
from itertools import islice
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', '')
SHEET_ID = os.environ.get('SHEET_ID', '')
KEYFILE = os.environ.get('JSON_KEY', '')

def sheet_to_json(obj, filename):
    bday_json = []
    for row in islice(obj, 1, None):
        name = row[0]
        greeting = row[2]
        publish = row[3]

        if not row or not greeting or not publish:
            continue
        else:
            obj_props = {
                "name": name,
                "greeting": greeting,
                "publish": publish
            }

            bday_json.append(obj_props)

    with open(filename, 'w') as f:
        json.dump(bday_json, f)

    return

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scope)
gc = gspread.authorize(credentials)

sheet = gc.open_by_key('1bVb5PvL8uWxOGD60luDFOLalWICwKkF9ycko5imsCjE').get_worksheet(0)
sheet_array = sheet.get_all_values()

print(sheet_array)

# sheet_to_json(sheet_array, './birthday.json')

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# )
#
# s3_path = 'news/projects/all/20200315-sid-birthday/sid-greetings/'
# output = s3_path + 'birthday.json'
#
# s3.upload_file('./birthday.json', AWS_S3_BUCKET, output)
