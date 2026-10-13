import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
URUNLER_DOSYASI = BASE_DIR / "urunler.json"
RAPOR_DOSYASI = BASE_DIR / "PazarAnalizRaporu.xlsx"
JSON_RAPOR_DOSYASI = BASE_DIR / "analiz_raporu.json"

ONERILEN_TALEP_DURUMLARI = {"Yüksek", "Çok Yüksek", "Trend"}
MINIMUM_KAR_MARJI = 30.0


def tavsiye_olustur(kar_marji, talep_skoru):
    if kar_marji >= 100 and talep_skoru in ONERILEN_TALEP_DURUMLARI:
        return "YÜKSEK POTANSİYEL — Onay için güçlü aday"
    if kar_marji >= MINIMUM_KAR_MARJI and talep_skoru in ONERILEN_TALEP_DURUMLARI:
        return "İYİ FIRSAT — İnceleme ve onay önerilir"
    return "BEKLEMEDE — Kriterlerin altında veya talep belirsiz"


def urunleri_oku():
    if not URUNLER_DOSYASI.exists():
        raise FileNotFoundError(
            "urunler.json bulunamadı. Dosyanın proje ana klasöründe olduğundan emin olun."
        )

    with URUNLER_DOSYASI.open("r", encoding="utf-8") as dosya:
        return json.load(dosya)


def analiz_et(urunler):
    raporlar = []

    for urun in urunler:
        maliyet = float(urun["maliyet"])
        satis_fiyati = float(urun["satis_fiyati"])

        if maliyet <= 0:
            raise ValueError(f"Ürün {urun['id']} için maliyet 0'dan büyük olmalıdır.")

        net_kar = satis_fiyati - maliyet
        kar_marji = round((net_kar / maliyet) * 100, 2)
        talep_skoru = urun.get("talep_skoru", "Bilinmiyor")

        raporlar.append(
            {
                "Ürün ID": urun["id"],
                "Ürün Adı": urun["urun_adi"],
                "Kategori": urun["kategori"],
                "Maliyet (TL)": maliyet,
                "Satış Fiyatı (TL)": satis_fiyati,
                "Net Kâr (TL)": net_kar,
                "Kâr Marjı (%)": kar_marji,
                "Talep Durumu": talep_skoru,
                "Departman Tavsiyesi": tavsiye_olustur(kar_marji, talep_skoru),
                "Açıklama": urun["metin"],
                "Görsel URL": urun["gorsel_url"],
            }
        )

    return raporlar


def raporlari_kaydet(raporlar):
    tablo = pd.DataFrame(raporlar)
    tablo.to_excel(RAPOR_DOSYASI, index=False)

    with JSON_RAPOR_DOSYASI.open("w", encoding="utf-8") as dosya:
        json.dump(raporlar, dosya, ensure_ascii=False, indent=2)


def terminal_ozeti_yazdir(raporlar):
    print("\n--- PAZAR ANALİZ VE RAPORLAMA DEPARTMANI ---\n")

    for rapor in raporlar:
        print(f"Ürün ID: {rapor['Ürün ID']}")
        print(f"Ürün: {rapor['Ürün Adı']}")
        print(f"Net kâr: {rapor['Net Kâr (TL)']:.2f} TL")
        print(f"Kâr marjı: %{rapor['Kâr Marjı (%)']:.2f}")
        print(f"Talep: {rapor['Talep Durumu']}")
        print(f"Tavsiye: {rapor['Departman Tavsiyesi']}")
        print("-" * 55)

    print(f"\nExcel raporu hazır: {RAPOR_DOSYASI.name}")
    print(f"JSON raporu hazır: {JSON_RAPOR_DOSYASI.name}")
    print("Son karar sizdedir; sistem yalnızca analiz ve tavsiye üretir.\n")


def main():
    urunler = urunleri_oku()
    raporlar = analiz_et(urunler)
    raporlari_kaydet(raporlar)
    terminal_ozeti_yazdir(raporlar)


if __name__ == "__main__":
    main()