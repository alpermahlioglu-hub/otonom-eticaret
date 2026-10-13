import os
import json
from departments.market_intelligence.analyzer import pazar_analizi_yap

def ana_koordinator():
    print("========================================")
    print("OTONOM ŞİRKET KOORDİNATÖRÜ BAŞLADI")
    print("========================================")

    # 1. Adım: Pazar Analizi Yap ve Raporu Oluştur
    analiz_sonucu = pazar_analizi_yap()
    
    # 2. Adım: urunler.json verisini güvenli bir şekilde oku
    with open("urunler.json", "r", encoding="utf-8") as f:
        urunler = json.load(f)

    urun_idleri = [u["id"] for u in urunler]
    print(f"📦 İşlenen Ürün ID'leri: {urun_idleri}")
    print("✅ Koordinasyon döngüsü başarıyla tamamlandı.")

if __name__ == "__main__":
    ana_koordinator()