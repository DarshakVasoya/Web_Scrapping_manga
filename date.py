
from datetime import datetime
from datetime import date

# parcing the date
def parse_date(date_str, format_str='%m/%d/%Y'):
    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError as e:
        # Get today's date
        today = date.today()
        return datetime.strptime(today, format_str).date()
   
try:
    print(parse_date("06/20/2024798jkhkj"))
except:
    print("error")
    today = date.today()
    print(today)