import streamlit as st

st.set_page_config(page_title="롤 챔피언 추천기", page_icon="🎮", layout="centered")

# 챔피언 매핑
champion_db = {
    # 탑솔러
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "초반 스노우볼형"): ("레넥톤", "기동성과 폭발적인 딜로 초반부터 공격적인 탑솔러"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "공격적", "후반 밸류형"): ("카밀", "후반에 강력한 1대1과 팀파이트 활약 가능"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "수비적", "초반 스노우볼형"): ("제이스", "초반 라인전 주도권과 변신으로 변칙적 플레이 가능"),
    ("튼튼하게 앞라인을 담당하는 탑솔러형", "수비적", "후반 밸류형"): ("케일", "후반 성장 후 압도적인 캐리력을 보여주는 탑솔러"),

    # 정글
    ("전략적으로 움직이는 운영형", "공격적", "초반 스노우볼형"): ("리 신", "초반 공격적인 정글 운영과 갱킹으로 승기를 잡는 스타일"),
    ("전략적으로 움직이는 운영형", "공격적", "후반 밸류형"): ("비에고", "중후반부터 강력한 한타 캐리 잠재력을 가진 정글러"),
    ("전략적으로 움직이는 운영형", "수비적", "초반 스노우볼형"): ("뽀삐", "강력한 CC와 초반 안정적인 맵 장악력 보유"),
    ("전략적으로 움직이는 운영형", "수비적", "후반 밸류형"): ("마오카이", "후반까지 안정적으로 성장하며 팀 승리에 기여"),

    # 미드
    ("팀을 이끄는 리더형", "공격적", "초반 스노우볼형"): ("라이즈", "글로벌 궁극기로 팀을 이끄는 전형적인 리더형 미드"),
    ("팀을 이끄는 리더형", "공격적", "후반 밸류형"): ("요네", "후반 캐리력이 뛰어난 공격형 미드"),
    ("팀을 이끄는 리더형", "수비적", "초반 스노우볼형"): ("갈리오", "팀을 보호하고 한타에 강력한 영향력을 주는 수비형 미드"),
    ("팀을 이끄는 리더형", "수비적", "후반 밸류형"): ("아지르", "후반 왕귀 후 강력한 한타 지배력을 가진 미드"),

    # 원딜
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "공격적", "초반 스노우볼형"): ("드레이븐", "초반 강력한 라인전과 화력을 발휘"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "공격적", "후반 밸류형"): ("제리", "후반 캐리력이 뛰어난 기동성 높은 원딜"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "수비적", "초반 스노우볼형"): ("진", "초반 안정적인 라인전과 후반 폭딜 제공"),
    ("팀의 주력 화력을 담당하는 원거리 딜러형", "수비적", "후반 밸류형"): ("아펠리오스", "후반 한타에서 압도적인 캐리력을 보이는 원딜"),

    # 서포터
    ("팀원을 도와주는 서포터형", "공격적", "초반 스노우볼형"): ("블리츠크랭크", "초반 강력한 이니시에이팅으로 게임 흐름을 바꾸는 서포터"),
    ("팀원을 도와주는 서포터형", "공격적", "후반 밸류형"): ("알리스타", "후반에도 탱킹과 이니시로 팀을 이끄는 서포터"),
    ("팀원을 도와주는 서포터형", "수비적", "초반 스노우볼형"): ("브라움", "초반 팀 보호와 안정적인 수비 가능"),
    ("팀원을 도와주는 서포터형", "수비적", "후반 밸류형"): ("쓰레쉬", "후반에도 팀 보호와 이니시로 유틸성이 뛰어난 서포터"),
}

# 한글 → 영문 URL 매핑 (스플래시 이미지)
champion_img_map = {
    "레넥톤": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Renekton_0.jpg",
    "카밀": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Camille_0.jpg",
    "제이스": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Jayce_0.jpg",
    "케일": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Kayle_0.jpg",
    "리 신": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_0.jpg",
    "비에고": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Viego_0.jpg",
    "뽀삐": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Poppy_0.jpg",
    "마오카이": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Maokai_0.jpg",
    "라이즈": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ryze_0.jpg",
    "요네": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yone_0.jpg",
    "갈리오": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Galio_0.jpg",
    "아지르": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Azir_0.jpg",
    "드레이븐": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Draven_0.jpg",
    "제리": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Zeri_0.jpg",
    "진": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Jhin_0.jpg",
    "아펠리오스": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Aphelios_0.jpg",
    "블리츠크랭크": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Blitzcrank_0.jpg",
    "알리스타": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Alistar_0.jpg",
    "브라움": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Braum_0.jpg",
    "쓰레쉬": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Thresh_0.jpg",
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
    
    img_url = champion_img_map.get(champion, None)
    if img_url:
        st.image(img_url, use_container_width=True)
    else:
        st.warning("이미지를 불러올 수 없습니다.")
    
    st.button("처음으로 돌아가기", on_click=lambda: st.session_state.update({"step": 1, "q1": None, "q2": None, "q3": None}))

if st.session_state.step == 1:
    step1()
elif st.session_state.step == 2:
    step2()
elif st.session_state.step == 3:
    step3()
elif st.session_state.step == 4:
    result()
