import os
import json
import pandas as pd
import google.generativeai as genai

# Gemini API Anahtarı Yapılandırması
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def pazar_analizi_yap():
    print("📈 Pazar İstihbarat & Trend Analizi Modülü Çalışıyor...")

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    Sen bir E-Ticaret Pazar Araştırma ve Trend Analiz Uzmanısın.
    Türkiye ve global e-ticaret pazarında şu an yüksek talep gören ve yüksek kâr marjına sahip 2 potansiyel ürün fikri belirle.

    Lütfen çıktıyı SADECE ve TAM OLARAK aşağıdaki JSON formatında ver (başka metin, açıklama veya markdown ekleme):
    {
      "urunler": [
        {
          "id": "KDN-001",
          "ad": "Kişiselleştirilebilir Oversize Tişört",
          "kategori": "Giyim & Moda",
          "hedef_kitle": "Gençler ve Sokak Modası Tutkunları",
          "tahmini_maliyet_tl": 150,
          "onerilen_satis_tl": 450,
          "trend_skoru": 92
        },
        {
          "id": "CB-001",
          "ad": "Organik Pamuklu Bebek Tulum Seti",
          "kategori": "Bebek & Çocuk",
          "hedef_kitle": "Yeni Ebeveynler",
          "tahmini_maliyet_tl": 200,
          "onerilen_satis_tl": 590,
          "trend_skoru": 88
        }
      ]
    }
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Markdown formatı temizliği (```json ... ```)
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        data = json.loads(raw_text.strip())
        urunler = data.get("urunler", [])

    except Exception as e:
        print(f"⚠️ Gemini API yanıtı işlenirken varsayılan verilere geçildi: {e}")
        urunler = [
            {
                "id": "KDN-001",
                "ad": "Kişiselleştirilebilir Oversize Tişört",
                "kategori": "Giyim & Moda",
                "hedef_kitle": "Gençler ve Sokak Modası Tutkunları",
                "tahmini_maliyet_tl": 150,
                "onerilen_satis_tl": 450,
                "trend_skoru": 92
            },
            {
                "id": "CB-001",
                "ad": "Organik Pamuklu Bebek Tulum Seti",
                "kategori": "Bebek & Çocuk",
                "hedef_kitle": "Yeni Ebeveynler",
                "tahmini_maliyet_tl": 200,
                "onerilen_satis_tl": 590,
                "trend_skoru": 88
            }
        ]

    # JSON Olarak Kaydet
    with open("analiz_raporu.json", "w", encoding="utf-8") as f:
        json.dump({"urunler": urunler}, f, ensure_ascii=False, indent=2)

    # Excel Raporu Oluştur (PazarAnalizRaporu.xlsx)
    df = pd.DataFrame(urunler)
    df.to_excel("PazarAnalizRaporu.xlsx", index=False)

    print(f"✅ Pazar analizi başarıyla tamamlandı. {len(urunler)} ürün 'analiz_raporu.json' ve 'PazarAnalizRaporu.xlsx' olarak kaydedildi.")
    return urunler

if __name__ == "__main__":
    pazar_analizi_yap()