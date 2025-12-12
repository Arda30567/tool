# Python Toolbox - Profesyonel Araç Seti

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows-blue)

## 📋 İçindekiler
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Araçlar](#araçlar)
- [Lisans](#lisans)
- [Deploy](#deploy)

---

## ✨ Özellikler

### 🚀 6 Ana Kategori - 30+ Araç

#### 1. **PDF Araçları**
- ✅ PDF Birleştirme
- ✅ PDF Ayırma
- ✅ PDF → JPG Dönüştürme
- ✅ JPG → PDF Dönüştürme
- ✅ PDF Sıkıştırma
- ✅ Filigran Ekleme (Metin/Görsel)

#### 2. **QR & Barkod Araçları**
- ✅ QR Kod Üretme
- ✅ QR Kod Çözme
- ✅ Toplu QR Üretme (CSV'den)
- ✅ Barkod Üretme (EAN13, CODE128)
- ✅ WiFi QR Kodu
- ✅ Telefon QR Kodu

#### 3. **Görsel Araçları**
- ✅ Toplu Görsel Dönüştürme
- ✅ Toplu Yeniden Boyutlandırma
- ✅ Toplu Filigran Ekleme
- ✅ Çözünürlük Okuma
- ✅ Optimize Etme

#### 4. **Dosya Dönüştürücüler**
- ✅ Excel → JSON
- ✅ JSON → Excel
- ✅ CSV → Excel
- ✅ TXT → PDF
- ✅ Word → PDF

#### 5. **Sistem Araçları**
- ✅ MD5, SHA256 Hash Üretme
- ✅ Dosya Şifreleme (AES)
- ✅ ZIP → Şifreli ZIP
- ✅ Dosya Bilgisi
- ✅ Secure Password Generator

#### 6. **İnternet Araçları**
- ✅ YouTube Thumbnail İndirici
- ✅ URL Kısaltıcı
- ✅ İnternet Hız Testi
- ✅ Web Sitesi Durum Kontrolü
- ✅ IP Adresi Görüntüleme

---

## 🛠️ Kurulum

### Gerekli Sistem Gereksinimleri
- Python 3.8 veya üzeri
- Windows 10/11 (EXE versiyonu için)
- 500 MB boş disk alanı

### Python ile Kurulum
```bash
# 1. Projeyi klonlayın
git clone https://github.com/yourusername/python_toolbox.git
cd python_toolbox

# 2. Gerekli paketleri yükleyin
pip install -r requirements.txt

# 3. Uygulamayı çalıştırın
python app.py
```

### Windows EXE ile Kullanım
1. [Releases](https://github.com/yourusername/python_toolbox/releases) sayfasından EXE dosyasını indirin
2. `PythonToolbox.exe` dosyasını çalıştırın
3. İlk çalıştırmada Windows Defender uyarısı gelebilir
4. "Daha fazla bilgi" -> "Çalıştır" diyerek devam edin

---

## 🎯 Kullanım

### Arayüz
- **Sol Panel**: Araç kategorileri
- **Ana Alan**: Seçili aracın ayarları
- **Menü Çubuğu**: Dosya ve yardım menüleri
- **Durum Çubuğu**: İşlem ilerlemesi ve bilgiler

### Temel Kullanım Adımları
1. Soldan bir araç kategorisi seçin
2. Sekmelerden işlem türünü belirleyin
3. Gerekli dosyaları/dosyaları seçin
4. Parametreleri ayarlayın
5. "Başlat" butonuna tıklayın

### Sürükle & Bırak Desteği
- PDF dosyalarını sıralı birleştirme
- Görsel dosyaları toplu işleme
- CSV dosyaları toplu QR üretme

---

## 🔧 Araçlar

### PDF Araçları
```python
from tools.pdf_tools import PDFTools

pdf_tools = PDFTools()

# PDF Birleştirme
pdf_tools.merge_pdfs(['file1.pdf', 'file2.pdf'], 'output.pdf')

# PDF Ayırma
pdf_tools.split_pdf('input.pdf', 'output_dir', split_type="pages")

# PDF → JPG
pdf_tools.pdf_to_jpg('input.pdf', 'output_dir', dpi=300)

# JPG → PDF
pdf_tools.jpg_to_pdf(['image1.jpg', 'image2.jpg'], 'output.pdf')

# PDF Sıkıştırma
pdf_tools.compress_pdf('input.pdf', 'output.pdf')

# Filigran Ekleme
pdf_tools.add_watermark_text('input.pdf', 'output.pdf', 'WATERMARK TEXT')
```

### QR & Barkod Araçları
```python
from tools.qr_tools import QRTools

qr_tools = QRTools()

# QR Kod Üretme
qr_tools.generate_qr('https://example.com', 'qr.png')

# WiFi QR Kodu
qr_tools.generate_wifi_qr('MyWiFi', 'password123', 'wifi_qr.png')

# QR Kod Okuma
qr_tools.read_qr('qr_image.png')

# Barkod Üretme
qr_tools.generate_barcode('1234567890123', 'EAN13', 'barcode.png')

# Toplu QR (CSV'den)
qr_tools.batch_generate_qr('data.csv', 'output_dir')
```

### Görsel Araçları
```python
from tools.image_tools import ImageTools

image_tools = ImageTools()

# Görsel Dönüştürme
image_tools.convert_image('input.png', 'output.jpg', 'JPEG')

# Toplu Dönüştürme
image_tools.batch_convert('input_dir', 'output_dir', 'WEBP')

# Yeniden Boyutlandırma
image_tools.resize_image('input.jpg', 'output.jpg', (800, 600))

# Filigran Ekleme
image_tools.add_text_watermark('input.jpg', 'output.jpg', 'WATERMARK')

# Optimize Etme
image_tools.optimize_image('input.jpg', 'output.jpg', quality=85)
```

### Dosya Dönüştürücüler
```python
from tools.convert_tools import ConvertTools

convert_tools = ConvertTools()

# Excel → JSON
convert_tools.excel_to_json('data.xlsx', 'data.json')

# JSON → Excel
convert_tools.json_to_excel('data.json', 'data.xlsx')

# CSV → Excel
convert_tools.csv_to_excel('data.csv', 'data.xlsx')

# TXT → PDF
convert_tools.txt_to_pdf('document.txt', 'document.pdf')

# Word → PDF
convert_tools.word_to_pdf('document.docx', 'document.pdf')
```

### Sistem Araçları
```python
from tools.system_tools import SystemTools

system_tools = SystemTools()

# Hash Hesaplama
md5_hash = system_tools.generate_md5('file.txt')
sha256_hash = system_tools.generate_sha256('file.txt')

# Dosya Şifreleme
system_tools.encrypt_file('file.txt', 'password123', 'file.encrypted')

# Dosya Çözme
system_tools.decrypt_file('file.encrypted', 'password123', 'file_decrypted.txt')

# ZIP Oluşturma
system_tools.create_zip(['file1.txt', 'file2.txt'], 'archive.zip', password='secret')

# ZIP Açma
system_tools.extract_zip('archive.zip', 'output_dir', password='secret')
```

### İnternet Araçları
```python
from tools.net_tools import NetTools

net_tools = NetTools()

# YouTube Thumbnail
net_tools.download_youtube_thumbnail('https://youtube.com/watch?v=VIDEO_ID', 'thumbnail.jpg')

# URL Kısaltma
short_url = net_tools.shorten_url_tinyurl('https://very-long-url.com')

# Hız Testi
speed_results = net_tools.test_internet_speed()
print(f"Download: {speed_results['download_mbps']} Mbps")
print(f"Upload: {speed_results['upload_mbps']} Mbps")
print(f"Ping: {speed_results['ping_ms']} ms")

# IP Adresi
ip_address = net_tools.get_public_ip()
```

---

## 🔐 Lisans Sistemi

### Free vs Pro Karşılaştırması

| Özellik | Free | Pro |
|---------|------|-----|
| PDF Birleştirme | 5 dosya | Sınırsız |
| Toplu İşlemler | 10 dosya | Sınırsız |
| Görsel İşleme | 20 dosya | Sınırsız |
| Filigran Ekleme | ❌ | ✅ |
| Sıkıştırma | ❌ | ✅ |
| Öncelikli Destek | ❌ | ✅ |
| Güncelleme Erken Erişim | ❌ | ✅ |

### Lisans Doğrulama
```python
from components.license_manager import LicenseManager, ProFeatures

lm = LicenseManager()
pro = ProFeatures(lm)

# Lisans yükleme
lm.load_license_file('license.json')

# Pro özellik kontrolü
if lm.is_pro_license_active('user@example.com'):
    print("Pro özellikler aktif!")
else:
    print("Free versiyon kullanılıyor")

# Limit kontrolü
result, message = pro.check_pdf_limit(10, 'user@example.com')
if not result:
    print(f"Limit aşıldı: {message}")
```

---

## 🚀 Deploy

### Railway Backend Deploy
Detaylı bilgi için: [DEPLOY.md](DEPLOY.md)

```bash
# Railway'e deploy için
git push origin main
# Railway dashboard'dan GitHub reposunu bağlayın
```

### Windows EXE Build
```bash
# PyInstaller ile build
python build_exe.py

# Veya manuel
pyinstaller --onefile --noconsole app.py
```

---

## 🎨 Arayüz Özellikleri

### Modern Tasarım
- ✅ Responsive layout
- ✅ Modern gri/siyah/beyaz renk şeması
- ✅ Büyük ve temiz butonlar
- ✅ Progress bar'lar
- ✅ Sekmeli arayüz

### Kullanıcı Dostu
- ✅ Sol dikey menü
- ✅ Üst başlık barı
- ✅ Sağ panelde araç ayarları
- ✅ Durum çubuğu
- ✅ Sürükle & bırak desteği

---

## 📁 Proje Yapısı

```
python_toolbox/
├── app.py                 # Ana uygulama
├── requirements.txt       # Python paketleri
├── Procfile              # Railway deploy
├── build.spec            # PyInstaller spec
├── build_exe.py          # EXE build script
├── README.md             # Bu dosya
├── DEPLOY.md             # Deploy talimatları
├── ui/
│   └── main_window.py    # Ana pencere
├── components/
│   └── license_manager.py # Lisans yönetimi
├── tools/
│   ├── pdf_tools.py      # PDF araçları
│   ├── qr_tools.py       # QR & barkod araçları
│   ├── image_tools.py    # Görsel araçları
│   ├── convert_tools.py  # Dosya dönüştürücü
│   ├── system_tools.py   # Sistem araçları
│   └── net_tools.py      # İnternet araçları
├── api/
│   └── main.py           # FastAPI backend
└── assets/
    └── icons/            # İkonlar
```

---

## 🛡️ Güvenlik

- AES-256 şifreleme
- Güvenli hash algoritmaları (SHA-256)
- API anahtarları korunur
- Lisans doğrulaması
- Güvenli password generator

---

## 📞 Destek

Herhangi bir sorunuz veya sorununuz varsa:

1. **GitHub Issues**: [New Issue](https://github.com/yourusername/python_toolbox/issues/new)
2. **Detaylı Açıklama**: Hata mesajını ve adımları ekleyin
3. **Sistem Bilgisi**: Python versiyonu ve işletim sistemi

### Sık Karşılaşılan Sorunlar

#### Q: PyInstaller build hatası alıyorum
A: Tüm gerekli modüllerin yüklü olduğundan emin olun:
```bash
pip install -r requirements.txt
```

#### Q: QR kod okumuyor
A: Görsel net ve kontrastlı olduğundan emin olun

#### Q: PDF işlemi çok uzun sürüyor
A: Büyük PDF dosyaları için Pro versiyon kullanın

---

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

---

## ⭐ Yıldız Geçmişi

- ⭐ 2024-01-01: İlk sürüm yayınlandı
- ⭐ 2024-01-15: PDF araçları eklendi
- ⭐ 2024-02-01: QR & Barkod araçları eklendi
- ⭐ 2024-02-15: Görsel araçları eklendi
- ⭐ 2024-03-01: Lisans sistemi eklendi
- ⭐ 2024-03-15: EXE build desteği eklendi

---

## 🙏 Teşekkürler

- [PySide6](https://pypi.org/project/PySide6/) - GUI Framework
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) - PDF işleme
- [qrcode](https://pypi.org/project/qrcode/) - QR kod üretimi
- [Pillow](https://pypi.org/project/Pillow/) - Görsel işleme
- [pandas](https://pypi.org/project/pandas/) - Veri analizi
- [cryptography](https://pypi.org/project/cryptography/) - Şifreleme
- [requests](https://pypi.org/project/requests/) - HTTP istekleri

---

**Made with ❤️ by Python Toolbox Team**

[⭐ Bu projeye yıldız verin](https://github.com/yourusername/python_toolbox) | [🚀 GitHub'da görün](https://github.com/yourusername/python_toolbox)