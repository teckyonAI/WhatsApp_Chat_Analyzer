from os import sep

from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stat(selected_user,df):
    if selected_user != 'Complete Chat Analysis':
        df =df[df['User_name'] == selected_user ]
        
    data=df[df.User_name == "group_notification"]
    df = df.drop(data.index)   
        # Fetch the Number of all messages
    number_of_messages = df.shape[0]
        # Fetch the Number of words
    words = []
    for message in df.Messages:
         words.extend(message.split())
    
    # fetching the Number of media messages
    number_of_media_messages = df[df["Messages"]=='<Media omitted>\n'].shape[0]
   # fetching the  number of URL
    
    extractor = URLExtract()
    url = []
    for message in df["Messages"]:
       url.extend(extractor.find_urls(message))

         
    # fetching the NUMBER OF days
    days = len(df['Days'].unique())
    # Fetching the number of months 
    months =len(df['Month'].unique())
    # Fetching the number of years
    years = len(df['Year'].unique())
    #fetching the number of members
    members = len(df['User_name'].unique())
    # fetching the name of members
    name_of_members = df['User_name'].unique().tolist()
    name_of_members = pd.DataFrame(name_of_members).rename(columns={0:'Members',})

    
    return number_of_messages,len(words),number_of_media_messages,url,days,months,years,members,name_of_members
    

def yearly_messages(selected_user,selected_year,df):
    
    
    if selected_user == 'Complete Chat Analysis':
        df =df[(df["Year"] == selected_year)]
        df = df.drop(['Month','Days','Hour','Minute'],axis=1)
        data=df[df.User_name == "group_notification"]
        df = df.drop(data.index)
        return df
    elif selected_user != 'Complete Chat Analysis':
        df = df[(df["Year"] == selected_year) & (df["User_name"] == selected_user)]
        df = df.drop(['Month','Days','Hour','Minute'],axis=1)
        data=df[df.User_name == "group_notification"]
        df = df.drop(data.index)
        return df

def monthly_messages(selected_user,selected_month,df):
    
    
    if selected_user == 'Complete Chat Analysis':
        df =df[(df["Month"] == selected_month)]
        df = df.drop(['Year','Days','Hour','Minute'],axis=1)
        data=df[df.User_name == "group_notification"]
        df = df.drop(data.index)
        return df
    elif selected_user != 'Complete Chat Analysis':
        df = df[(df["Month"] == selected_month) & (df["User_name"] == selected_user)]
        df = df.drop(['Year','Days','Hour','Minute'],axis=1)
        data=df[df.User_name == "group_notification"]
        df = df.drop(data.index)
        return df
def busy_user(df):
    dat=df[df.User_name == "group_notification"]
    df = df.drop(dat.index)
    data = df['User_name'].value_counts().head(5)

    percent = round((df['User_name'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Members','User_name':'Percentage(%)'})
    return data,percent

def create_wordcloud(selected_user,df):

    f=open('stop_hinglish.txt','r')
    stopwords = f.read()

    if selected_user != 'Complete Chat Analysis':
        df =df[df['User_name'] == selected_user ]
    
    temp = df[df['User_name'] != 'group_notification' ]
    temp = temp[temp['Messages'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
         y=[]
         for word in message.lower().split():
             if word not in stopwords:
                 y.append(word)
         return " ".join(y)

        
               

    
    wc = WordCloud(width=400,height=400,min_font_size=10,background_color='black')
    temp["Messages"] = temp['Messages'].apply(remove_stop_words)
    data_word_cloud = wc.generate(temp["Messages"].str.cat(sep=' '))
    return data_word_cloud

def most_common_words(selected_user,df):

    f=open('stop_hinglish.txt','r')
    stopwords = f.read()

    if selected_user != 'Complete Chat Analysis':
        df =df[df['User_name'] == selected_user ]
    
    temp = df[df['User_name'] != 'group_notification' ]
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    words=[]

    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)

    
    return_df = pd.DataFrame(Counter(words).most_common(20))
    return  return_df


def total_emoji(selected_user,df):
    if selected_user != 'Complete Chat Analysis':
        df = df[df['User_name'] == selected_user]

    emojis = []
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Complete Chat Analysis':
        df = df[df['User_name'] == selected_user]

    timeline = df.groupby(['Year', 'Month_Num', 'Month']).count()['Messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Complete Chat Analysis':
        df = df[df['User_name'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Complete Chat Analysis':
        df = df[df['User_name'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Complete Chat Analysis':
        df = df[df['User_name'] == selected_user]

    return df['Month'].value_counts()

