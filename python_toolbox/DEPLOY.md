# Python Toolbox - Deploy Talimatları

## İçindekiler
1. [Railway'e Backend Deploy Etme](#railway-backend-deploy)
2. [Windows için EXE Oluşturma](#windows-exe-build)
3. [Lisans Sistemi Kullanımı](#license-system)
4. [API Kullanımı](#api-usage)

---

## Railway Backend Deploy

### Adım 1: Railway Hesabı Oluşturma
1. [Railway](https://railway.app) adresine gidin
2. GitHub hesabınızla kaydolun
3. Yeni bir proje oluşturun

### Adım 2: Proje Dosyalarını Hazırlama
```bash
# Proje klasörünüze gidin
cd python_toolbox

# Gerekli dosyaların olduğundan emin olun:
# - api/main.py (FastAPI uygulaması)
# - requirements.txt
# - Procfile
```

### Adım 3: Railway'e Deploy Etme

#### Yöntem 1: GitHub ile (Önerilen)
1. Projenizi GitHub'a yükleyin:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/python_toolbox.git
git push -u origin main
```

2. Railway dashboard'dan "New Project" -> "Deploy from GitHub"
3. Python Toolbox reposunu seçin
4. Deploy işlemi otomatik başlayacak

#### Yöntem 2: CLI ile
```bash
# Railway CLI'yi yükleyin
npm i -g @railway/cli

# Login olun
railway login

# Proje oluşturun
railway init

# Deploy edin
railway up
```

### Adım 4: Ortam Değişkenleri Ayarlama
Railway dashboard'dan:
1. Project Settings -> Variables
2. Aşağıdaki değişkenleri ekleyin:
   - `PORT`: 8000 (otomatik ayarlanır)
   - Python versiyonu için `NIXPACKS_PYTHON_VERSION`: "3.11"

### Adım 5: API Test Etme
```bash
# Health check
curl https://your-app-domain.up.railway.app/health

# Örnek cevap:
# {"status":"healthy","timestamp":"2024-01-01T00:00:00","version":"1.0.0"}
```

---

## Windows EXE Build

### Gerekli Kurulumlar
```bash
# Python 3.8+ yüklü olduğundan emin olun
python --version

# Gerekli paketleri yükleyin
pip install -r requirements.txt
pip install pyinstaller
```

### Build İşlemi

#### Yöntem 1: build_exe.py Scripti (Önerilen)
```bash
# Build scriptini çalıştırın
python build_exe.py

# 1. Basit build (önerilen)
# 2. Spec dosyası ile build
```

#### Yöntem 2: Manuel PyInstaller Komutu
```bash
pyinstaller --onefile --noconsole --name=PythonToolbox --add-data="tools;tools" --add-data="ui;ui" --add-data="components;components" --add-data="api;api" --add-data="assets;assets" --hidden-import="PySide6.QtCore" --hidden-import="PySide6.QtGui" --hidden-import="PySide6.QtWidgets" --hidden-import="fitz" --hidden-import="PyPDF2" --hidden-import="PIL.Image" --clean --optimize=2 app.py
```

### Build Sonrası
1. `dist/PythonToolbox.exe` dosyası oluşacak
2. EXE dosyası masaüstüne kopyalanacak
3. İlk çalıştırmada Windows Defender uyarısı gelebilir
4. "Daha fazla bilgi" -> "Çalıştır" diyerek devam edin

### Sorun Giderme

#### "ModuleNotFoundError" Hatası
```bash
# Eksik modülleri belirleyin ve spec dosyasına ekleyin
# build.spec dosyasındaki hiddenimports listesine ekleyin
```

#### EXE Çok Büyük
```bash
# Kullanılmayan modülleri exclude edin
# build.spec dosyasındaki excludes listesine ekleyin
# Örnek: '--exclude-module matplotlib'
```

---

## License System

### Offline Lisans Oluşturma
```python
from components.license_manager import LicenseManager

lm = LicenseManager()
license_data = lm.generate_offline_license(
    email="user@example.com",
    name="John Doe",
    license_type="pro"
)

# license_data['license_key'] ile lisans anahtarını alın
```

### Lisans Doğrulama
```python
is_valid, message = lm.verify_offline_license(
    license_key="YOUR_LICENSE_KEY",
    email="user@example.com"
)

if is_valid:
    print("Pro özellikler aktif!")
else:
    print(f"Hata: {message}")
```

### Pro Özellik Limitleri
```python
pro_features = ProFeatures(lm)
limits = pro_features.check_pdf_limit(10, "user@example.com")

if not limits[0]:
    print(f"Limit aşıldı: {limits[1]}")
```

### Free vs Pro Karşılaştırması
| Özellik | Free | Pro |
|---------|------|-----|
| PDF Birleştirme | 5 dosya | Sınırsız |
| Toplu İşlemler | 10 dosya | Sınırsız |
| Görsel İşleme | 20 dosya | Sınırsız |
| Filigran Ekleme | ❌ | ✅ |
| Sıkıştırma | ❌ | ✅ |

---

## API Usage

### Health Check
```bash
curl -X GET "https://your-api-domain.com/health"
```

### Generate License
```bash
curl -X POST "https://your-api-domain.com/generate-license" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "name": "John Doe",
    "license_type": "pro"
  }'
```

### Verify License
```bash
curl -X POST "https://your-api-domain.com/verify-license" \
  -H "Content-Type: application/json" \
  -d '{
    "license_key": "YOUR_LICENSE_KEY",
    "email": "user@example.com"
  }'
```

### Generate API Key
```bash
curl -X POST "https://your-api-domain.com/generate-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "qr_generator"
  }'
```

### Get Stats
```bash
curl -X GET "https://your-api-domain.com/stats"
```

---

## Güvenlik Notları

1. **API Key'leri Koruyun**: API key'lerinizi .env dosyalarında saklayın
2. **Lisans Doğrulaması**: Her zaman lisans geçerliliğini kontrol edin
3. **Rate Limiting**: API çağrıları için rate limiting uygulayın
4. **HTTPS Kullanın**: Production'da mutlaka HTTPS kullanın

## Destek

Herhangi bir sorunuz veya sorununuz varsa:
1. GitHub Issues açın
2. Detaylı hata mesajı ekleyin
3. Python versiyonunuzu ve işletim sisteminizi belirtin

---

**Başarılar dileriz!** 🚀