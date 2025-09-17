import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 기본 페이지 설정 ---
st.set_page_config(
    page_title="실시간 데이터 시각화",
    page_icon="✍",
    layout="wide"
)

# --- 2. 대시보드 제목 ---
st.title("실시간 데이터 입력 및 시각화 대시보드")
st.write("아래 표에 직접 데이터를 입력하거나 수정하면, 오른쪽 차트가 실시간으로 업데이트됩니다.")
st.info("표의 마지막 빈 줄에 내용을 입력하면 새 행이 추가됩니다", icon="💡")

# --- 3. Session State를 활용한 데이터 프레임 초기화 ---
if 'df' not in st.session_state:
    initial_data = {
        "항목": ["사과 🍎", "바나나 🍌", "딸기 🍓", "오렌지 🍊"],
        "수량": [100, 55, 74, 66]
    }
    st.session_state.df = pd.DataFrame(initial_data)


# --- 4. 화면 레이아웃 구성 ---
col1, col2 = st.columns([0.8,1.2])


# --- 5. 데이터 입력 영역 (왼쪽 컬럼) ---
with col1:
    st.header("데이터 입력")
    #에디터 사용을 통해 수정 가능하도록 설정
    #dynamic => 추가, 수정 등 자유롭게 설정
  
    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        key="data_editor",
        use_container_width=True
    )


# --- 6. 실시간 시각화 영역 (오른쪽 컬럼) ---
with col2:
    st.header("실시간 시각화")

    # 추가된 부분: 그래프 선택 기능
    chart_type = st.selectbox(
        "보고 싶은 그래프를 선택하세요:",
        ["막대그래프", "파이그래프", "꺾은선그래프", "영역그래프"]
    )

    if not edited_df.empty:
        try:
            # 수정된 부분: 선택에 따라 다른 그래프를 그림
            if chart_type == "막대그래프":
                fig = px.bar(
                    edited_df, x="항목", y="수량", title="항목별 수량",
                    color="항목", template="plotly_white"
                )
            elif chart_type == "파이그래프":
                fig = px.pie(
                    edited_df, names="항목", values="수량", title="항목별 비율",
                    hole=0.3 # 도넛 모양으로 만들기
                )
            elif chart_type == "꺾은선그래프":
                fig = px.line(
                    edited_df, x="항목", y="수량", title="항목별 수량 추이",
                    markers=True, # 데이터 지점에 점 표시
                    template="plotly_white"
                )
            elif chart_type == "영역그래프":
                fig = px.area(
                    edited_df, x="항목", y="수량", title="항목별 수량 영역",
                    markers=True, template="plotly_white"
                )

            fig.update_layout(yaxis_title="수량", xaxis_title="항목")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"차트를 그리는 중 오류가 발생했습니다: {e}")
            st.warning("차트를 그리려면 '항목'과 '수량' 컬럼이 필요하며, '수량' 컬럼은 숫자여야 합니다.")
    else:
        st.info("데이터를 입력하면 차트가 여기에 표시됩니다.")

