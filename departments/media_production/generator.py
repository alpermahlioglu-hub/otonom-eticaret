import os
import json

def icerik_uret():
    print("🎨 Medya ve İçerik Üretim Departmanı Çalışıyor...")
    
    rapor_dosyasi = "analiz_raporu.json"
    if not os.path.exists(rapor_dosyasi):
        print("⚠️ analiz_raporu.json bulunamadı, varsayılan verilerle devam ediliyor.")
        urunler = [
            {"id": "KDN-001", "ad": "Kişiselleştirilebilir Oversize Tişört"},
            {"id": "CB-001", "ad": "Organik Pamuklu Bebek Tulum Seti"}
        ]
    else:
        with open(rapor_dosyasi, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Rapor formatına göre ürün listesini çıkar
            urunler = data.get("urunler", [
                {"id": "KDN-001", "ad": "Kişiselleştirilebilir Oversize Tişört"},
                {"id": "CB-001", "ad": "Organik Pamuklu Bebek Tulum Seti"}
            ])

    medya_planı = []
    for urun in urunler:
        urun_ad = urun.get("ad", urun.get("urun_adi", "Trend Ürün"))
        medya_planı.append({
            "urun_id": urun.get("id", "N/A"),
            "urun_adi": urun_ad,
            "instagram_reels": f"🔥 Bu haftanın en çok satan Kadın/Çocuk trendi: {urun_ad}! Şık, konforlu ve indirimde. Link profilde! 🛒✨ #eticaret #trend",
            "tiktok_hook": f"Eğer hala {urun_ad} denemediysen çok şey kaçırıyorsun! 👇",
            "gorsel_konsept": f"Aydınlık stüdyo ortamında {urun_ad} ürününün minimalist ve estetik çekimi."
        })

    cikti_dosyasi = "medya_icerikleri.json"
    with open(cikti_dosyasi, "w", encoding="utf-8") as f:
        json.dump(medya_planı, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(medya_planı)} ürün için medya içerikleri üretildi ve '{cikti_dosyasi}' dosyasına kaydedildi.")
    return medya_planı

if __name__ == "__main__":
    icerik_uret()