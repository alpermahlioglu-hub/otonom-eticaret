import os
import json
import asyncio
from pathlib import Path
from gtts import gTTS
import imageio_ffmpeg

OUTPUT_DIR = Path("outputs")
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "videos"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

async def ses_uret(metin, dosya_yolu):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: gTTS(text=metin, lang='tr', slow=False).save(str(dosya_yolu)))

async def medya_uret(urun_idleri=None):
    print("[MediaProduction] Medya üretim departmanı devreye girdi...")
    rapor_yolu = Path("analiz_raporu.json")
    if not rapor_yolu.exists():
        print("Hata: analiz_raporu.json bulunamadı!")
        return
    
    with open(rapor_yolu, "r", encoding="utf-8") as f:
        urunler = json.load(f)
        
    for urun in urunler:
        uid = str(urun.get("id"))
        if urun_idleri and uid not in [str(x) for x in urun_idleri]:
            continue
            
        urun_adi = urun.get("urun_adi", "Ürün")
        aciklama = urun.get("pazarlama_metni", "")
        
        ses_dosyasi = AUDIO_DIR / f"{uid}_ses.mp3"
        video_dosyasi = VIDEO_DIR / f"{uid}_{urun_adi.replace(' ', '_')}.mp4"
        
        print(f"[MediaProduction] İşleniyor: {urun_adi}")
        
        ses_metni = f"Dikkat! {urun_adi}. {aciklama}"
        await ses_uret(ses_metni, ses_dosyasi)
        
        gecici_bg = AUDIO_DIR / f"{uid}_bg.mp4"
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        cmd_bg = [
            ffmpeg_path, "-y", "-f", "lavfi",
            "-i", "color=c=navy:s=1080x1920:r=30",
            "-t", "5", str(gecici_bg)
        ]
        proc = await asyncio.create_subprocess_exec(*cmd_bg, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()
        
        cmd_mux = [
            ffmpeg_path, "-y",
            "-i", str(gecici_bg),
            "-i", str(ses_dosyasi),
            "-c:v", "copy", "-c:a", "aac",
            "-shortest", str(video_dosyasi)
        ]
        proc_mux = await asyncio.create_subprocess_exec(*cmd_mux, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc_mux.communicate()
        print(f"[MediaProduction] Üretildi: {video_dosyasi}")

if __name__ == "__main__":
    import sys
    ids = sys.argv[1:] if len(sys.argv) > 1 else None
    asyncio.run(medya_uret(ids))