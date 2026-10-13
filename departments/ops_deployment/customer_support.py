import os
import json
import google.generativeai as genai

# API Anahtarı Kurulumu
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def musteri_destek_taslaklari_uret():
    print("🎧 Akıllı Müşteri Destek & SSS Asistanı Çalışıyor...")

    analiz_dosyasi = "analiz_raporu.json"
    if not os.path.exists(analiz_dosyasi):
        print("⚠️ analiz_raporu.json bulunamadı. Varsayılan SSS taslağı hazırlanıyor.")
        urunler = [{"ad": "Kişiselleştirilebilir Oversize Tişört"}]
    else:
        with open(analiz_dosyasi, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                urunler = data.get("urunler", [])
            except Exception:
                urunler = [{"ad": "Trend E-Ticaret Ürünü"}]

    model = genai.GenerativeModel('gemini-1.5-flash')
    destek_rehberleri = []

    for urun in urunler:
        urun_adi = urun.get("ad", urun.get("urun_adi", "Trend Ürün"))

        prompt = f"""
        Sen e-ticaret müşteri ilişkileri ve destek ekibi yöneticisisin.
        Aşağıdaki ürün için müşterilerden gelebilecek muhtemel 3 soruyu ve bunlara verilecek son derece kurumsal, nazik ve çözüm odaklı yanıtları hazırla:

        Ürün Adı: {urun_adi}

        Çıktıyı tam olarak şu JSON formatında ver (başka metin ekleme):
        {{
            "urun_adi": "{urun_adi}",
            "sss_listesi": [
                {{"soru": "Örnek soru 1?", "yanit": "Kurumsal yanıt 1"}},
                {{"soru": "Örnek soru 2?", "yanit": "Kurumsal yanıt 2"}},
                {{"soru": "Örnek soru 3?", "yanit": "Kurumsal yanıt 3"}}
            ],
            "genel_iade_kargo_notu": "Kargo ve iade süreçleriyle ilgili standart mesaj."
        }}
        """

        try:
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # JSON Temizliği
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            json_data = json.loads(raw_text.strip())
            destek_rehberleri.append(json_data)
        except Exception as e:
            print(f"⚠️ {urun_adi} için müşteri destek taslağı üretilirken hata oluştu: {e}")
            destek_rehberleri.append({
                "urun_adi": urun_adi,
                "sss_listesi": [
                    {"soru": "Kargo ne zaman ulaşır?", "yanit": "Siparişiniz 1-3 iş günü içerisinde kargoya verilir."},
                    {"soru": "İade yapabilir miyim?", "yanit": "14 gün içerisinde sebep belirtmeksizin iade edebilirsiniz."}
                ],
                "genel_iade_kargo_notu": "Tüm ürünlerimiz garantilidir."
            })

    cikti_dosyasi = "musteri_destek_rehberi.json"
    with open(cikti_dosyasi, "w", encoding="utf-8") as f:
        json.dump(destek_rehberleri, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(destek_rehberleri)} ürün için müşteri destek rehberi oluşturuldu ve '{cikti_dosyasi}' dosyasına kaydedildi.")
    return destek_rehberleri

if __name__ == "__main__":
    musteri_destek_taslaklari_uret()