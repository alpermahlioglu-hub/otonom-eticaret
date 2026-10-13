import os
import json
import random

def rakip_fiyat_analizi_yap():
    print("🔍 Rakip & Fiyat İstihbarat Modülü Çalışıyor...")
    
    analiz_dosyasi = "analiz_raporu.json"
    if not os.path.exists(analiz_dosyasi):
        print("⚠️ analiz_raporu.json bulunamadı. Varsayılan ürünlerle rakip analizi yapılıyor.")
        urunler = [
            {"id": "KDN-001", "ad": "Kişiselleştirilebilir Oversize Tişört", "maliyet": 150},
            {"id": "CB-001", "ad": "Organik Pamuklu Bebek Tulum Seti", "maliyet": 200}
        ]
    else:
        with open(analiz_dosyasi, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                urunler = data.get("urunler", [])
            except Exception:
                urunler = []

    rakip_analiz_sonuclari = []

    for urun in urunler:
        urun_ad = urun.get("ad", urun.get("urun_adi", "Trend Ürün"))
        maliyet = urun.get("tahmini_maliyet_tl", 150)
        
        # Rakip pazaryeri fiyat simülasyonu / taranması
        rakip_fiyat_1 = round(maliyet * random.uniform(1.8, 2.5), 2)
        rakip_fiyat_2 = round(maliyet * random.uniform(2.0, 2.8), 2)
        ortalama_rakip_fiyat = round((rakip_fiyat_1 + rakip_fiyat_2) / 2, 2)
        
        # Rekabetçi dinamik satış fiyatı (Rakipten %5 daha uygun ama yüksek kâr marjlı)
        onerilen_satis_fiyati = round(ortalama_rakip_fiyat * 0.95, 2)
        net_kar = round(onerilen_satis_fiyati - maliyet, 2)

        rakip_analiz_sonuclari.append({
            "urun_id": urun.get("id", "N/A"),
            "urun_adi": urun_ad,
            "maliyet_tl": maliyet,
            "rakip_pazaryeri_1_tl": rakip_fiyat_1,
            "rakip_pazaryeri_2_tl": rakip_fiyat_2,
            "ortalama_rakip_fiyati_tl": ortalama_rakip_fiyat,
            "bizim_onerilen_fiyat_tl": onerilen_satis_fiyati,
            "tahmini_net_kar_tl": net_kar
        })

    cikti_dosyasi = "rakip_fiyat_raporu.json"
    with open(cikti_dosyasi, "w", encoding="utf-8") as f:
        json.dump(rakip_analiz_sonuclari, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(rakip_analiz_sonuclari)} ürün için rakip fiyat analizi tamamlandı ve '{cikti_dosyasi}' dosyasına kaydedildi.")
    return rakip_analiz_sonuclari

if __name__ == "__main__":
    rakip_fiyat_analizi_yap()