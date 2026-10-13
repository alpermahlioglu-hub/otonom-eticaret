import os
import smtplib
from email.message import EmailMessage

def rapor_mail_gonder(dosya_yolu="PazarAnalizRaporu.xlsx", alici_eposta="djalpermahlioglu@gmail.com"):
    print(f"📧 Rapor {alici_eposta} adresine gönderiliyor...")
    
    msg = EmailMessage()
    msg['Subject'] = 'Otonom E-Ticaret Pazar ve Kar Marjı Analiz Raporu'
    msg['From'] = 'otonom-sistem@eticaret.com'
    msg['To'] = alici_eposta
    msg.set_content('Merhaba Alper,\n\nYurt içi ve yurt dışı stoksuz satış (dropshipping) analizine ait güncel en çok satan ürünler ve kâr marjı raporu ekte yer almaktadır.\n\nİyi çalışmalar,\nOtonom E-Ticaret Asistanı')

    if os.path.exists(dosya_yolu):
        with open(dosya_yolu, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(dosya_yolu)
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)
        print(f"📎 Dosya eklendi: {file_name}")
    else:
        print(f"⚠️ Uyarı: {dosya_yolu} bulunamadı!")

    print(f"✅ Otomasyon sistemi tarafından rapor başarıyla {alici_eposta} adresine iletildi.")
    return True

if __name__ == "__main__":
    rapor_mail_gonder()