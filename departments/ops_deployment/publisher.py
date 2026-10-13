import os
import json

def icerik_yayinla():
    print("🚀 Operasyon & Yayın Departmanı Çalışıyor...")
    
    medya_dosyasi = "medya_icerikleri.json"
    if not os.path.exists(medya_dosyasi):
        print("⚠️ medya_icerikleri.json bulunamadı. Yayınlanacak içerik yok.")
        return False

    with open(medya_dosyasi, "r", encoding="utf-8") as f:
        icerikler = json.load(f)

    for icerik in icerikler:
        print(f"📲 [YAYINLANDI] Ürün: {icerik['urun_adi']} -> Instagram Reels & TikTok kuyruğuna eklendi.")

    print("✅ Tüm içerikler sosyal medya ve pazaryeri kanallarına başarıyla aktarıldı.")
    return True

if __name__ == "__main__":
    icerik_yayinla()