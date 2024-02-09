import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# Sample DataFrame
df = pd.read_csv('./DataScraping_and_processing/karthik_cleaned_data.csv')
df.dropna(inplace=True)
df['airline_name'] = df['airline_name'].str.lower()

# Sidebar Filters
st.sidebar.header("Filters")
airline = st.sidebar.selectbox("Airline", options=pd.unique(df['airline_name']))
sentiment = st.sidebar.selectbox("Sentiment", options=["All", "Promoter 😁", "Detractor 🤬", "Neutral 😐"])
start_date, end_date = st.sidebar.select_slider("Select Date Range", options=pd.unique(df['review_date']), value=(df['review_date'].min(), df['review_date'].max()))

# Filter data based on selections
filtered_data = df[(df['airline_name'] == airline) | (airline == "All")]
filtered_data = filtered_data[(filtered_data['NPS_category'] == sentiment) | (sentiment == "All")]
filtered_data = filtered_data[(filtered_data['review_date'] >= start_date) & (filtered_data['review_date'] <= end_date)]

# 2 by 2 layout of charts
# donut chart on the top right and word cloud on the bottom right
st.title("Airline Reviews Dashboard")
st.subheader("Sentiment Analysis")
fig, ax = plt.subplots(1, 2, figsize=(20, 10))
filtered_data['NPS_category'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax[0])
ax[0].set_title("Sentiment Distribution")
ax[0].set_ylabel("")
ax[0].set_xlabel("")
ax[0].legend()
wordcloud = WordCloud(width=800, height=400).generate(" ".join(filtered_data['clean_text']))
ax[1].imshow(wordcloud, interpolation='bilinear')
ax[1].set_title("Word Cloud")
ax[1].axis('off')
st.pyplot(fig)
