import os
import json

# Departman Modülleri
from departments.market_intelligence.analyzer import pazar_analizi_yap
from departments.market_intelligence.competitor import rakip_fiyat_analizi_yap
from departments.media_production.generator import icerik_uret
from departments.media_production.seo_writer import seo_icerik_uret
from departments.ops_deployment.publisher import icerik_yayinla
from departments.ops_deployment.customer_support import musteri_destek_taslaklari_uret
from departments.ops_deployment.notifier import rapor_mail_gonder

def tum_sirketi_calistir():
    print("==================================================")
    print("🏢 OTONOM E-TİCARET ŞİRKETİ ORKESTRATÖRÜ BAŞLADI")
    print("==================================================")

    # 1. DEPARTMAN: Pazar İstihbaratı & Trend Analizi
    print("\n--- 1. ADIM: PAZAR ANALİZİ & İSTİHBARAT ---")
    try:
        pazar_analizi_yap()
    except Exception as e:
        print(f"⚠️ Pazar analizi geçici bir engelle karşılaştı: {e}")

    # 1.1 MODÜL: Rakip & Fiyat İstihbaratı
    print("\n--- 1.1 ADIM: RAKİP & DİNAMİK FİYAT ANALİZİ ---")
    rakip_fiyat_analizi_yap()

    # 2. DEPARTMAN: Medya & İçerik Üretimi
    print("\n--- 2. ADIM: MEDYA & İÇERİK ÜRETİMİ ---")
    icerik_uret()

    # 2.1 MODÜL: SEO Uyumlu Blog & İçerik Motoru
    print("\n--- 2.1 ADIM: SEO BLOG & MAKALE ÜRETİMİ ---")
    seo_icerik_uret()

    # 3. DEPARTMAN: Operasyon & Otomatik Yayın
    print("\n--- 3. ADIM: SOSYAL MEDYA & PAZARYERİ YAYINI ---")
    icerik_yayinla()

    # 3.1 MODÜL: Müşteri Destek & SSS Asistanı
    print("\n--- 3.1 ADIM: MÜŞTERİ DESTEK & SSS TASLAKLARI ---")
    musteri_destek_taslaklari_uret()

    # 4. DEPARTMAN: Bildirim & Yönetici Raporlaması
    print("\n--- 4. ADIM: YÖNETİCİ BİLDİRİMİ & BÜLTEN ---")
    rapor_mail_gonder(dosya_yolu="PazarAnalizRaporu.xlsx", alici_eposta="djalpermahlioglu@gmail.com")

    print("\n==================================================")
    print("🎉 TÜM DEPARTMANLAR UYUMLU ŞEKİLDE ÇALIŞTI VE SÜREÇ TAMAMLANDI")
    print("==================================================")

if __name__ == "__main__":
    tum_sirketi_calistir()