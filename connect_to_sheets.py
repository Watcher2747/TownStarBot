import os
import gspread
import pandas as pd
from google.oauth2 import service_account
import json

my_secret = json.loads(os.environ['google_json'])

class Sheets:

  def __init__(self):
    pass

  def save_df_locally(self):

    #credentials to the account
    credentials = service_account.Credentials.from_service_account_info(
      my_secret)
    scope = [
      'https://spreadsheets.google.com/feeds',
      'https://www.googleapis.com/auth/drive'
    ]
    creds = credentials.with_scopes(scope)
    # authorize the clientsheet
    client = gspread.authorize(creds)

    sheet = client.open('Town Star Goods Breakdown')
    sheet_instance = sheet.get_worksheet(0)
    sheet_records = sheet_instance.get()

    df = pd.DataFrame.from_dict(sheet_records)
    # view the top records

    df.columns = df.iloc[0]
    df = df[1:]

    df.to_csv('df_original.csv', index=False)

  def get_df_data(self):
    df = pd.read_csv('df_original.csv')
    return df
