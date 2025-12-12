import json
import os
import hashlib
import uuid
from datetime import datetime, timedelta
import requests
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class LicenseManager:
    def __init__(self, api_base_url=None):
        self.api_base_url = api_base_url or "https://your-api-domain.com"
        self.licenses_file = "licenses.json"
        self.local_licenses = self._load_local_licenses()
        
    def _load_local_licenses(self):
        if os.path.exists(self.licenses_file):
            try:
                with open(self.licenses_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_local_licenses(self):
        with open(self.licenses_file, 'w') as f:
            json.dump(self.local_licenses, f, indent=2)
    
    def _generate_license_key(self, email, license_type="pro"):
        timestamp = datetime.now().isoformat()
        data = f"{email}:{license_type}:{timestamp}:{uuid.uuid4().hex}"
        return hashlib.sha256(data.encode()).hexdigest()[:32].upper()
    
    def generate_offline_license(self, email, name, license_type="pro"):
        license_key = self._generate_license_key(email, license_type)
        
        license_data = {
            "license_key": license_key,
            "email": email,
            "name": name,
            "license_type": license_type,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
            "is_active": True,
            "usage_count": 0,
            "offline": True
        }
        
        self.local_licenses[license_key] = license_data
        self._save_local_licenses()
        
        return license_data
    
    def verify_offline_license(self, license_key, email):
        if license_key not in self.local_licenses:
            return False, "Lisans bulunamadı"
        
        license_data = self.local_licenses[license_key]
        
        if not license_data.get("is_active", False):
            return False, "Lisans aktif değil"
        
        if license_data["email"] != email:
            return False, "E-posta adresi uyuşmuyor"
        
        expires_at = datetime.fromisoformat(license_data["expires_at"])
        if datetime.now() > expires_at:
            return False, "Lisans süresi dolmuş"
        
        license_data["usage_count"] = license_data.get("usage_count", 0) + 1
        license_data["last_used"] = datetime.now().isoformat()
        self.local_licenses[license_key] = license_data
        self._save_local_licenses()
        
        return True, "Lisans doğrulandı"
    
    def generate_online_license(self, email, name, license_type="pro"):
        try:
            response = requests.post(
                f"{self.api_base_url}/generate-license",
                json={
                    "email": email,
                    "name": name,
                    "license_type": license_type
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                license_data = data.get("license_data")
                self.local_licenses[license_data["license_key"]] = license_data
                self._save_local_licenses()
                return license_data
            else:
                return None
        except Exception as e:
            print(f"Online lisans oluşturma hatası: {e}")
            return None
    
    def verify_online_license(self, license_key, email):
        try:
            response = requests.post(
                f"{self.api_base_url}/verify-license",
                json={
                    "license_key": license_key,
                    "email": email
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Lisans doğrulandı"
            else:
                return False, "Lisans doğrulanamadı"
        except Exception as e:
            print(f"Online lisans doğrulama hatası: {e}")
            return False, "Bağlantı hatası"
    
    def load_license_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                license_data = json.load(f)
            
            if self.validate_license_data(license_data):
                self.local_licenses[license_data["license_key"]] = license_data
                self._save_local_licenses()
                return True, "Lisans dosyası yüklendi"
            else:
                return False, "Geçersiz lisans dosyası"
        except Exception as e:
            return False, f"Dosya yükleme hatası: {e}"
    
    def validate_license_data(self, license_data):
        required_fields = ["license_key", "email", "license_type", "created_at", "expires_at"]
        return all(field in license_data for field in required_fields)
    
    def is_pro_license_active(self, email=None):
        if email:
            for license_key, license_data in self.local_licenses.items():
                if license_data["email"] == email and license_data.get("is_active", False):
                    expires_at = datetime.fromisoformat(license_data["expires_at"])
                    if datetime.now() <= expires_at:
                        return True
            return False
        else:
            for license_data in self.local_licenses.values():
                if license_data.get("is_active", False):
                    expires_at = datetime.fromisoformat(license_data["expires_at"])
                    if datetime.now() <= expires_at:
                        return True
            return False
    
    def get_license_info(self, license_key):
        if license_key in self.local_licenses:
            return self.local_licenses[license_key]
        return None
    
    def get_all_licenses(self):
        return self.local_licenses
    
    def revoke_license(self, license_key):
        if license_key in self.local_licenses:
            self.local_licenses[license_key]["is_active"] = False
            self._save_local_licenses()
            return True
        return False
    
    def export_license(self, license_key, output_path):
        if license_key in self.local_licenses:
            with open(output_path, 'w') as f:
                json.dump(self.local_licenses[license_key], f, indent=2)
            return True
        return False
    
    def check_license_limits(self, email=None):
        if self.is_pro_license_active(email):
            return {
                "pdf_limit": float('inf'),
                "batch_limit": float('inf'),
                "image_limit": float('inf'),
                "pro_features": True
            }
        else:
            return {
                "pdf_limit": 5,
                "batch_limit": 10,
                "image_limit": 20,
                "pro_features": False
            }

class ProFeatures:
    def __init__(self, license_manager):
        self.license_manager = license_manager
    
    def check_pdf_limit(self, file_count, email=None):
        limits = self.license_manager.check_license_limits(email)
        if not limits["pro_features"] and file_count > limits["pdf_limit"]:
            return False, f"Free versiyonda en fazla {limits['pdf_limit']} PDF işleyebilirsiniz"
        return True, "OK"
    
    def check_batch_limit(self, item_count, email=None):
        limits = self.license_manager.check_license_limits(email)
        if not limits["pro_features"] and item_count > limits["batch_limit"]:
            return False, f"Free versiyonda en fazla {limits['batch_limit']} dosya işleyebilirsiniz"
        return True, "OK"
    
    def check_image_limit(self, image_count, email=None):
        limits = self.license_manager.check_license_limits(email)
        if not limits["pro_features"] and image_count > limits["image_limit"]:
            return False, f"Free versiyonda en fazla {limits['image_limit']} görsel işleyebilirsiniz"
        return True, "OK"
    
    def get_feature_status(self, email=None):
        is_pro = self.license_manager.is_pro_license_active(email)
        return {
            "is_pro": is_pro,
            "can_use_batch": is_pro,
            "can_use_unlimited_pdf": is_pro,
            "can_use_unlimited_images": is_pro,
            "has_watermark_feature": is_pro,
            "has_compression_feature": is_pro
        }