from datetime import datetime
def date_to_str():
    today_date =str(datetime.now())
    today_date = today_date.replace(" ",'')
    today_date = today_date.replace("-",'')
    today_date = today_date.replace(":",'')
    today_date = today_date.replace(".",'')
    return today_date