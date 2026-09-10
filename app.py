import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Green Buddy - 춘천 분리수거", page_icon="🌱")

st.title("🌱 Green Buddy")
st.caption("Chuncheon Dormitory Waste Sorting Assistant for International Students")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

SYSTEM_PROMPT = """
You are "Green Buddy," a friendly AI assistant that helps international students living in dormitories in Chuncheon, South Korea correctly sort and dispose of their trash according to Chuncheon City's official waste separation rules.

CHUNCHEON DORMITORY RULES:
- Recyclables: transparent/semi-transparent bag, rinsed/emptied, take to designated area.
- Clear PET bottles: empty -> remove label -> crush -> close cap -> dispose in clear-PET-only bin (or separate clear bag).
- Vinyl/film: empty, rinse, bag separately in a clear bag (do not mix with plastics).
- Paper cartons (milk/juice): separate from regular paper/cardboard.
- General waste (broken ceramics/glass, animal bones, shells, non-flammable): official sky-blue (하늘색) bag, put out after sunset.
- Food waste: remove liquid/foreign matter. Use designated food-waste bag in bin OR tap RFID card at the building's RFID food-waste bin.
- Mixed trash is illegal dumping (fine up to 1,000,000 KRW).
- Contact: Chuncheon City Resource Recycling Division, 033-250-3133.

TASK:
Analyze the uploaded image and respond in the language detected (default: English). 4-5 short, friendly sentences in this format:
- Item: [Identified item]
- Category: [Category, Korean term in parentheses]
- How to dispose: [1-3 concrete steps]
- Note: [Only if relevant, fine risk or dorm collection area reminder]
"""

if api_key:
    genai.configure(api_key=api_key, api_version="v1")
    model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

    uploaded_file = st.file_uploader("쓰레기 사진을 찍거나 올려주세요 (Take a photo or upload)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("분리수거 방법 확인하기 (Check How to Sort)", type="primary"):
            with st.spinner("Green Buddy가 춘천시 기준을 확인 중입니다..."):
                try:
                    response = model.generate_content([image, "How do I sort and throw this away in my dorm?"])
                    st.success("안내 완료!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
else:
    st.warning("진행하려면 Gemini API 키가 필요합니다.")
