import gspread
gc=gspread.service_account(filename='creds.json')
sh=gc.open('database').sheet1
#sh.resize(1)
#sh.update('A2','test')
sh.append_row(['a','b'])
print(len(sh.get_all_values()))