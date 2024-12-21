import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import matplotlib.font_manager as fm
import os

# 페이지 설정 (최상단 위치)
st.set_page_config(page_title="누비자 데이터 분석", layout="wide")

# 한글 폰트 설정
def set_korean_font():
    import matplotlib
    if not os.path.exists("/usr/share/fonts/truetype/nanum"):
        os.system("apt-get update -qq && apt-get install -y fonts-nanum*")
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        matplotlib.rc('font', family=font_prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
        return font_prop
    else:
        raise FileNotFoundError("폰트 파일을 찾을 수 없습니다.")

# 한글 폰트 설정 적용
font_prop = set_korean_font()

# Streamlit 제목 및 설명
st.title("🚲 창원시 공영자전거 데이터 대시보드")
st.markdown("""
### 목적
- 창원시 공영자전거의 데이터 분석 및 환경적 영향을 평가합니다.
- 미세먼지 현황과 교통혼잡 완화 효과를 시각적으로 이해합니다.
""")

# Sidebar 메뉴
st.sidebar.header("📋 메뉴")
menu = st.sidebar.selectbox("메뉴를 선택하세요", ["대여 및 반납 데이터", "터미널 위치", "미세먼지 현황", "교통혼잡 영향"])

# 데이터 로드 함수
@st.cache_data
def load_data():
    rental_data = pd.read_csv("rental_data.csv", encoding="euc-kr")
    station_data = pd.read_csv("station_data.csv", encoding="euc-kr")
    return rental_data, station_data

# 데이터 로드
rental_data, station_data = load_data()

# 1. 대여 및 반납 데이터
if menu == "대여 및 반납 데이터":
    st.header("대여 및 반납 데이터")
    st.subheader("대여 데이터 미리보기")
    st.dataframe(rental_data.head())
    st.subheader("터미널 정보 미리보기")
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

# 3. 미세먼지 현황
elif menu == "미세먼지 현황":
    st.header("🌫️ 창원시 미세먼지 현황")
    
    # 예제 데이터
    air_quality_data = pd.DataFrame({
        "날짜": ["2022-12-01", "2022-12-02", "2022-12-03"],
        "미세먼지(PM10)": [40, 50, 35],
        "초미세먼지(PM2.5)": [20, 25, 18]
    })
    st.dataframe(air_quality_data)

    # 미세먼지 그래프
    st.subheader("미세먼지 현황 시각화")
    plt.figure(figsize=(10, 5))
    plt.plot(air_quality_data["날짜"], air_quality_data["미세먼지(PM10)"], label="PM10 (미세먼지)", marker='o')
    plt.plot(air_quality_data["날짜"], air_quality_data["초미세먼지(PM2.5)"], label="PM2.5 (초미세먼지)", marker='o')
    plt.xlabel("날짜", fontproperties=font_prop)
    plt.ylabel("농도 (㎍/㎥)", fontproperties=font_prop)
    plt.title("미세먼지 및 초미세먼지 현황", fontproperties=font_prop)
    plt.legend(prop=font_prop)
    st.pyplot(plt)

# 4. 공영자전거와 교통혼잡 영향
elif menu == "교통혼잡 영향":
    st.header("🚗 공영자전거와 교통혼잡 영향")
    
    # 예제 데이터
    congestion_data = pd.DataFrame({
        "월": ["2022-01", "2022-02", "2022-03"],
        "누비자 이용률(%)": [20, 25, 30],
        "교통혼잡지수": [70, 65, 60]
    })
    st.dataframe(congestion_data)

    # 교통혼잡 그래프
    st.subheader("공영자전거와 교통혼잡")
    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.bar(congestion_data["월"], congestion_data["누비자 이용률(%)"], color='b', alpha=0.6, label="누비자 이용률 (%)")
    ax1.set_ylabel("누비자 이용률 (%)", color='b', fontproperties=font_prop)
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(congestion_data["월"], congestion_data["교통혼잡지수"], color='r', marker='o', label="교통혼잡지수")
    ax2.set_ylabel("교통혼잡지수", color='r', fontproperties=font_prop)
    ax2.tick_params(axis='y', labelcolor='r')

    fig.tight_layout()
    plt.title("공영자전거와 교통혼잡의 상관관계", fontproperties=font_prop)
    st.pyplot(fig)
