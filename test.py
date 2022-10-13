from connect_to_sheets import Sheets

sheets = Sheets()

df = sheets.get_df_data()
columns = ['Cityprice', 'Req1 Units', 
                    'Req2 Units', 'Req3 Units']

print(df.info())