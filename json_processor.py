import json
from datetime import datetime

# JSON tarih formatını insan tarafından anlaşılabilir hale çevirme fonksiyonu
def parse_json_date(json_date):
    timestamp = int(json_date[6:16])  # "/Date(1718053200000+0300)/" formatını işlemek için
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')

# JSON dosyasını oku ve verileri filtrele
def load_json_data(uploaded_json_file):
    try:
        # Dosyayı doğrudan bellekte oku
        json_data = json.load(uploaded_json_file)
        filtered_data = json_data.get("GetIMKBStocksClosePriceResult", [])
        return filtered_data, None
    except Exception as e:
        return None, str(e)

# JSON verisinden hisse kodu ve tarih çekme
def extract_stock_code_and_date(query, filtered_data):
    query = query.lower()
    possible_codes = [stock.get('Stock_Code', '').lower() for stock in filtered_data if stock.get('Stock_Code')]

    for code in possible_codes:
        if code in query:
            date = None
            for word in query.split():
                if word.count("/") == 2:  # Tarih formatı kontrolü
                    date = word
            return code.upper(), date  # Büyük harflerle hisse kodunu geri döndür
    return None, None

# JSON verisinden hisse koduna ve tarihe göre veriyi bulma fonksiyonu
def find_stock_data(filtered_data, stock_code, date=None):
    relevant_data = [stock for stock in filtered_data if stock.get('Stock_Code') == stock_code]

    if date:
        relevant_data = [stock for stock in relevant_data if parse_json_date(stock.get('Date', '')) == date]

    if not relevant_data:
        return f"{stock_code} için veri bulunamadı."  # Eğer veri yoksa kullanıcıya bildirelim
    return relevant_data

# İşlem hacmi verilerini bulma ve ortalama hesaplama fonksiyonu
def calculate_average_volume(filtered_data, stock_code, days=7):
    relevant_data = find_stock_data(filtered_data, stock_code)

    if not relevant_data:
        return f"{stock_code} hisse senedi için yeterli veri bulunamadı."
    
    # İşlem hacmi bilgilerini çekip ortalama hesaplama
    volumes = [stock.get('Volume', 0) for stock in relevant_data[:days] if 'Volume' in stock]
    if not volumes:
        return f"{stock_code} hisse senedi için işlem hacmi bilgisi bulunamadı."
    
    average_volume = sum(volumes) / len(volumes)
    return f"{stock_code} hisse senedinin son {days} gündeki ortalama işlem hacmi: {average_volume}"
