import re
import pandas as pd
def data_prepocessing(data):
    pattern=r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w\w\s-\s"
    messages=re.split(pattern,data)[1:]

    pattern=r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w\w"
    dates=re.findall(pattern,data)

    df=pd.DataFrame({"date":dates,"user_and_message":messages})
    df["date"]=pd.to_datetime(df["date"])

    msg=[]
    user=[]
    for message in df['user_and_message']:
        entry=re.split(r"\w:\s",message)
        if entry[1:]:
            msg.append(entry[1])
            user.append(entry[0])
        else:
            user.append("group_notification")
            msg.append(entry[0])
    df["message"]=msg
    df["user"]=user
    df.drop(columns=["user_and_message"],inplace=True)
        
    df["year"]=df["date"].dt.year
    df["month"]=df["date"].dt.month_name()
    df["day"]=df["date"].dt.day
    df["day_name"]=df["date"].dt.day_name()
    df["minute"]=df["date"].dt.minute
    df["hour"]=df["date"].dt.hour
    period=[]
    for hour in df[["day_name","hour"]]["hour"]:
        if hour==23:
            period.append(str(hour)+ "-" +str("00"))
        elif hour==0:
            period.append("00"+ "-" +str(hour+1))
        else:
            period.append(str(hour)+ "-" +str(hour+1))
            
    df["period"]=period

    df=df[["date","user","message","month","day_name","day","year","hour","minute","period"]].copy()

    return df

