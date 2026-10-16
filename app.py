import streamlit as st
import base64
from openai import OpenAI

st.set_page_config(
    page_title="Real LooksMax AI",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 Real LooksMax AI")
st.markdown("Analiz vneshnosti cherez GPT-4o.")

# Vvedi klyuch tut ili v boku
api_key = st.sidebar.text_input("OpenAI API Key:", value="", type="password")

uploaded_file = st.file_uploader("Zagruzi foto litsa", type=["jpg", "jpeg", "png"])

if uploaded_file and api_key:
    st.image(uploaded_file, caption="Tvoyo foto", use_column_width=True)
    
    if st.button("🚀 Zapustit analiz"):
        client = OpenAI(api_key=api_key)
        
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        
        # Ispolzuem prostoy i chistyy tekst
        prompt = (
            "Analyze this photo from a style, grooming, and visual aesthetics perspective. "
            "Evaluate facial symmetry, jawline structure, skin texture, and haircut. "
            "Provide a structured looksmaxing guide with steps for 1 month, 3 months, and 6 months. "
            "Keep the tone direct, motivating, and professional."
        )

        with st.spinner("Obrabotka..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=1000,
                )
                
                result_text = response.choices[0].message.content
                st.success("Gotovo!")
                st.markdown(result_text)

            except Exception as e:
                st.error(f"Oshibka: {e}")

elif uploaded_file and not api_key:
    st.warning("⚠️ Vvedi API Key.")
