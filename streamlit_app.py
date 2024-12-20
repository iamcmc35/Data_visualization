import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium

# Title and description
st.title("누비자 데이터 분석 대시보드")
st.markdown("""
### 분석 목표
- 2022년 12월 데이터를 기반으로 누비자 대여 및 반납 패턴을 분석합니다.
- 시간대별 이용량, 터미널 간 이동 경로 등을 시각화합니다.
""")

# Load data
@st.cache
def load_data():
    rental_data = pd.read_csv("rental_data.csv")  # 현재 디렉토리에서 파일 로드
    station_data = pd.read_csv("station_data.csv")  # 현재 디렉토리에서 파일 로드
    return rental_data, station_data

rental_data, station_data = load_data()

# Data overview
st.header("데이터 미리보기")
st.subheader("대여 및 반납 데이터")
st.dataframe(rental_data.head())

st.subheader("터미널 정보 데이터")
st.dataframe(station_data.head())

# Time-based analysis
st.header("시간대별 이용량 분석")
hourly_counts = rental_data['대여시간(시)'].value_counts().sort_index()
st.bar_chart(hourly_counts)

# Map visualization
st.header("터미널 위치 시각화")
map = folium.Map(location=[35.2, 128.65], zoom_start=12)
for _, row in station_data.iterrows():
    folium.Marker(
        [row['위도'], row['경도']],
        tooltip=row['터미널명']
    ).add_to(map)
folium_static(map)

st.markdown("### 추가 분석 기능은 계속 업데이트될 예정입니다!")
