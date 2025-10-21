import streamlit as st
from PIL import Image
import pytesseract
import numpy as np
import cv2

st.set_page_config(page_title="Baccarat Predictor", page_icon="🎴", layout="centered")

st.title("🎴 모바일용 바카라 예측기")
st.markdown("📸 사진 업로드 또는 직접 입력으로 결과를 분석합니다.")

uploaded_file = st.file_uploader("결과표 사진 업로드 (또는 카메라 촬영)", type=["jpg", "png", "jpeg"])

def enhance_for_ocr(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.medianBlur(gray, 3)
    _, th = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
    return Image.fromarray(th)

ocr_text = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지", use_container_width=True)
    gray = enhance_for_ocr(image)
    ocr_text = pytesseract.image_to_string(gray, lang="eng")
    st.text_area("OCR 인식 결과", ocr_text, height=150)

st.markdown("---")
st.markdown("### ✏️ 수동 입력")
manual_input = st.text_input("직접 결과 입력 (예: P B B T P)", value=ocr_text.strip())

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
