import streamlit as st
from json_processor import load_json_data, extract_stock_code_and_date, calculate_average_volume
from csv_processor import process_csv
from ollama_handler import handle_general_question

st.title("LLaMA3 Destekli JSON ve CSV İşlem Asistanı")

# JSON dosyasını yükle
uploaded_json_file = st.file_uploader("JSON dosyasını yükleyin", type=["json"])
if uploaded_json_file is not None:
    filtered_data, error = load_json_data(uploaded_json_file)
    if error:
        st.error(f"JSON dosyası yüklenirken bir hata oluştu: {error}")
    else:
        st.success("JSON dosyası yüklendi!")

# CSV dosyasını yükle
uploaded_csv_file = st.file_uploader("CSV dosyasını yükleyin", type=["csv"])
if uploaded_csv_file is not None and uploaded_json_file is not None:
    process_csv(uploaded_csv_file, lambda question: handle_general_question(question))
    st.success("CSV dosyası işlendi ve cevaplar eklendi!")

# Soru sorma alanı
st.header("Soru Sorun")
user_question = st.text_input("Sorunuzu buraya yazın:")

# Soruyu işleme ve cevap verme
if st.button("Soruyu Sor"):
    if uploaded_json_file is None:
        st.warning("Lütfen önce bir JSON dosyası yükleyin.")
    elif user_question:
        # JSON verisinden hisse kodu ve tarih bilgisi çekme
        stock_code, date = extract_stock_code_and_date(user_question, filtered_data)
        
        if stock_code:
            # Eğer hisse kodu ve tarih varsa veriyi bulup gösterelim
            relevant_data = calculate_average_volume(filtered_data, stock_code)
            st.write(f"Sonuç: {relevant_data}")
        else:
            # Ollama ile genel soruya cevap verelim
            response = handle_general_question(user_question)
            st.write(f"Ollama cevabı: {response}")
    else:
        st.warning("Lütfen bir soru girin.")
