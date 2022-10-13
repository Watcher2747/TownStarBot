import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

my_secret = os.environ['google_json']


class Sheets:

  def __init__(self):
    pass

  def save_df_locally(self):
    # defining the scope of the application
    scope_app = [
      'https://spreadsheets.google.com/feeds',
      'https://www.googleapis.com/auth/drive'
    ]
    #credentials to the account
    cred = ServiceAccountCredentials.from_json_keyfile_name(
      my_secret, scope_app)
    # authorize the clientsheet
    client = gspread.authorize(cred)

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


print(my_secret)
