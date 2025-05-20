import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Gemma 모델 초기화
llm = Ollama(model="gemma3:latest")

# 페이지 설정
st.set_page_config(page_title="재료 기반 음식 추천", page_icon="🍽️")
st.title("🍚 뭐 만들어 먹지?")

# 세션 상태 초기화
if "ingredient" not in st.session_state:
    st.session_state.ingredient = None

if "dishes" not in st.session_state:
    st.session_state.dishes = []

if "selected_dish" not in st.session_state:
    st.session_state.selected_dish = None

# 1단계: 재료 입력
ingredient = st.text_input("재료를 입력하세요 (예: 사과, 당근)", "")

if ingredient and st.button("요리 추천받기"):
    st.session_state.ingredient = ingredient
    st.session_state.selected_dish = None  # 초기화

    # 요리 추천 프롬프트
    prompt_template = PromptTemplate.from_template(
        "다음 재료로 만들 수 있는 한국 음식 5가지를 추천해줘: {ingredient}. 각 음식은 한 줄로만 알려줘."
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(ingredient)

    # 줄 단위로 음식 리스트 만들기
    st.session_state.dishes = [dish.strip("-• \n") for dish in response.strip().split("\n") if dish.strip()]

# 2단계: 음식 리스트 출력 및 선택
if st.session_state.dishes and not st.session_state.selected_dish:
    st.subheader(f"🧑‍🍳 '{st.session_state.ingredient}'(으)로 만들 수 있는 음식들:")
    dish_choice = st.radio("음식을 하나 선택하세요:", st.session_state.dishes)

    if st.button("레시피 보기"):
        st.session_state.selected_dish = dish_choice

# 3단계: 레시피 출력
if st.session_state.selected_dish:
    st.subheader(f"📋 '{st.session_state.selected_dish}'의 레시피")

    recipe_prompt = PromptTemplate.from_template(
        "한국 요리 '{dish}'의 상세한 레시피를 단계별로 설명해줘. 간단명료하게 부탁해."
    )

    recipe_chain = LLMChain(llm=llm, prompt=recipe_prompt)
    recipe = recipe_chain.run(st.session_state.selected_dish)

    st.markdown(recipe)
