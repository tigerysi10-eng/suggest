
import streamlit as st
import os
from supabase import create_client

# 페이지 설정
st.set_page_config(
    page_title="한 줄 건의함",
    page_icon="💬"
)

st.title("💬 한 줄 건의함")
st.write("익명으로 자유롭게 의견을 남겨 주세요!")

# 환경 변수 불러오기
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Supabase 연결
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase 환경 변수가 설정되지 않았습니다.")
    st.stop()

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Supabase 연결 실패: {e}")
    st.stop()

# 건의 작성
st.subheader("건의 작성")

with st.form("suggestion_form"):
    content = st.text_input("건의 내용을 입력하세요.")

    category = st.selectbox(
        "건의 유형",
        ["기타", "시설", "수업", "급식", "학교생활"]
    )

    submit = st.form_submit_button("제출")

    if submit:
        if not content.strip():
            st.warning("빈 내용은 제출할 수 없습니다.")
        else:
            try:
                supabase.table("suggestions").insert({
                    "content": content.strip(),
                    "category": category,
                    "likes": 0
                }).execute()

                st.success("건의가 제출되었습니다!")
                st.rerun()

            except Exception as e:
                st.error(f"건의 저장 실패: {e}")

# 건의 목록
st.divider()
st.subheader("📋 건의 목록")

try:
    response = (
        supabase.table("suggestions")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    suggestions = response.data

    if suggestions:
        for item in suggestions:
            with st.container(border=True):
                st.write(f"**[{item['category']}]**")
                st.write(item["content"])

                st.caption(
                    f"작성일: {item['created_at']}"
                )

                col1, col2 = st.columns([1, 4])

                with col1:
                    st.write(f"👍 {item['likes']}")

                with col2:
                    if st.button(
                        "좋아요",
                        key=f"like_{item['id']}"
                    ):
                        try:
                            supabase.table("suggestions").update({
                                "likes": item["likes"] + 1
                            }).eq("id", item["id"]).execute()

                            st.rerun()

                        except Exception as e:
                            st.error(f"좋아요 처리 실패: {e}")

    else:
        st.info("아직 등록된 건의가 없습니다.")

except Exception as e:
    st.error(f"건의 목록을 불러오지 못했습니다: {e}")
