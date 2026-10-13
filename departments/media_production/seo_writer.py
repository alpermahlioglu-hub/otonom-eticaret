import os
import json
import google.generativeai as genai

# API Anahtarı Kurulumu
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def seo_icerik_uret():
    print("📝 SEO & Blog Trafik Motoru Çalışıyor...")

    analiz_dosyasi = "analiz_raporu.json"
    if not os.path.exists(analiz_dosyasi):
        print("⚠️ analiz_raporu.json bulunamadı. Varsayılan konuyla SEO içeriği üretiliyor.")
        urunler = [{"ad": "Kişiselleştirilebilir Oversize Tişört", "hedef_kitle": "Gençler ve Sokak Modası Tutkunları"}]
    else:
        with open(analiz_dosyasi, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                urunler = data.get("urunler", [])
            except Exception:
                urunler = [{"ad": "Trend E-Ticaret Ürünü", "hedef_kitle": "Genel Alıcı Kitle"}]

    model = genai.GenerativeModel('gemini-1.5-flash')
    seo_makaleleri = []

    for urun in urunler:
        urun_adi = urun.get("ad", urun.get("urun_adi", "Trend Ürün"))
        hedef_kitle = urun.get("hedef_kitle", "E-ticaret Müşterileri")

        prompt = f"""
        Sen kıdemli bir E-Ticaret SEO ve İçerik Pazarlama Uzmanısın.
        Aşağıdaki ürün için Google arama motorunda organik üst sıralara çıkacak SEO uyumlu bir blog/makale içeriği tasarla:

        Ürün Adı: {urun_adi}
        Hedef Kitle: {hedef_kitle}

        Lütfen çıktıyı tam olarak şu JSON formatında ver (başka açıklama veya ekstra metin yazma):
        {{
            "urun_adi": "{urun_adi}",
            "seo_baslik": "Arama motoru uyumlu ilgi çekici başlık (Max 60 karakter)",
            "meta_aciklama": "Google arama sonuçlarında görünecek meta açıklama (Max 155 karakter)",
            "anahtar_kelimeler": ["kelime1", "kelime2", "kelime3", "kelime4"],
            "blog_icerik_html": "<h2>Giriş Başlığı</h2><p>Paragraf metni...</p><h3>Neden Tercih Edilmeli?</h3><p>İçerik...</p>"
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
            seo_makaleleri.append(json_data)
        except Exception as e:
            print(f"⚠️ {urun_adi} için SEO içeriği üretilirken hata oluştu: {e}")
            seo_makaleleri.append({
                "urun_adi": urun_adi,
                "seo_baslik": f"{urun_adi} İncelemesi ve Trendler",
                "meta_aciklama": f"En yeni {urun_adi} modelleri ve fiyatları için hemen sitemizi ziyaret edin.",
                "anahtar_kelimeler": [urun_adi, "e-ticaret", "satın al"],
                "blog_icerik_html": f"<h2>{urun_adi} Kalitesi</h2><p>Detaylı bilgi için sitemizi inceleyin.</p>"
            })

    cikti_dosyasi = "seo_blog_icerikleri.json"
    with open(cikti_dosyasi, "w", encoding="utf-8") as f:
        json.dump(seo_makaleleri, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(seo_makaleleri)} ürün için SEO makalesi üretildi ve '{cikti_dosyasi}' dosyasına kaydedildi.")
    return seo_makaleleri

if __name__ == "__main__":
    seo_icerik_uret()