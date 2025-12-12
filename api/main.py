from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
import os
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Optional

app = FastAPI(title="Python Toolbox API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LICENSES_FILE = "licenses.json"
API_KEYS_FILE = "api_keys.json"

class LicenseRequest(BaseModel):
    email: str
    name: str
    license_type: str = "pro"

class LicenseVerification(BaseModel):
    license_key: str
    email: str

class APIKeyRequest(BaseModel):
    service: str

class APIKeyVerification(BaseModel):
    api_key: str

def load_licenses():
    if os.path.exists(LICENSES_FILE):
        with open(LICENSES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_licenses(licenses):
    with open(LICENSES_FILE, 'w') as f:
        json.dump(licenses, f, indent=2)

def load_api_keys():
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_api_keys(api_keys):
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f, indent=2)

def generate_license_key(email, license_type="pro"):
    timestamp = datetime.now().isoformat()
    data = f"{email}:{license_type}:{timestamp}:{secrets.token_hex(16)}"
    return hashlib.sha256(data.encode()).hexdigest()[:32].upper()

def generate_api_key(service):
    timestamp = datetime.now().isoformat()
    data = f"{service}:{timestamp}:{secrets.token_hex(16)}"
    return hashlib.sha256(data.encode()).hexdigest()[:24]

@app.get("/")
async def root():
    return {"message": "Python Toolbox API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "api": "running"
        }
    }

@app.post("/generate-license")
async def generate_license(request: LicenseRequest):
    licenses = load_licenses()
    
    license_key = generate_license_key(request.email, request.license_type)
    
    license_data = {
        "license_key": license_key,
        "email": request.email,
        "name": request.name,
        "license_type": request.license_type,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=365)).isoformat(),
        "is_active": True,
        "usage_count": 0
    }
    
    licenses[license_key] = license_data
    save_licenses(licenses)
    
    return {
        "success": True,
        "license_key": license_key,
        "message": "Lisans başarıyla oluşturuldu",
        "license_data": license_data
    }

@app.post("/verify-license")
async def verify_license(request: LicenseVerification):
    licenses = load_licenses()
    
    if request.license_key not in licenses:
        raise HTTPException(status_code=404, detail="Lisans bulunamadı")
    
    license_data = licenses[request.license_key]
    
    if not license_data.get("is_active", False):
        raise HTTPException(status_code=403, detail="Lisans aktif değil")
    
    if license_data["email"] != request.email:
        raise HTTPException(status_code=403, detail="E-posta adresi uyuşmuyor")
    
    expires_at = datetime.fromisoformat(license_data["expires_at"])
    if datetime.now() > expires_at:
        raise HTTPException(status_code=403, detail="Lisans süresi dolmuş")
    
    license_data["usage_count"] = license_data.get("usage_count", 0) + 1
    licenses[request.license_key] = license_data
    save_licenses(licenses)
    
    return {
        "success": True,
        "message": "Lisans doğrulandı",
        "license_type": license_data["license_type"],
        "expires_at": license_data["expires_at"],
        "usage_count": license_data["usage_count"]
    }

@app.post("/generate-api-key")
async def generate_api_key_endpoint(request: APIKeyRequest):
    api_keys = load_api_keys()
    
    api_key = generate_api_key(request.service)
    
    key_data = {
        "api_key": api_key,
        "service": request.service,
        "created_at": datetime.now().isoformat(),
        "is_active": True,
        "usage_count": 0
    }
    
    api_keys[api_key] = key_data
    save_api_keys(api_keys)
    
    return {
        "success": True,
        "api_key": api_key,
        "message": f"{request.service} için API anahtarı oluşturuldu",
        "key_data": key_data
    }

@app.post("/verify-api-key")
async def verify_api_key_endpoint(request: APIKeyVerification):
    api_keys = load_api_keys()
    
    if request.api_key not in api_keys:
        raise HTTPException(status_code=404, detail="API anahtarı bulunamadı")
    
    key_data = api_keys[request.api_key]
    
    if not key_data.get("is_active", False):
        raise HTTPException(status_code=403, detail="API anahtarı aktif değil")
    
    key_data["usage_count"] = key_data.get("usage_count", 0) + 1
    key_data["last_used"] = datetime.now().isoformat()
    api_keys[request.api_key] = key_data
    save_api_keys(api_keys)
    
    return {
        "success": True,
        "message": "API anahtarı doğrulandı",
        "service": key_data["service"],
        "usage_count": key_data["usage_count"],
        "last_used": key_data.get("last_used")
    }

@app.get("/license-info/{license_key}")
async def get_license_info(license_key: str):
    licenses = load_licenses()
    
    if license_key not in licenses:
        raise HTTPException(status_code=404, detail="Lisans bulunamadı")
    
    return licenses[license_key]

@app.get("/api-usage/{api_key}")
async def get_api_usage(api_key: str):
    api_keys = load_api_keys()
    
    if api_key not in api_keys:
        raise HTTPException(status_code=404, detail="API anahtarı bulunamadı")
    
    return {
        "api_key": api_key,
        "service": api_keys[api_key]["service"],
        "usage_count": api_keys[api_key]["usage_count"],
        "created_at": api_keys[api_key]["created_at"],
        "last_used": api_keys[api_key].get("last_used", "Never")
    }

@app.post("/revoke-license")
async def revoke_license(license_key: str):
    licenses = load_licenses()
    
    if license_key not in licenses:
        raise HTTPException(status_code=404, detail="Lisans bulunamadı")
    
    licenses[license_key]["is_active"] = False
    save_licenses(licenses)
    
    return {
        "success": True,
        "message": "Lisans iptal edildi"
    }

@app.post("/revoke-api-key")
async def revoke_api_key(api_key: str):
    api_keys = load_api_keys()
    
    if api_key not in api_keys:
        raise HTTPException(status_code=404, detail="API anahtarı bulunamadı")
    
    api_keys[api_key]["is_active"] = False
    save_api_keys(api_keys)
    
    return {
        "success": True,
        "message": "API anahtarı iptal edildi"
    }

@app.get("/stats")
async def get_stats():
    licenses = load_licenses()
    api_keys = load_api_keys()
    
    active_licenses = sum(1 for lic in licenses.values() if lic.get("is_active", False))
    total_licenses = len(licenses)
    
    active_api_keys = sum(1 for key in api_keys.values() if key.get("is_active", False))
    total_api_keys = len(api_keys)
    
    total_usage = sum(lic.get("usage_count", 0) for lic in licenses.values())
    total_api_usage = sum(key.get("usage_count", 0) for key in api_keys.values())
    
    return {
        "licenses": {
            "total": total_licenses,
            "active": active_licenses,
            "inactive": total_licenses - active_licenses
        },
        "api_keys": {
            "total": total_api_keys,
            "active": active_api_keys,
            "inactive": total_api_keys - active_api_keys
        },
        "usage": {
            "total_license_usage": total_usage,
            "total_api_usage": total_api_usage
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)