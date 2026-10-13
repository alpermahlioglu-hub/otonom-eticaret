import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

def rapor_eposta_gonder():
    print("[OpsDeployment] E-posta bildirim servisi başlatılıyor...")
    
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    
    if not sender_email or not sender_password or not receiver_email:
        print("[OpsDeployment] Uyarı: E-posta ortam değişkenleri (SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL) eksik. Mail gönderimi atlanıyor.")
        return

    msg = EmailMessage()
    msg['Subject'] = '📊 Otonom E-Ticaret Günlük Pazar Analiz Raporu'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msg.set_content(
        "Merhaba,\n\n"
        "Otonom e-ticaret şirketinizin yapay zeka pazar analizi ve medya üretim departmanları günlük görevlerini başarıyla tamamlamıştır.\n\n"
        "Ekli dosyada güncel Pazar Analiz Raporu (Excel) bulunmaktadır.\n\n"
        "İyi çalışmalar,\nOtonom Şirket Koordinatörü"
    )
    
    excel_yolu = Path("PazarAnalizRaporu.xlsx")
    if excel_yolu.exists():
        with open(excel_yolu, "rb") as f:
            file_data = f.read()
            file_name = excel_yolu.name
        msg.add_attachment(file_data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=file_name)
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("[OpsDeployment] Pazar analiz raporu e-posta olarak başarıyla gönderildi!")
    except Exception as e:
        print(f"[OpsDeployment] E-posta gönderilirken hata oluştu: {e}")

if __name__ == "__main__":
    rapor_eposta_gonder()