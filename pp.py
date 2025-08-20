import streamlit as st

st.set_page_config(page_title="롤 챔피언 추천기", page_icon="🎮", layout="centered")

# CSS로 배경 꾸미기
st.markdown(
    """
    <style>
    /* 전체 배경 */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1612832021055-4e5f4b1f7c51?auto=format&fit=crop&w=1470&q=80");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    /* 질문 카드 스타일 */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }
    /* 제목 스타일 */
    h1, h2, h3 {
        color: #ff69b4;
        text-align: center;
        font-family: "Comic Sans MS", cursive, sans-serif;
    }
    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #ffb6c1;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        width: 200px;
        margin: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True
)

# 챔피언 매핑 (간단하게 예시)
champion_db = {
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "초반 스노우볼형"): ("레넥톤", "기동성과 폭발적인 딜로 초반부터 공격적인 탑솔러"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "후반 밸류형"): ("카밀", "후반에 강력한 1대1과 팀파이트 활약 가능"),
    # 나머지는 생략, 기존 코드 그대로
}

# session_state 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "q1" not in st.session_state:
    st.session_state.q1 = None
if "q2" not in st.session_state:
    st.session_state.q2 = None
if "q3" not in st.session_state:
    st.session_state.q3 = None

def go_next_step():
    st.session_state.step += 1

def step1():
    st.header("1/3 질문")
    st.write("선호하는 플레이 스타일을 선택하세요.")
    st.session_state.q1 = st.radio("1. 선호하는 플레이 스타일은?", ["공격적", "수비적"])
    st.button("다음", on_click=go_next_step)

def step2():
    st.header("2/3 질문")
    st.write("게임할 때 당신은?")
    st.session_state.q2 = st.radio("2. 게임할 때 당신은?", [
        "튼튼하게 앞라인을 담당하는 탑솔러형",
        "전략적으로 움직이는 운영형",
        "팀을 이끄는 리더형",
        "팀의 주력 화력을 담당하는 원거리 딜러형",
        "팀원을 도와주는 서포터형"
    ])
    st.button("다음", on_click=go_next_step)

def step3():
    st.header("3/3 질문")
    st.write("당신의 성향에 가까운 것은?")
    st.session_state.q3 = st.radio("3. 당신의 성향에 가까운 것은?", ["초반 스노우볼형", "후반 밸류형"])
    st.button("결과 보기", on_click=go_next_step)

def result():
    st.header("🏆 추천 챔피언")
    key = (st.session_state.q2, st.session_state.q1, st.session_state.q3)
    champion, desc = champion_db.get(key, ("정보 없음", "해당 조합에 맞는 챔피언 데이터가 없습니다."))
    st.subheader(f"추천 챔피언: {champion}")
    st.write(desc)
    st.button("처음으로 돌아가기", on_click=lambda: st.session_state.update({"step":1,"q1":None,"q2":None,"q3":None}))

# 단계별 호출
if st.session_state.step == 1:
    step1()
elif st.session_state.step == 2:
    step2()
elif st.session_state.step == 3:
    step3()
elif st.session_state.step == 4:
    result()
