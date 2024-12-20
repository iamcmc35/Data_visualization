import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# Title and description
st.title("누비자 데이터 분석 대시보드")
st.markdown("2022년 12월 데이터를 활용한 터미널 이동 경로 및 이용 분석")

# Load data
rental_data = pd.read_csv("data/rental_data.csv")
station_data = pd.read_csv("data/station_data.csv")

# Data overview
st.header("데이터 미리보기")
st.dataframe(rental_data.head())

# Analysis Section
st.header("시간대별 이용량")
hourly_counts = rental_data['대여시간(시)'].value_counts().sort_index()
st.bar_chart(hourly_counts)

# Interactive map for terminals
st.header("터미널 이동 경로")
bicycle_id = st.selectbox("분석할 자전거를 선택하세요:", rental_data['자전거번호'].unique())
bicycle_data = rental_data[rental_data['자전거번호'] == bicycle_id]

map = folium.Map(location=[35.2, 128.65], zoom_start=12)
for _, row in bicycle_data.iterrows():
    folium.Marker(
        [row['출발위도'], row['출발경도']],
        tooltip=f"출발: {row['출발터미널명']}"
    ).add_to(map)
    folium.Marker(
        [row['도착위도'], row['도착경도']],
        tooltip=f"도착: {row['도착터미널명']}"
    ).add_to(map)
folium_static(map)
