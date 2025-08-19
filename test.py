import streamlit as st

st.set_page_config(page_title="롤 챔피언 추천기", page_icon="🎮", layout="centered")

# 챔피언 매핑
champion_db = {
    # 탑솔러
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "초반 스노우볼형"): ("리븐", "기동성과 폭발적인 딜로 초반부터 공격적인 탑솔러"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "후반 밸류형"): ("피오라", "후반에도 강력한 1대1과 팀파이트 활약 가능"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "수비적", "초반 스노우볼형"): ("나서스", "초반 약하지만 성장을 통해 팀을 압도"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "수비적", "후반 밸류형"): ("요릭", "튼튼한 방어와 후반 팀파이트에서 안정적인 활약"),

    # 정글
    ("전략적으로 움직이는 운영형", "공격적", "초반 스노우볼형"): ("리 신", "초반 공격적인 정글 운영과 갱킹으로 승기를 잡는 스타일"),
    ("전략적으로 움직이는 운영형", "공격적", "후반 밸류형"): ("카직스", "중반~후반 성장 후 강력한 스노우볼링 가능"),
    ("전략적으로 움직이는 운영형", "수비적", "초반 스노우볼형"): ("세주아니", "초반 전략적 맵 장악과 팀 보호에 강점"),
    ("전략적으로 움직이는 운영형", "수비적", "후반 밸류형"): ("마오카이", "후반까지 안정적으로 성장하며 팀 승리에 기여"),

    # 미드 (리더형)
    ("팀을 이끄는 리더형", "공격적", "초반 스노우볼형"): ("라이즈", "초반부터 적극적으로 성장하며 팀 승리에 기여"),
    ("팀을 이끄는 리더형", "공격적", "후반 밸류형"): ("요네", "후반 캐리력이 뛰어난 공격형 리더형 미드"),
    ("팀을 이끄는 리더형", "수비적", "초반 스노우볼형"): ("조이", "초반 안전하게 견제하며 성장"),
    ("팀을 이끄는 리더형", "수비적", "후반 밸류형"): ("카사딘", "후반에 강력한 캐리와 맵 장악으로 팀 승리 기여"),

    # 원딜
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "공격적", "초반 스노우볼형"): ("드레이븐", "초반 공격적으로 화력을 발휘"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "공격적", "후반 밸류형"): ("카이사", "후반 캐리력이 뛰어난 공격형 원딜"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "수비적", "초반 스노우볼형"): ("바루스", "안정적인 견제와 초반 견제 가능"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "수비적", "후반 밸류형"): ("스몰더", "후반에도 안정적인 딜링 가능"),

    # 서포터
    ("팀원을 도와주는 서포터형", "공격적", "초반 스노우볼형"): ("레오나", "초반 강력한 이니시에이팅으로 팀 승기 확보"),
    ("팀원을 도와주는 서포터형", "공격적", "후반 밸류형"): ("쓰레쉬", "후반에도 팀 보호와 딜 지원"),
    ("팀원을 도와주는 서포터형", "수비적", "초반 스노우볼형"): ("브라움", "초반 안전하게 팀 보호 및 견제"),
    ("팀원을 도와주는 서포터형", "수비적", "후반 밸류형"): ("소나", "후반 힐과 지원으로 팀 승리 기여"),
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

# 단계별 페이지
def step1():
    st.header("1/3 질문")
    st.write("선호하는 플레이 스타일을 선택하세요.")
    st.session_state.q1 = st.radio("1. 선호하는 플레이 스타일은?", ["공격적", "수비적"])
    if st.button("다음"):
        st.session_state.step = 2
        st.experimental_rerun()

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
    if st.button("다음"):
        st.session_state.step = 3
        st.experimental_rerun()

def step3():
    st.header("3/3 질문")
    st.write("당신의 성향에 가까운 것은?")
    st.session_state.q3 = st.radio(
        "3. 당신의 성향에 가까운 것은?", 
        [
            "초반 스노우볼형 (게임 초반부터 공격적으로 성장하며 승기를 잡는 스타일)", 
            "후반 밸류형 (초반은 조심스럽게 운영하지만, 후반에 팀 승리에 큰 영향을 주는 스타일)"
        ]
    )
    if st.button("결과 보기"):
        st.session_state.step = 4
        st.experimental_rerun()

def result():
    st.header("🏆 추천 챔피언")
    key = (st.session_state.q2, st.session_state.q1, st.session_state.q3)
    champion, desc = champion_db.get(key, ("정보 없음", "해당 조합에 맞는 챔피언 데이터가 없습니다."))
    st.subheader(f"추천 챔피언: {champion}")
    st.write(desc)
    st.image(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion.replace(' ', '')}_0.jpg")
    if st.button("처음으로 돌아가기"):
        st.session_state.step = 1
        st.experimental_rerun()

# 단계별 함수 호출
if st.session_state.step == 1:
    step1()
elif st.session_state.step == 2:
    step2()
elif st.session_state.step == 3:
    step3()
elif st.session_state.step == 4:
    result()
