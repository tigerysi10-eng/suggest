
import streamlit as st

st.title("한 줄 건의함")
st.write("자유롭게 의견을 남겨 주세요!")

if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

with st.form("suggestion_form"):
    suggestion = st.text_input("건의 내용을 입력하세요.")
    submit = st.form_submit_button("제출")

    if submit:
        if suggestion.strip() == "":
            st.warning("빈 내용은 제출할 수 없습니다.")
        else:
            st.session_state.suggestions.insert(0, suggestion.strip())
            st.success("건의가 제출되었습니다!")

st.subheader("건의 목록")

if st.session_state.suggestions:
    for i, item in enumerate(st.session_state.suggestions, 1):
        st.write(f"{i}. {item}")
else:
    st.write("아직 등록된 건의가 없습니다.")
