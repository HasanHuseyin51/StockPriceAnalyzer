from langchain_community.llms import Ollama

# Ollama modelini başlat
cached_llm = Ollama(model="llama3:latest")

# Genel sorular için Ollama modelini kullanarak cevap verme
def handle_general_question(query_text):
    response = cached_llm.invoke(f"Soru: {query_text}\nLütfen cevabınızı Türkçe verin.")
    return response.strip()
