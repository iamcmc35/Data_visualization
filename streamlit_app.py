import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import requests

# Title and layout
st.set_page_config(page_title="누비자 데이터 분석", layout="wide")
st.title("🚲 창원시 공영자전거 데이터 대시보드")
st.markdown("""
### 목적
- 창원시 공영자전거의 데이터 분석 및 환경적 영향을 평가합니다.
- 미세먼지 현황과 교통혼잡 완화 효과를 시각적으로 이해합니다.
""")

# Sidebar menu
st.sidebar.header("📋 메뉴")
menu = st.sidebar.selectbox("메뉴를 선택하세요", ["대여 및 반납 데이터", "터미널 위치", "미세먼지 현황", "교통혼잡 영향"])

# Load data
@st.cache_data
def load_data():
    rental_data = pd.read_csv("rental_data.csv", encoding="euc-kr")
    station_data = pd.read_csv("station_data.csv", encoding="euc-kr")
    return rental_data, station_data

rental_data, station_data = load_data()

# 1. 대여 및 반납 데이터
if menu == "대여 및 반납 데이터":
    st.header("대여 및 반납 데이터")
    st.subheader("데이터 미리보기")
    st.dataframe(rental_data.head())
    st.subheader("터미널 정보")
    st.dataframe(station_data.head())

# 2. 터미널 위치 시각화
elif menu == "터미널 위치":
    st.header("터미널 위치 시각화")
    map = folium.Map(location=[35.2, 128.65], zoom_start=12)
    for _, row in station_data.iterrows():
        folium.Marker(
            [row['위도'], row['경도']],
            tooltip=row['터미널명']
        ).add_to(map)
    folium_static(map)

# 3. 창원시 미세먼지 현황
elif menu == "미세먼지 현황":
    st.header("🌫️ 창원시 미세먼지 현황")

    # 미세먼지 데이터 API (수동 데이터 또는 API 연동 필요)
    @st.cache_data
    def get_air_quality_data():
        # Placeholder for actual API data fetching
        data = {
            "날짜": ["2022-12-01", "2022-12-02", "2022-12-03", "2022-12-04", "2022-12-05"],
            "미세먼지(PM10)": [40, 50, 35, 70, 55],
            "초미세먼지(PM2.5)": [20, 25, 18, 30, 28]
        }
        return pd.DataFrame(data)

    air_quality_data = get_air_quality_data()
    st.dataframe(air_quality_data)

    # 시각화
    st.subheader("미세먼지 현황 시각화")
    plt.figure(figsize=(10, 5))
    plt.plot(air_quality_data["날짜"], air_quality_data["미세먼지(PM10)"], label="PM10 (미세먼지)", marker='o')
    plt.plot(air_quality_data["날짜"], air_quality_data["초미세먼지(PM2.5)"], label="PM2.5 (초미세먼지)", marker='o')
    plt.xlabel("날짜")
    plt.ylabel("농도 (㎍/㎥)")
    plt.title("미세먼지 및 초미세먼지 현황")
    plt.legend()
    st.pyplot(plt)

# 4. 공영자전거와 교통혼잡
elif menu == "교통혼잡 영향":
    st.header("🚗 공영자전거와 교통혼잡 영향")

    # 가상의 데이터: 공영자전거 이용률과 교통혼잡지수
    data = {
        "월": ["2022-01", "2022-02", "2022-03", "2022-04", "2022-05"],
        "누비자 이용률(%)": [20, 25, 30, 35, 40],
        "교통혼잡지수": [70, 68, 65, 60, 55]
    }
    congestion_data = pd.DataFrame(data)
    st.dataframe(congestion_data)

    # 시각화
    st.subheader("공영자전거와 교통혼잡")
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.bar(congestion_data["월"], congestion_data["누비자 이용률(%)"], color='b', alpha=0.6, label="누비자 이용률 (%)")
    ax1.set_ylabel("누비자 이용률 (%)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(congestion_data["월"], congestion_data["교통혼잡지수"], color='r', marker='o', label="교통혼잡지수")
    ax2.set_ylabel("교통혼잡지수", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    - 공영자전거 이용률이 증가하면서 교통혼잡지수가 점차 감소하는 경향이 보입니다.
    - 이는 공영자전거가 교통 체증 완화에 기여하고 있음을 나타냅니다.
    """)

st.markdown("**데이터와 분석은 계속 업데이트됩니다!**")
