[
  {
    "name": "Ahri",
    "mbti": ["ENFP", "ENTP"],
    "role": "Mid",
    "playstyle": "기동성, 유연한 플레이",
    "image_url": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Ahri.png"
  },
  {
    "name": "Garen",
    "mbti": ["ESTJ", "ESFJ"],
    "role": "Top",
    "playstyle": "단단함, 직관적 전투",
    "image_url": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Garen.png"
  }
]

import streamlit as st
import pandas as pd
import random

# 데이터 로드
champions = pd.read_csv("champions_mbti.csv")  # CSV에는 name, mbti, role, playstyle, image_url 포함

# 제목
st.title("🎯 MBTI 기반 롤 챔피언 추천")
st.write("당신의 MBTI에 맞는 챔피언을 추천해드립니다!")

# MBTI 선택
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]
user_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_types)

if st.button("추천받기"):
    matched = champions[champions["mbti"].str.contains(user_mbti)]
    
    if matched.empty:
        st.warning("해당 MBTI에 대한 추천이 없습니다.")
    else:
        choice = matched.sample(1).iloc[0]  # 랜덤으로 한 명 추천
        st.subheader(f"추천 챔피언: {choice['name']}")
        st.image(choice['image_url'], width=150)
        st.write(f"**포지션**: {choice['role']}")
        st.write(f"**플레이 스타일**: {choice['playstyle']}")

