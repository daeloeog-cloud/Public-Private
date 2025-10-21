import streamlit as st

st.set_page_config(page_title="Baccarat Predictor", page_icon="🎴", layout="centered")

st.title("🎴 모바일용 바카라 예측기 (OCR 제거 버전)")
st.markdown("✏️ 결과를 직접 입력해서 분석합니다. (OCR 기능 제외)")

st.markdown("---")
st.markdown("### 수동 입력")
manual_input = st.text_input("직접 결과 입력 (예: P B B T P)", value="")

if manual_input:
    seq = manual_input.replace(',', ' ').split()
    total = len(seq)
    p_count = seq.count("P")
    b_count = seq.count("B")
    t_count = seq.count("T")

    st.markdown(f"**총 판수:** {total}")
    st.markdown(f"🟦 Player: {p_count} / 🔴 Banker: {b_count} / ⚪ Tie: {t_count}")

    if total >= 3:
        last3 = seq[-3:]
        pattern = ''.join(last3)
        st.markdown(f"최근 3회 패턴: {pattern}")
        if pattern.count("P") > pattern.count("B"):
            st.success("📊 다음 예측: **Banker 쪽 확률 높음**")
        elif pattern.count("B") > pattern.count("P"):
            st.info("📊 다음 예측: **Player 쪽 확률 높음**")
        else:
            st.warning("📊 무승부 확률도 존재 (Tie 가능성 있음)")

st.markdown("---")
st.markdown("### 💰 마틴게일 계산기")

start_bet = st.number_input("시작 배팅 금액(₩)", min_value=1000, value=1000, step=1000)
odds = st.number_input("배당 (예: Banker=1.56, Player=2.48)", min_value=1.01, value=1.56, step=0.01)
target_profit = st.number_input("목표 수익(₩)", min_value=500, value=1000, step=500)
max_rounds = st.slider("최대 마틴 횟수", 1, 10, 6)

bets = [start_bet]
for i in range(1, max_rounds):
    next_bet = (target_profit + sum(bets)) / (odds - 1)
    bets.append(round(next_bet, -3))

st.write("📈 마틴 배팅 금액표:")
for i, b in enumerate(bets, start=1):
    st.write(f"{i}회차: {int(b):,}원")

total = sum(bets)
st.success(f"총 필요 시드: {int(total):,}원")

st.markdown("---")
st.caption("Made with ❤️ by ChatGPT (GPT-5)")
