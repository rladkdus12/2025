import streamlit as st
import pandas as pd
from typing import List, Dict

st.set_page_config(page_title="MBTI 기반 롤 챔피언 추천", page_icon="🎯", layout="wide")

# ------------------------------
# 1) 데이터: 챔피언 메타 정보
# ------------------------------
# 각 챔피언의 기본 정보와 태그(플레이 스타일), 난이도, 주 포지션을 정의합니다.
# 이미지는 버전 의존성이 낮은 스플래시 이미지를 사용합니다.

CHAMPIONS: Dict[str, Dict] = {
    # 탑/정글/미드/원딜/서폿 (League positions)
    "Garen": {"roles": ["Top"], "difficulty": "Easy", "tags": ["bruiser", "tank", "macro", "teamfight", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Garen_0.jpg"},
    "Malphite": {"roles": ["Top"], "difficulty": "Easy", "tags": ["tank", "engage", "teamfight", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Malphite_0.jpg"},
    "Ashe": {"roles": ["ADC", "Support"], "difficulty": "Easy", "tags": ["utility", "poke", "kiting", "vision", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ashe_0.jpg"},

    "Soraka": {"roles": ["Support"], "difficulty": "Easy", "tags": ["heal", "utility", "peel", "teamplay", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Soraka_0.jpg"},
    "Sona": {"roles": ["Support"], "difficulty": "Easy", "tags": ["aura", "utility", "teamfight", "poke", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sona_0.jpg"},
    "Nami": {"roles": ["Support"], "difficulty": "Medium", "tags": ["utility", "engage", "peel", "poke", "teamplay"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Nami_0.jpg"},

    "Shen": {"roles": ["Top"], "difficulty": "Medium", "tags": ["global", "tank", "peel", "teamplay", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Shen_0.jpg"},
    "Orianna": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["control", "teamfight", "wombo", "poke", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Orianna_0.jpg"},
    "Karma": {"roles": ["Support", "Mid"], "difficulty": "Medium", "tags": ["utility", "poke", "shield", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Karma_0.jpg"},

    "Viktor": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["control", "scaling", "poke", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Viktor_0.jpg"},
    "Azir": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["dps", "outplay", "teamfight", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Azir_0.jpg"},
    "Ryze": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["scaling", "macro", "splitpush", "control"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ryze_0.jpg"},

    "Zed": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["assassin", "outplay", "burst", "roam", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Zed_0.jpg"},
    "Riven": {"roles": ["Top"], "difficulty": "Hard", "tags": ["outplay", "mobility", "splitpush", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Riven_0.jpg"},
    "LeeSin": {"roles": ["Jungle"], "difficulty": "Hard", "tags": ["playmaker", "mobility", "insec", "early", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_0.jpg"},

    "Vayne": {"roles": ["ADC"], "difficulty": "Hard", "tags": ["duelist", "mobility", "outplay", "lategame", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Vayne_0.jpg"},
    "Ezreal": {"roles": ["ADC"], "difficulty": "Medium", "tags": ["skillshot", "kiting", "poke", "mobility"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ezreal_0.jpg"},
    "Akali": {"roles": ["Mid", "Top"], "difficulty": "Hard", "tags": ["assassin", "outplay", "burst", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Akali_0.jpg"},

    "Ahri": {"roles": ["Mid"], "difficulty": "Medium", "tags": ["pick", "charm", "roam", "mobility", "burst"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg"},
    "Lulu": {"roles": ["Support"], "difficulty": "Medium", "tags": ["utility", "enchanter", "peel", "teamplay"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Lulu_0.jpg"},
    "Seraphine": {"roles": ["Support", "Mid"], "difficulty": "Easy", "tags": ["utility", "poke", "teamfight", "aura"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Seraphine_0.jpg"},

    "Jayce": {"roles": ["Top", "Mid"], "difficulty": "Hard", "tags": ["poke", "burst", "lane-bully", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Jayce_0.jpg"},
    "Heimerdinger": {"roles": ["Mid", "Top"], "difficulty": "Medium", "tags": ["pusher", "zone", "poke", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Heimerdinger_0.jpg"},
    "Xerath": {"roles": ["Mid"], "difficulty": "Medium", "tags": ["artillery", "poke", "siege", "macro"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Xerath_0.jpg"},

    "Draven": {"roles": ["ADC"], "difficulty": "Hard", "tags": ["aggressive", "snowball", "lane-bully", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Draven_0.jpg"},
    "Talon": {"roles": ["Mid"], "difficulty": "Medium", "tags": ["assassin", "roam", "burst", "splitpush"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Talon_0.jpg"},
    "Pantheon": {"roles": ["Top", "Jungle", "Support"], "difficulty": "Medium", "tags": ["aggressive", "pick", "global", "skirmish"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Pantheon_0.jpg"},

    "MissFortune": {"roles": ["ADC"], "difficulty": "Easy", "tags": ["lane-bully", "aoe", "wombo", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/MissFortune_0.jpg"},
    "Samira": {"roles": ["ADC"], "difficulty": "Hard", "tags": ["aggressive", "combo", "reset", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Samira_0.jpg"},
    "Katarina": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["reset", "snowball", "assassin", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Katarina_0.jpg"},

    "Ekko": {"roles": ["Jungle", "Mid"], "difficulty": "Medium", "tags": ["roam", "assassin", "outplay", "pick"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ekko_0.jpg"},
    "Zoe": {"roles": ["Mid"], "difficulty": "Hard", "tags": ["pick", "burst", "poke", "mechanical"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Zoe_0.jpg"},

    "JarvanIV": {"roles": ["Jungle"], "difficulty": "Medium", "tags": ["engage", "wombo", "teamfight", "gank"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/JarvanIV_0.jpg"},
    "Darius": {"roles": ["Top"], "difficulty": "Medium", "tags": ["bruiser", "snowball", "lane-bully", "teamfight"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Darius_0.jpg"},

    "Leona": {"roles": ["Support"], "difficulty": "Easy", "tags": ["engage", "tank", "pick", "teamfight", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Leona_0.jpg"},
    "Braum": {"roles": ["Support"], "difficulty": "Easy", "tags": ["peel", "engage", "tank", "teamplay", "simple"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Braum_0.jpg"},
    "Taric": {"roles": ["Support"], "difficulty": "Medium", "tags": ["invuln", "utility", "teamfight", "peel"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Taric_0.jpg"},

    "Galio": {"roles": ["Mid", "Support"], "difficulty": "Medium", "tags": ["global", "wombo", "engage", "teamfight"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Galio_0.jpg"},
    "Vi": {"roles": ["Jungle"], "difficulty": "Medium", "tags": ["engage", "pick", "gank", "teamfight"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Vi_0.jpg"},
    "Sett": {"roles": ["Top", "Jungle", "Support"], "difficulty": "Medium", "tags": ["bruiser", "brawler", "teamfight", "skirmish"], "image": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Sett_0.jpg"},
}

# MBTI별 추천 우선 후보(초기 베이스 매칭)
MBTI_TO_CHAMPS: Dict[str, List[str]] = {
    "ISTJ": ["Garen", "Malphite", "Ashe"],
    "ISFJ": ["Soraka", "Sona", "Nami"],
    "INFJ": ["Shen", "Orianna", "Karma"],
    "INTJ": ["Viktor", "Azir", "Ryze"],
    "ISTP": ["Zed", "Riven", "LeeSin"],
    "ISFP": ["Vayne", "Ezreal", "Akali"],
    "INFP": ["Ahri", "Lulu", "Seraphine"],
    "INTP": ["Jayce", "Heimerdinger", "Xerath"],
    "ESTP": ["Draven", "Talon", "Pantheon"],
    "ESFP": ["MissFortune", "Samira", "Katarina"],
    "ENFP": ["Ahri", "Ekko", "Nami"],
    "ENTP": ["Ekko", "Jayce", "Zoe"],
    "ESTJ": ["JarvanIV", "Garen", "Darius"],
    "ESFJ": ["Leona", "Braum", "Taric"],
    "ENFJ": ["Galio", "Orianna", "JarvanIV"],
    "ENTJ": ["Darius", "Sett", "Vi"],
}

# 포지션 통일 이름
ALL_ROLES = ["Top", "Jungle", "Mid", "ADC", "Support"]

# ------------------------------
# 2) 유틸 함수
# ------------------------------

def slug(name: str) -> str:
    return name.replace("'", "").replace(" ", "").lower()


def difficulty_score(pref: str, champ_diff: str) -> int:
    # 사용자가 원하는 난이도와 챔피언 난이도가 얼마나 맞는지 점수화
    order = {"Easy": 1, "Medium": 2, "Hard": 3}
    return 2 if order.get(pref, 2) == order.get(champ_diff, 2) else 0


def aggression_score(level: int, tags: List[str]) -> int:
    # 0(안전)~10(공격). 공격적이면 aggressive/assassin/lane-bully/reset 등 가산
    if level >= 7:
        hot = {"aggressive", "assassin", "lane-bully", "snowball", "reset", "burst"}
        return 2 if any(t in tags for t in hot) else 0
    elif level <= 3:
        calm = {"tank", "peel", "utility", "simple"}
        return 2 if any(t in tags for t in calm) else 0
    return 1 if ("balanced" in tags or "macro" in tags) else 0


def mechanics_score(pref: str, tags: List[str]) -> int:
    if pref == "높음":
        return 2 if ("mechanical" in tags or "outplay" in tags or "skillshot" in tags) else 0
    if pref == "낮음":
        return 2 if ("simple" in tags or "tank" in tags) else 0
    return 1 if ("macro" in tags or "utility" in tags) else 0


def teamplay_score(pref: str, tags: List[str]) -> int:
    if pref == "팀 위주":
        return 2 if ("teamfight" in tags or "utility" in tags or "engage" in tags or "peel" in tags or "wombo" in tags) else 0
    if pref == "개인 캐리":
        return 2 if ("assassin" in tags or "duelist" in tags or "splitpush" in tags or "snowball" in tags) else 0
    return 1 if ("macro" in tags or "pick" in tags) else 0


def role_score(pref_roles: List[str], champ_roles: List[str]) -> int:
    if not pref_roles:
        return 1  # 선택 안 했으면 가벼운 보정
    return 2 if any(r in champ_roles for r in pref_roles) else 0


def base_mbti_score(user_mbti: str, champ_name: str) -> int:
    if user_mbti in MBTI_TO_CHAMPS and champ_name in MBTI_TO_CHAMPS[user_mbti]:
        # 같은 MBTI 풀에 있으면 기반 점수 3
        return 3
    return 0


# ------------------------------
# 3) 사이드바 & 입력 UI
# ------------------------------
with st.sidebar:
    st.markdown("## ⚙️ 설정")
    st.caption("MBTI와 선호도를 선택해서 더 정밀한 추천을 받아보세요.")

    mbti_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ",
        "ISTP", "ISFP", "INFP", "INTP",
        "ESTP", "ESFP", "ENFP", "ENTP",
        "ESTJ", "ESFJ", "ENFJ", "ENTJ",
    ]
    user_mbti = st.selectbox("MBTI 선택", mbti_types, index=mbti_types.index("INFP"))

    pref_roles = st.multiselect("선호 포지션(복수 선택)", ALL_ROLES, default=[])

    col_a, col_b = st.columns(2)
    with col_a:
        pref_difficulty = st.selectbox("선호 난이도", ["Easy", "Medium", "Hard"], index=1)
    with col_b:
        pref_mech = st.selectbox("기계적 숙련도 선호", ["낮음", "보통", "높음"], index=1)

    aggr = st.slider("공격성(안전→공격)", 0, 10, 5)
    team_pref = st.selectbox("팀플레이/개인플레이", ["상황에 따라", "팀 위주", "개인 캐리"], index=0)

    st.divider()
    topn = st.slider("추천 개수", 1, 5, 3)
    run = st.button("🚀 추천받기")

# ------------------------------
# 4) 본문: 헤더
# ------------------------------
st.title("🎯 MBTI 기반 롤 챔피언 추천")
st.write("MBTI와 플레이 선호도를 바탕으로 챔피언을 추천합니다. 아래 결과는 **취향 점수 매칭**에 기반합니다.")

# ------------------------------
# 5) 매칭 로직 & 결과
# ------------------------------

def compute_scores() -> pd.DataFrame:
    rows = []
    for name, meta in CHAMPIONS.items():
        score = 0
        reasons = []

        # 1) MBTI 베이스
        b = base_mbti_score(user_mbti, name)
        if b:
            score += b
            reasons.append(f"MBTI {user_mbti} 추천 풀 포함(+{b})")

        # 2) 포지션
        r = role_score(pref_roles, meta["roles"])
        if r:
            score += r
            if pref_roles:
                reasons.append(f"선호 포지션과 일치(+{r}) : {', '.join(meta['roles'])}")

        # 3) 난이도
        d = difficulty_score(pref_difficulty, meta["difficulty"])
        if d:
            score += d
            reasons.append(f"선호 난이도와 일치(+{d}) : {meta['difficulty']}")

        # 4) 공격성
        a = aggression_score(aggr, meta["tags"])
        if a:
            score += a
            reasons.append(f"공격 성향 보정(+{a})")

        # 5) 기계적 숙련도
        m = mechanics_score(pref_mech, meta["tags"])
        if m:
            score += m
            reasons.append(f"기계적 난이도 선호(+{m})")

        # 6) 팀플레이 성향
        t = teamplay_score(team_pref, meta["tags"])
        if t:
            score += t
            reasons.append(f"팀/개인 성향 매칭(+{t})")

        rows.append({
            "name": name,
            "score": score,
            "roles": ", ".join(meta["roles"]),
            "difficulty": meta["difficulty"],
            "tags": ", ".join(meta["tags"]),
            "image": meta["image"],
            "reasons": reasons,
        })

    df = pd.DataFrame(rows).sort_values(["score", "name"], ascending=[False, True]).reset_index(drop=True)

    # 동점자 정렬 가벼운 규칙: MBTI 우선 → 선호 포지션 포함 수 → 이름
    def tie_breaker(row):
        mbti_bonus = 1 if row["name"] in MBTI_TO_CHAMPS[user_mbti] else 0
        pos_bonus = sum(1 for r in CHAMPIONS[row["name"]]["roles"] if r in pref_roles)
        return (mbti_bonus, pos_bonus, -len(row["name"]))

    df["_tb"] = df.apply(tie_breaker, axis=1)
    df = df.sort_values(["score", "_tb"], ascending=[False, False]).drop(columns=["_tb"]).reset_index(drop=True)
    return df


if run:
    result_df = compute_scores()
    if result_df.empty:
        st.warning("추천 계산에 실패했어요. 입력 값을 확인해주세요.")
    else:
        cols = st.columns(topn)
        for i in range(topn):
            if i >= len(result_df):
                break
            row = result_df.iloc[i]
            with cols[i]:
                st.markdown(f"### {i+1}. {row['name']}  ")
                st.image(row["image"], use_column_width=True)
                st.markdown(f"**포지션:** {row['roles']}  ")
                st.markdown(f"**난이도:** {row['difficulty']}  ")
                st.markdown(f"**태그:** {row['tags']}  ")
                with st.expander("추천 이유 보기"):
                    for r in row["reasons"]:
                        st.write("- ", r)
                # 외부 참고 링크 (슬러그 기반)
                _slug = slug(row["name"]) 
                st.markdown(
                    f"[OP.GG 검색](https://www.op.gg/champions/{_slug}) · "
                    f"[Fandom 위키](https://leagueoflegends.fandom.com/wiki/{row['name'].replace(' ', '_')})"
                )

        st.divider()
        with st.expander("전체 후보 점수표 보기"):
            show_cols = ["name", "score", "roles", "difficulty", "tags"]
            st.dataframe(result_df[show_cols], use_container_width=True, height=420)
else:
    # 초기 화면 안내
    left, right = st.columns([1, 1])
    with left:
        st.markdown("""
        ### 사용 방법
        1. **사이드바**에서 MBTI와 선호(포지션/난이도/공격성/숙련도/팀성향)를 고릅니다.
        2. **추천받기** 버튼을 누르면 상단에 **상위 N명**의 챔피언이 표시됩니다.
        3. 각 카드의 *추천 이유*와 외부 링크로 더 자세히 살펴보세요!
        """)
    with right:
        st.image("https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg", caption="예시 이미지: Ahri", use_column_width=True)

st.caption("※ 비공식 팬메이드 프로젝트입니다. Riot Games와 직접적인 관련이 없습니다. 이미지는 Riot Data Dragon의 공개 리소스를 사용합니다.")
