
from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji
def count_message(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    num_message=df.shape[0]
    words=[]
    for message in df["message"]:
        words.extend(message.split())
    
    extractor=URLExtract()
    url_count=[]
    for m in df["message"]:
        url_count.extend(extractor.find_urls(m))
        

    media= df[df["message"]=="<Media omitted>\n"].shape[0]
    return num_message,len(words),media,len(url_count)


def most_busy_user(df):
    df=df[df["user"]!="group_notification"]
    x=df["user"].value_counts().head()

    per=round(df["user"].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={"user":"percentage","index":"user"})
    return x,per


def create_word_cloud(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    df=df[df["user"]!="group_notification"]
    temp=df[df["message"]!="<Media omitted>\n"]

    words=[]
    for m in temp["message"]:
        words.extend(m.split())

    most_common_word=pd.DataFrame(Counter(words).most_common(20))  

    wc=WordCloud(width=500,height=500,background_color="white",min_font_size=10)
    words=wc.generate(temp["message"].str.cat(sep=" "))

 
    return words,most_common_word

def emoji_state(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    emojis=[]
    for msg in df["message"]:
        for c in msg:
            if c in emoji.UNICODE_EMOJI["en"]:
                emojis.extend(c)

    x=pd.DataFrame(Counter(emojis).most_common(20))

    return x 


def timeline_create(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    df["month_num"]=df["date"].dt.month
    timeline=df.groupby(["year","month_num","month"]).count()["message"].reset_index()
    time=[]
    for i in range(len(timeline)):
        time.append(timeline["month"][i]+"-"+str(timeline["year"][i]))
    
    timeline["time"]=time

    return timeline


def daily_timeline(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    df["day_"]=df["date"].dt.date
    day_timeline=df.groupby("day_").count()["message"].reset_index()
   

    return day_timeline



def week_active_map(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    active_day=df.groupby("day_name").count()["message"].reset_index()

    return active_day
def month_active_map(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]

    active_day=df.groupby("month").count()["message"].reset_index()

    return active_day

def activity_heatmap(selected_user,df):
    if selected_user!="overall":
        df= df[df["user"]==selected_user]
    hm=df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0) 
    return hm