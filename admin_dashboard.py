import streamlit as st
import os
import re
from collections import Counter
import zipfile
import io
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# --- 관리자 로그인 보호 ---
PASSWORD = "snapq1234"

st.set_page_config(page_title="SnapQ 관리자 대시보드", layout="wide")
st.title("🔐 SnapQ 관리자 로그인")

with st.form("login_form"):
    input_pwd = st.text_input("관리자 비밀번호를 입력하세요", type="password")
    submitted = st.form_submit_button("로그인")

if submitted:
    if input_pwd != PASSWORD:
        st.error("❌ 비밀번호가 틀렸습니다. 다시 시도하세요.")
        st.stop()
    else:
        st.success("✅ 로그인 성공! 관리자 대시보드를 불러옵니다.")

# --- 로그인 성공 시에만 실행 ---
if input_pwd == PASSWORD:

    # --- 함수들 ---
    def get_user_logs():
        files = os.listdir()
        users = set()
        for f in files:
            if f.startswith("wrong_log_") and f.endswith(".txt"):
                users.add(f.replace("wrong_log_", "").replace(".txt", ""))
        return sorted(users)

    def parse_wrong_log(user):
        filename = f"wrong_log_{user}.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            return 0, [], []
        total = content.count("❌ 문제 유형:")
        themes = re.findall(r"\[(.+?) - Lv\d\]", content)
        types = re.findall(r"문제 유형: (.+)", content)
        return total, themes, types

    def parse_vocab_log(user):
        filename = f"vocab_log_{user}.txt"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return 0
        words = [line.strip() for line in lines if line.strip() and not line.startswith("[") and not line.startswith("-")]
        return len(set(words))

    def delete_user_logs(user):
        removed = []
        for prefix in ["wrong_log_", "vocab_log_"]:
            filename = f"{prefix}{user}.txt"
            if os.path.exists(filename):
                os.remove(filename)
                removed.append(filename)
        return removed

    def create_backup_zip():
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in os.listdir():
                if filename.startswith("wrong_log_") or filename.startswith("vocab_log_"):
                    with open(filename, "r", encoding="utf-8") as f:
                        zf.writestr(filename, f.read())
        memory_zip.seek(0)
        return memory_zip

    # --- 대시보드 시작 ---
    st.title("🛠 SnapQ 관리자 리포트 + 기록 관리")

    users = get_user_logs()
    if not users:
        st.warning("⚠️ 분석 가능한 학생 기록이 없습니다.")
        st.stop()

    selected_user = st.selectbox("👤 학생 선택", users)
    view_all = st.checkbox("👥 전체 학생 비교 보기")

    if not view_all:
        st.header(f"📄 {selected_user} 님의 리포트")

        total_wrong, themes, types = parse_wrong_log(selected_user)
        total_vocab = parse_vocab_log(selected_user)

        st.metric("❌ 누적 오답 수", total_wrong)
        st.metric("📚 단어 저장 수", total_vocab)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🧭 지문 범주 TOP 3")
            for theme, count in Counter(themes).most_common(3):
                st.markdown(f"- {theme}: {count}회")

        with col2:
            st.markdown("### 🧠 문제 유형 통계")
            for t, count in Counter(types).items():
                st.markdown(f"- {t}: {count}회")

        st.markdown("---")
        with st.expander("🗑 기록 삭제 (관리자 전용)", expanded=False):
            confirm = st.checkbox(f"⚠️ {selected_user}의 모든 기록을 정말 삭제할까요?")
            if confirm:
                if st.button("❌ 기록 완전 삭제"):
                    removed_files = delete_user_logs(selected_user)
                    if removed_files:
                        st.success(f"✅ 삭제 완료: {', '.join(removed_files)}")
                        st.warning("⚠️ 새로고침 후 목록에서 사라집니다.")
                    else:
                        st.info("삭제할 파일이 없습니다.")

    else:
        st.header("📊 전체 학생 비교")

        summary_data = []
        for user in users:
            total_wrong, themes, types = parse_wrong_log(user)
            total_vocab = parse_vocab_log(user)
            summary_data.append({
                "학생": user,
                "오답 수": total_wrong,
                "단어 수": total_vocab
            })

        df = pd.DataFrame(summary_data)

        st.markdown("### 📋 학생별 통계 비교")
        st.dataframe(df)

        st.markdown("### 🔍 지문 범주별 오답 빈도")
        all_themes = []
        for user in users:
            _, themes, _ = parse_wrong_log(user)
            all_themes.extend(themes)

        for theme, count in Counter(all_themes).most_common(5):
            st.markdown(f"- {theme}: {count}회")

        st.markdown("### 🧠 전체 문제 유형 통계")
        all_types = []
        for user in users:
            _, _, types = parse_wrong_log(user)
            all_types.extend(types)

        for t, count in Counter(all_types).most_common():
            st.markdown(f"- {t}: {count}회")

        st.markdown("### 📊 그래프로 보는 비교")

        # 오답 수 그래프
        fig1, ax1 = plt.subplots()
        ax1.bar(df["학생"], df["오답 수"], color="salmon")
        ax1.set_title("학생별 누적 오답 수")
        st.pyplot(fig1)

        # 단어 수 그래프
        fig2 = px.bar(df, x="학생", y="단어 수", color="단어 수", color_continuous_scale="Blues", title="학생별 단어 저장 수")
        st.plotly_chart(fig2)

    # 선택 학생의 문제 유형 분포 (파이차트)
    if not view_all:
        type_counts = Counter(types)
        if type_counts:
            st.markdown("### 🧠 문제 유형 분포 (Pie Chart)")
            fig3 = px.pie(
                names=list(type_counts.keys()),
                values=list(type_counts.values()),
                title=f"{selected_user}의 문제 유형 비율"
            )
            st.plotly_chart(fig3)
        else:
            st.info("⚠️ 문제 유형 데이터가 부족합니다.")

    st.markdown("---")
    st.subheader("📦 전체 기록 백업 다운로드")

    if st.button("⬇️ 기록 백업 (ZIP 파일로 저장)"):
        zip_file = create_backup_zip()
        st.download_button(
            label="📁 ZIP 파일 다운로드",
            data=zip_file,
            file_name="snapq_backup.zip",
            mime="application/zip"
        )
