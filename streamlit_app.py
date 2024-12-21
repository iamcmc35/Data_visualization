import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import folium_static
import folium
import plotly.graph_objects as go
import requests

# Title and description
st.title("누비자 데이터 분석 및 환경 영향 대시보드")
st.markdown("""
### 분석 목표
- 창원시 미세먼지 현황과 공영자전거 이용의 교통 혼잡 완화 효과를 분석합니다.
- 2022년 12월 데이터를 기반으로 누비자 대여 및 반납 패턴을 시각화합니다.
""")

# Section 1: 창원시 미세먼지 현황
st.header("창원시 미세먼지 현황")
try:
    # Example data for air quality (replace with actual API response)
    pm10 = 75  # PM10 예시 값
    pm2_5 = 45  # PM2.5 예시 값

    # Gauge Chart for PM10
    st.subheader("미세먼지 (PM10)")
    fig_pm10 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pm10,
        title={'text': "PM10 농도 (㎍/㎥)"},
        gauge={
            'axis': {'range': [0, 150]},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 80], 'color': "yellow"},
                {'range': [80, 150], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    st.plotly_chart(fig_pm10)

    # Gauge Chart for PM2.5
    st.subheader("초미세먼지 (PM2.5)")
    fig_pm2_5 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pm2_5,
        title={'text': "PM2.5 농도 (㎍/㎥)"},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 15], 'color': "green"},
                {'range': [15, 35], 'color': "yellow"},
                {'range': [35, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 35
            }
        }
    ))
    st.plotly_chart(fig_pm2_5)

except Exception as e:
    st.error("미세먼지 데이터를 가져오는 데 실패했습니다. 인터넷 연결 또는 API 키를 확인하세요.")

# Load data
@st.cache_data
def load_data():
    rental_data = pd.read_csv("rental_data.csv", encoding="euc-kr")
    station_data = pd.read_csv("station_data.csv", encoding="euc-kr")
    return rental_data, station_data

rental_data, station_data = load_data()

# Ensure '대여일' column exists
if '출발일' in rental_data.columns:
    rental_data['대여일'] = pd.to_datetime(rental_data['출발일'], errors='coerce')
else:
    st.error("데이터에 '출발일' 열이 없습니다. CSV 파일을 확인하세요.")

# Section 2: 시간대별 자전거 대여량 분석
st.header("시간대별 자전거 대여량 분석")
rental_data['대여시간'] = pd.to_datetime(rental_data['출발시간'], errors='coerce').dt.hour
hourly_counts = rental_data['대여시간'].value_counts().sort_index()

# Plot hourly rental counts
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(hourly_counts.index, hourly_counts.values, color='skyblue')
ax.set_title("시간대별 자전거 대여량", fontsize=16)
ax.set_xlabel("시간대 (시)", fontsize=12)
ax.set_ylabel("대여량 (건수)", fontsize=12)
st.pyplot(fig)

# Section 3: 공영자전거 이용률에 따른 차량 대체 효과
st.header("공영자전거 이용률에 따른 차량 대체 효과")
average_daily_rentals = rental_data['대여일'].nunique()  # 하루 평균 대여 건수 계산
car_replacement_rate = 0.2  # 자전거 1대당 대체되는 차량 비율 (예: 20%)
estimated_car_reduction = average_daily_rentals * car_replacement_rate

# Display results
st.write(f"공영자전거를 통해 하루 약 {estimated_car_reduction:.0f}대의 차량 운행이 감소합니다.")

# Visualization
fig, ax = plt.subplots(figsize=(8, 6))
categories = ['대여된 자전거', '대체된 차량']
values = [average_daily_rentals, estimated_car_reduction]
ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'orange'])
ax.set_title("공영자전거 이용에 따른 차량 대체 효과")
st.pyplot(fig)

# Section 4: 터미널별 대여량 히트맵
st.header("터미널별 대여량 히트맵")
rental_counts = rental_data['출발터미널'].value_counts()

# Merge with station data to get coordinates
terminal_data = pd.merge(
    rental_counts.reset_index(),
    station_data[['터미널번호', '위도', '경도']],
    left_on='index',
    right_on='터미널번호',
    how='left'
)

# Create map with heatmap
map = folium.Map(location=[35.2, 128.65], zoom_start=12)
for _, row in terminal_data.iterrows():
    folium.Circle(
        location=[row['위도'], row['경도']],
        radius=row['출발터미널'] * 10,  # Adjust size based on rental counts
        color='blue',
        fill=True,
        fill_opacity=0.6
    ).add_to(map)
folium_static(map)
