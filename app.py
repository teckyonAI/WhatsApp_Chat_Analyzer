
import streamlit as slt
import wordcloud
import preprocess
import helper
import matplotlib.pyplot as plt
slt.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = slt.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocess.preprocess(data)
    

    # Fetch user name
    user_list = df['User_name'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Complete Chat Analysis")

    selected_user =  slt.sidebar.selectbox("User Names",user_list)
    if slt.sidebar.button("Analysis Statistics"):
        with slt.spinner("Processing data..."):
            slt.title("Top Statistics")
            number_of_messages,words,number_of_media_messages,url,days,months,years,members,name_of_members = helper.fetch_stat(selected_user,df)
            
            colu1,colu2,colu3,colu4 = slt.columns(4)
            
            with colu1:
                slt.header("Toltal Days:")
                slt.title(days)
            with colu2:
                slt.header("Total Months:")
                slt.title(months)
            with colu3:
                slt.header("Total Years:")
                slt.title(years)
            with colu4:
                slt.header("Total members:")
                slt.title(members)
            
            
            slt.write(":heavy_minus_sign:" * 50)
            col1,col2,col3 = slt.columns(3)
            

            with col1:
                slt.header("Total Messages:")
                slt.title(number_of_messages)
            with col2:
                slt.header("Total Words:")
                slt.title(words)
            with col3:
                slt.header("Media Messages:")
                slt.title(number_of_media_messages)
            slt.write(":heavy_minus_sign:" * 50)
            colum1,colum2 = slt.columns(2)
            with colum1:
                slt.header("URL Shared:")
                slt.title(len(url))
                slt.dataframe(url)
            with colum2:
                slt.header("ALL Members")
                slt.title(members)
                slt.dataframe(name_of_members)
            slt.write(":heavy_minus_sign:" * 50)
             # monthly timeline
            slt.title("Monthly Timeline of Messages")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['Messages'],color='green')
            plt.xticks(rotation='vertical')
            slt.pyplot(fig)
            slt.write(":heavy_minus_sign:" * 50)
            # daily timeline
            slt.title("Daily Timeline of Messages")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['Messages'], color='black')
            plt.xticks(rotation='vertical')
            slt.pyplot(fig)
            slt.write(":heavy_minus_sign:" * 50)
             
             # activity map
            slt.title('Activity Map')
            col1,col2 = slt.columns(2)

            with col1:
               slt.header("Most busy day")
               busy_day = helper.week_activity_map(selected_user,df)
               fig,ax = plt.subplots()
               ax.bar(busy_day.index,busy_day.values,color='purple')
               plt.xticks(rotation='vertical')
               slt.pyplot(fig)

            with col2:
               slt.header("Most busy month")
               busy_month = helper.month_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values,color='orange')
               plt.xticks(rotation='vertical')
               slt.pyplot(fig)

            
        # Find the busiest person
            if selected_user == "Complete Chat Analysis":
                slt.write(":heavy_minus_sign:" * 50)
                slt.title("Most Active Memebers")
                x,percent = helper.busy_user(df)
                fig,ax = plt.subplots()
                col1,col2 = slt.columns(2)
                with col1:
                    ax.bar(x.index,x.values )
                    plt.xticks(rotation ='vertical' )
                    slt.pyplot(fig)
                with col2:
                    slt.header("Percentages(%)")
                    slt.dataframe(percent)
            slt.write(":heavy_minus_sign:" * 50)
            
            # Word Cloud
            slt.title("Wordcloud of All Messages")
            dat_wordcloud = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(dat_wordcloud)
            slt.pyplot(fig)
            slt.write(":heavy_minus_sign:" * 50)   
        # Most Common Words
            slt.title("Most Common Words in Messages")
            most_common_df = helper.most_common_words(selected_user,df)
            fig,ax = plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation ='vertical' )
            slt.pyplot(fig)
            slt.write(":heavy_minus_sign:" * 50)  
        # emoji analysis
        emoji_df = helper.total_emoji(selected_user,df)
        slt.title("Emoji Analysis")

        coli1,coli2 = slt.columns(2)

        with coli1:
            slt.dataframe(emoji_df)
        with coli2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            slt.pyplot(fig)
             
             
                

               
        
        slt.write(":heavy_minus_sign:" * 50)        
    


# new button Anlysis Messages start 
    if slt.sidebar.checkbox("Analysis Messages"):
        with slt.spinner("Processing data..."):     
            # Fetch years
            year_list = df['Year'].unique().tolist()
            #year_list.remove("group_notification")
            year_list.sort()
            slt.header(" Select Year")
            selected_year = slt.selectbox("Years",year_list)
            if selected_year is not None:
                selected_month=1
                data =helper.yearly_messages(selected_user,selected_year,df)
                slt.dataframe(data)


            slt.write(":heavy_minus_sign:" * 50) 
            # Fetch Months
            month_list = df['Month'].unique().tolist()
            month_list.sort()
            slt.header(" Select Month")
            selected_month = slt.selectbox("Months",month_list)
            if selected_year is not None:
                data =helper.monthly_messages(selected_user,selected_month,df)
                slt.dataframe(data)     

             
            
         
