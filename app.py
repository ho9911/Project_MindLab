import streamlit as st
import pandas as pd
import altair as alt

# ===============================
# 1️⃣ 데이터 불러오기
# ===============================

past_path = '/content/2018-2024.xlsx'
future_path = '/content/예상수요량_2025예측.xlsx'

past_df = pd.read_excel(past_path)
future_df = pd.read_excel(future_path)

past_df['월'] = past_df['월'].astype(int)
future_df['월'] = future_df['월'].astype(int)

past_df = past_df.rename(columns={'판매량(kg)': 'y'})
future_df = future_df.rename(columns={'예상수요량': 'y'})

past_df['y'] = past_df['y'].astype(int)
future_df['y'] = future_df['y'].round().astype(int)

# ===============================
# 2️⃣ 페이지 설정 & 스타일
# ===============================

st.set_page_config(page_title="과일 수요량 대시보드", layout="wide")

st.markdown("""
    <style>
        /* 타이틀을 더 아래로 내려서 헤더와 겹치지 않게 */
        .main > div:first-child {
            padding-top: 50px !important;
        }
        .title {
            font-size: 30px;
            font-weight: 700;
            margin-top: 25px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 페이지 타이틀
st.markdown("<div class='title'>🍎 과일 수요량 대시보드 (과거 + 2025 예측)</div>", unsafe_allow_html=True)

# ===============================
# 3️⃣ 데이터 선택
# ===============================

data_type = st.sidebar.radio("📂 사용할 데이터", ["과거 데이터", "2025년 예측 데이터"])
selected_df = past_df if data_type == "과거 데이터" else future_df

# ===============================
# 4️⃣ 년도 선택 (2025년 예측은 숨김)
# ===============================

if data_type == "과거 데이터":
    available_years = sorted(selected_df['년도'].unique())

    selected_years = st.multiselect(
        "📅 조회할 년도",
        available_years,
        default=[]  # 기본 선택 없음
    )

    df_filtered = selected_df[selected_df['년도'].isin(selected_years)]
else:
    df_filtered = selected_df.copy()  # 2025년만 존재 → 자동 고정

# ===============================
# 5️⃣ 과일 선택 (기본 선택 없음)
# ===============================

fruits = sorted(df_filtered['과일종류'].unique())

selected_fruits = st.multiselect(
    "🍊 표시할 과일 선택",
    fruits,
    default=[]   # 기본 선택 없음
)

df_chart = df_filtered[df_filtered['과일종류'].isin(selected_fruits)]

# ===============================
# 6️⃣ 그래프 영역
# ===============================

st.subheader("📈 월별 수요량 그래프")

if len(df_chart) > 0:

    if data_type == "과거 데이터":
        years = sorted(df_chart['년도'].unique())
    else:
        years = [2025]

    for y in years:
        st.markdown(f"### 📌 {y}년")

        df_year = df_chart[df_chart['년도'] == y]

        chart = (
            alt.Chart(df_year)
            .mark_line(point=True)
            .encode(
                x=alt.X('월:O', title='월', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('y:Q', title='수요량'),
                color='과일종류:N',
                tooltip=['년도', '과일종류', '월', 'y']
            )
            .properties(height=350)
        )

        st.altair_chart(chart, use_container_width=True)

else:
    st.info("그래프에 표시할 과일을 선택하세요.")

# ===============================
# 7️⃣ 테이블 영역
# ===============================

st.subheader("📊 상세 데이터")

selected_fruits_table = st.multiselect(
    "📋 테이블 표시 과일",
    fruits,
    default=[]
)

df_table = df_filtered[df_filtered['과일종류'].isin(selected_fruits_table)]

if len(df_table) > 0:
    df_show = df_table[['년도', '월', '과일종류', 'y']].rename(columns={'y': '수요량'})
    st.dataframe(df_show, use_container_width=True)
else:
    st.info("테이블에 표시할 과일을 선택하세요.")
