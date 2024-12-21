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

# Section 2: 공영자전거 이용률과 교통 혼잡 영향
st.header("공영자전거 이용률과 교통 혼잡 영향")
st.markdown("""
공영자전거는 교통 혼잡을 완화하는 데 중요한 역할을 합니다:
- **출근 및 퇴근 시간**에 자전거 이용량 증가: 대중교통과 자동차 사용률 감소 효과.
- **도심 지역**에서 자전거 이용은 차량 운행 감소로 이어져 배출가스를 줄이는 데 기여합니다.
- **장기적 효과**: 자전거 이용을 촉진하면 차량 소유를 줄이고, 도시 내 교통 혼잡을 완화할 수 있습니다.
""")

# Load data
@st.cache_data
def load_data():
    rental_data = pd.read_csv("rental_data.csv", encoding="euc-kr")
    station_data = pd.read_csv("station_data.csv", encoding="euc-kr")
    return rental_data, station_data

rental_data, station_data = load_data()

# Section 3: 터미널별 대여 및 반납 건수 분석
st.header("터미널별 대여 및 반납 건수 분석")
rental_counts = rental_data['출발터미널'].value_counts()
return_counts = rental_data['도착터미널'].value_counts()
terminal_usage = pd.DataFrame({
    "대여건수": rental_counts,
    "반납건수": return_counts
}).fillna(0)
st.bar_chart(terminal_usage)

# Section 4: 터미널 간 이동 경로 히트맵
st.header("터미널 간 이동 경로 히트맵")
movement_matrix = rental_data.pivot_table(
    index='출발터미널', columns='도착터미널', aggfunc='size', fill_value=0
)
plt.figure(figsize=(12, 8))
sns.heatmap(movement_matrix, cmap="Blues", square=True)
st.pyplot(plt)

# Section 5: 날짜별 이용량 변화 추세
st.header("날짜별 이용량 변화 추세")
rental_data['대여일'] = pd.to_datetime(rental_data['출발일'], errors='coerce')
daily_counts = rental_data['대여일'].value_counts().sort_index()
st.line_chart(daily_counts)

# Section 6: 터미널 위치 시각화
st.header("터미널 위치 시각화")
map = folium.Map(location=[35.2, 128.65], zoom_start=12)
for _, row in station_data.iterrows():
    folium.Marker(
        [row['위도'], row['경도']],
        tooltip=row['터미널명']
    ).add_to(map)
folium_static(map)

st.markdown("### 추가 분석 기능은 계속 업데이트될 예정입니다!")
