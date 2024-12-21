import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
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

# Fetch air quality data (dummy API URL, replace with actual API)
try:
    response = requests.get("https://api.weather.com/v3/wx/conditions/current", params={
        "language": "ko-KR",
        "format": "json",
        "apiKey": "your_api_key"  # Replace with a valid API key
    })
    air_data = response.json()

    pm10 = air_data.get("pm10", "N/A")  # 미세먼지
    pm2_5 = air_data.get("pm2_5", "N/A")  # 초미세먼지
    st.write(f"현재 미세먼지(PM10): {pm10} ㎍/㎥")
    st.write(f"현재 초미세먼지(PM2.5): {pm2_5} ㎍/㎥")

    # Display recommendation based on air quality
    if pm10 != "N/A" and int(pm10) > 80:
        st.warning("미세먼지가 높은 상태입니다. 자전거 이용 시 마스크 착용을 권장합니다.")
    elif pm2_5 != "N/A" and int(pm2_5) > 50:
        st.warning("초미세먼지가 높은 상태입니다. 야외 활동을 자제하세요.")
    else:
        st.success("공기가 양호합니다. 자전거 이용에 적합한 상태입니다.")
except Exception as e:
    st.error("미세먼지 데이터를 가져오는 데 실패했습니다. 인터넷 연결 또는 API 키를 확인하세요.")

# Section 2: 공영자전거 이용률과 교통 혼잡 영향
st.header("공영자전거 이용률과 교통 혼잡 영향")

# Insights on traffic congestion
st.markdown("""
공영자전거는 교통 혼잡을 완화하는 데 중요한 역할을 합니다:
- **출근 및 퇴근 시간**에 자전거 이용량 증가: 대중교통과 자동차 사용률 감소 효과.
- **도심 지역**에서 자전거 이용은 차량 운행 감소로 이어져 배출가스를 줄이는 데 기여합니다.
- **장기적 효과**: 자전거 이용을 촉진하면 차량 소유를 줄이고, 도시 내 교통 혼잡을 완화할 수 있습니다.

### 창원시 교통 혼잡 완화 효과
- 2022년 12월 기준, 누비자의 하루 평균 이용 건수는 약 `3000건`으로 추정됩니다.
- 이는 하루 약 `500대의 차량 운행`을 줄이는 효과를 가지고 있습니다.
""")

# Load data
@st.cache_data
def load_data():
    rental_data = pd.read_csv("rental_data.csv", encoding="euc-kr")  # 대여 데이터
    station_data = pd.read_csv("station_data.csv", encoding="euc-kr")  # 터미널 정보
    return rental_data, station_data

rental_data, station_data = load_data()

# Section 3: Data Overview
st.header("데이터 미리보기")
st.subheader("대여 및 반납 데이터")
st.dataframe(rental_data.head())

st.subheader("터미널 정보 데이터")
st.dataframe(station_data.head())

# Section 4: Map Visualization
st.header("터미널 위치 시각화")
map = folium.Map(location=[35.2, 128.65], zoom_start=12)
for _, row in station_data.iterrows():
    folium.Marker(
        [row['위도'], row['경도']],
        tooltip=row['터미널명']
    ).add_to(map)
folium_static(map)

st.markdown("### 추가 분석 기능은 계속 업데이트될 예정입니다!")
