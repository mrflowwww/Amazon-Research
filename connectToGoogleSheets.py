import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('18fWcohv-U-SFsdJ8RWR8WKduoRrFmXPQxz89eoWE9vQ')
worksheet = sh.sheet1

res = worksheet.get_all_records()
print(res)
