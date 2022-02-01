import streamlit as sl
import prepocessing
import helper
import matplotlib.pyplot as plt
import seaborn as sns 

sl.sidebar.title("Whatsapp message analysis")

upload_file=sl.sidebar.file_uploader("Choose a file")

if upload_file is not None:
    byte_data=upload_file.getvalue()
    data=byte_data.decode("utf-8")
    df=prepocessing.data_prepocessing(data)


    user_list=df["user"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"overall")
    select_user=sl.sidebar.selectbox("Show analysis with right person",user_list)
    
    if sl.sidebar.button("Show Analysis"):
        num_message,words,media,url_count=helper.count_message(select_user,df)
       
        col1,col2,col3,col4=sl.columns(4)
       
        with col1:
            sl.header("Total Message")
            sl.title(num_message)
        with col2:
            sl.header("Total Words")
            sl.title(words)

        with col3:
            sl.header("Media Shared")
            sl.title(media)

        
        with col4:
            sl.header("Link Shared")
            sl.title(url_count)

        
    
    
    if select_user=="overall":
        sl.title("Most Active User")
        x,percantage=helper.most_busy_user(df)
        fig,ax=plt.subplots()
       
        plt.xticks(rotation=15)

        col1,col2=sl.columns(2)
        with col1:
            ax.bar(x.index,x.values)
            sl.pyplot(fig)
        
        with col2:
            sl.dataframe(percantage)

    col1,col2=sl.columns(2)
    with col1:  
        most_active_day=helper.week_active_map(select_user,df)

        fig,ax=plt.subplots()
        ax.bar(most_active_day["day_name"],most_active_day["message"],color="g")
    
        sl.title("Weekly Activies")
        plt.xticks(rotation=90)
        sl.pyplot(fig)
    with col2:  
        month_active=helper.month_active_map(select_user,df)

        fig,ax=plt.subplots()
        ax.bar(month_active["month"],month_active["message"],color="yellow")
        plt.xticks(rotation=90)
        sl.title("Monthly Activies")
        sl.pyplot(fig)

    sl.title("Weekly Activity Map")
    heatmap_day=helper.activity_heatmap(select_user,df)
    fig,ax=plt.subplots()
    ax=sns.heatmap(heatmap_day)
    sl.pyplot(fig)

    
    # word cloud
    wc_df,most_common_message=helper.create_word_cloud(select_user,df)
    fig,ax=plt.subplots()
    sl.title("Word Cloud")
    ax.imshow(wc_df)
    sl.pyplot(fig)

    # most common user
    sl.title("most common Words")
    fig,ax=plt.subplots()
    ax.barh(most_common_message[0],most_common_message[1])
    plt.xticks(rotation=90)
    sl.pyplot(fig)

    # emoji anlysis
    emoji_df=helper.emoji_state(select_user,df)
    sl.title("Emoji Analysis")
    col1,col2=sl.columns(2)

    with col1:
       sl.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        sl.pyplot(fig)

    
    timeline=helper.timeline_create(select_user,df)

    fig,ax=plt.subplots()
    ax.plot(timeline["time"],timeline["message"],color="g")
    ax.scatter(timeline["time"],timeline["message"])
    plt.xticks(rotation=90)
    sl.title("Monthly TimeLine")
    sl.pyplot(fig)
    

    day_timeline=helper.daily_timeline(select_user,df)

    fig,ax=plt.subplots()
    ax.plot(day_timeline["day_"],day_timeline["message"],color="g")
    ax.scatter(day_timeline["day_"],day_timeline["message"])
    plt.xticks(rotation=90)
    sl.title("Daily TimeLine")
    sl.pyplot(fig)


