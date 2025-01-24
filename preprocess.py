import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    message  = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'Messages':message,'Dates':dates})
    df['Dates'] = pd.to_datetime(df['Dates'],format='%m/%d/%y, %H:%M %p - ')
    user_Name = []
    messages = []

    for message in df.Messages:
       piece = re.split("([\w\W]+?):\s",message)
       if piece[1:]:
           user_Name.append(piece[1])
           messages.append(piece[2])
       else:
         user_Name.append('group_notification')
         messages.append(piece[0])
    df['User_name'] = user_Name
    df['Messages'] = messages
    
    df['Year'] = df['Dates'].dt.year
    df['only_date'] = df['Dates'].dt.date
    df['Month'] = df['Dates'].dt.month_name()
    df['Month_Num'] = df['Dates'].dt.month
    df['Days'] = df['Dates'].dt.day
    df['day_name'] = df['Dates'].dt.day_name()
    df['Hour'] = df['Dates'].dt.hour
    df['Minute'] = df['Dates'].dt.minute
    df = df.drop("Dates",axis=1)
    return df



