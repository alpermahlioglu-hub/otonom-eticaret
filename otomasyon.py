import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from gtts import gTTS
import pandas as pd
import imageio_ffmpeg

OUTPUT_DIR = Path("outputs")
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "videos"
DATA_DIR = Path("data")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def urunleri_yukle():
    rapor_yolu = Path("analiz_raporu.json")
    if not rapor_yolu.exists():
        print(f"Hata: {rapor_yolu} bulunamadı!")
        return []
    
    with open(rapor_yolu, "r", encoding="utf-8") as f:
        try:
            veri = json.load(f)
            if isinstance(veri, list):
                return veri
            elif isinstance(veri, dict) and "urunler" in veri:
                return veri["urunler"]
            return []
        except Exception as e:
            print(f"JSON okuma hatası: {e}")
            return []

async def ses_uret(metin, dosya_yolu):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: gTTS(text=metin, lang='tr', slow=False).save(str(dosya_yolu)))

async def video_uret(urun):
    urun_id = urun.get("id", 1)
    urun_adi = urun.get("urun_adi", "Popüler Ürün")
    aciklama = urun.get("pazarlama_metni", f"{urun_adi} şimdi stoklarda!")
    
    print(f"\n--- ÜRETİM BAŞLADI: {urun_id} | {urun_adi} ---")
    
    ses_dosyasi = AUDIO_DIR / f"{urun_id}_ses.mp3"
    video_dosyasi = VIDEO_DIR / f"{urun_id}_{urun_adi.replace(' ', '_')}.mp4"
    
    print("1/3 Seslendirme hazırlanıyor...")
    ses_metni = f"Dikkat! {urun_adi}. {aciklama} Kaçırılmayacak fırsat!"
    await ses_uret(ses_metni, ses_dosyasi)
    
    print("2/3 Görsel arkaplan oluşturuluyor...")
    gecici_arkaplan = AUDIO_DIR / f"{urun_id}_bg.mp4"
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd_bg = [
        ffmpeg_path, "-y",
        "-f", "lavfi",
        "-i", "color=c=navy:s=1080x1920:r=30",
        "-t", "5",
        str(gecici_arkaplan)
    ]
    
    process = await asyncio.create_subprocess_exec(*cmd_bg, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.communicate()
    
    print("3/3 Video ve ses birleştiriliyor...")
    cmd_mux = [
        ffmpeg_path, "-y",
        "-i", str(gecici_arkaplan),
        "-i", str(ses_dosyasi),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(video_dosyasi)
    ]
    
    process_mux = await asyncio.create_subprocess_exec(*cmd_mux, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process_mux.communicate()
    
    print(f"Başarıyla Üretildi: {video_dosyasi}")

async def main(urun_idleri):
    print("\n--- İÇERİK VE VİDEO ÜRETİM DEPARTMANI ---")
    print(f"Patron onayı alındı. Seçilen ürün ID'leri: {urun_idleri}")
    
    urunler = urunleri_yukle()
    if not urunler:
        print("İşlenecek ürün bulunamadı.")
        return

    for uid in urun_idleri:
        bulunan = None
        for u in urunler:
            if str(u.get("id")) == str(uid):
                bulunan = u
                break
        
        if bulunan:
            await video_uret(bulunan)
        else:
            print(f"Uyarı: ID {uid} listede bulunamadı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Otonom E-Ticaret Video Üretim Botu")
    parser.add_argument("urun_idleri", nargs="+", help="İşlenecek ürün ID'leri")
    args = parser.parse_args()
    
    asyncio.run(main(args.urun_idleri))