import os
import json
import time
from google import genai
from google.genai.errors import ServerError

def pazar_analizi_yap():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY ortam değişkeni bulunamadı!")

    client = genai.Client(api_key=api_key)

    urunler_dosya_yolu = "urunler.json"
    if not os.path.exists(urunler_dosya_yolu):
        raise FileNotFoundError("urunler.json dosyası bulunamadı!")

    with open(urunler_dosya_yolu, "r", encoding="utf-8") as f:
        urunler_veri = json.load(f)

    print("📊 Pazar Analizi Başlatılıyor (Kadın & Çocuk/Bebek Kategorileri)...")

    prompt = f"""
    Sen uzman bir e-ticaret pazar analistisin.
    Aşağıdaki ürün verilerini analiz et:
    {json.dumps(urunler_veri, ensure_ascii=False, indent=2)}

    Lütfen her ürün için:
    1. Fiyat ve rekabet değerlendirmesi yap.
    2. Şikayetlerden yola çıkarak aksiyon önerisi sun.
    3. Pazarlama ve içerik stratejisi belirle.

    Yanıtını sadece geçerli bir JSON formatında döndür.
    """

    max_deneme = 3
    for deneme in range(1, max_deneme + 1):
        try:
            print(f"🔄 Model bağlantısı deneniyor (Deneme {deneme}/{max_deneme})...")
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )

            analiz_sonucu = response.text
            
            rapor_dosyasi = "analiz_raporu.json"
            with open(rapor_dosyasi, "w", encoding="utf-8") as f:
                f.write(analiz_sonucu)

            print("✅ Pazar analizi başarıyla tamamlandı ve 'analiz_raporu.json' dosyasına kaydedildi.")
            return analiz_sonucu

        except ServerError as e:
            print(f"⚠️ Sunucu yoğunluğu (503): {e}")
            if deneme < max_deneme:
                print("⏳ 5 saniye bekleyip tekrar denenecek...")
                time.sleep(5)
            else:
                print("❌ Maksimum deneme sınırına ulaşıldı.")
                raise e
        except Exception as e:
            print(f"❌ Beklenmeyen bir hata oluştu: {e}")
            raise e

if __name__ == "__main__":
    pazar_analizi_yap()