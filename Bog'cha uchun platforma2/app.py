import streamlit as st
import os
import base64
from main import (bazani_sozlash, kitob_tahrirlash, kitob_ochirish, 
                  get_connection, foydalanuvchi_qoshish, login_qilish)

st.set_page_config(page_title="Kutubxona", layout="centered")

# Dizayn
st.markdown("""
<style>
    h1, h2, h3 { color: #D35400 !important; }
    div.stButton > button { background-color: #D35400; color: white !important; border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("📚 Kutubxona Tizimi")
bazani_sozlash()

# Session State orqali foydalanuvchini eslab qolish
if 'user' not in st.session_state:
    st.session_state.user = None

# 1. Login va Ro'yxatdan o'tish oynasi
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Kirish", "Ro'yxatdan o'tish"])
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Parol", type="password", key="login_p")
        if st.button("Kirish"):
            user_data = login_qilish(u, p)
            if user_data:
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Username yoki parol xato!")
                
    with tab2:
        u_new = st.text_input("Yangi Username", key="reg_u")
        p_new = st.text_input("Yangi Parol", type="password", key="reg_p")
        if st.button("Ro'yxatdan o'tish"):
            if foydalanuvchi_qoshish(u_new, p_new):
                st.success("Muvaffaqiyatli ro'yxatdan o'tdingiz! Endi kiring.")
            else:
                st.error("Bu username allaqachon band!")
else:
    # 2. Tizimga kirgandan keyingi menyu
    st.sidebar.write(f"👤 Xush kelibsiz, **{st.session_state.user}**!")
    if st.sidebar.button("Chiqish"):
        st.session_state.user = None
        st.rerun()
        
    menu = st.sidebar.selectbox("Menyu", ["Kitob qo'shish", "Kitoblar ro'yxati"])
    conn = get_connection()
    
    if menu == "Kitob qo'shish":
        st.subheader("Yangi kitob qo'shish")
        with st.form("add_form"):
            n = st.text_input("Kitob nomi")
            a = st.text_input("Muallif")
            f = st.file_uploader("PDF yuklash", type="pdf")
            if st.form_submit_button("Saqlash"):
                if n and a and f:
                    os.makedirs("pdfs", exist_ok=True)
                    p = f"pdfs/{f.name}"
                    with open(p, "wb") as file: file.write(f.getbuffer())
                    with conn:
                        conn.execute("INSERT INTO kitoblar (nomi, muallif, pdf_path) VALUES (?, ?, ?)", (n, a, p))
                    st.success("Kitob qo'shildi!")
                    st.rerun()

    elif menu == "Kitoblar ro'yxati":
        st.subheader("📚 Fonddagi kitoblar")
        kitoblar = conn.execute("SELECT * FROM kitoblar").fetchall()
        for k in kitoblar:
            with st.expander(f"📖 {k[1]} - {k[2]}"):
                if k[3] and os.path.exists(k[3]):
                    with open(k[3], "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px"></iframe>'
                    if st.button(f"📖 {k[1]}ni o'qish", key=f"read_{k[0]}"):
                        st.markdown(pdf_display, unsafe_allow_html=True)