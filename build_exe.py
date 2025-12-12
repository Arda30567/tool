#!/usr/bin/env python3
"""
Python Toolbox - EXE Build Script
Bu script PyInstaller kullanarak Windows için executable oluşturur
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """Windows için EXE oluştur"""
    
    print("Python Toolbox EXE Builder")
    print("=" * 50)
    
    # Temizlik
    print("\n1. Önceki build dosyaları temizleniyor...")
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   ✓ {folder} klasörü silindi")
    
    # PyInstaller komutu
    print("\n2. PyInstaller ile build işlemi başlatılıyor...")
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        '--name=PythonToolbox',
        '--add-data=tools;tools',
        '--add-data=ui;ui', 
        '--add-data=components;components',
        '--add-data=api;api',
        '--add-data=assets;assets',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=PySide6.QtPrintSupport',
        '--hidden-import=fitz',
        '--hidden-import=PyPDF2',
        '--hidden-import=pikepdf',
        '--hidden-import=reportlab',
        '--hidden-import=qrcode',
        '--hidden-import=pyzbar',
        '--hidden-import=barcode',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageDraw',
        '--hidden-import=PIL.ImageFont',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=docx',
        '--hidden-import=docx2pdf',
        '--hidden-import=cryptography',
        '--hidden-import=requests',
        '--hidden-import=speedtest',
        '--hidden-import=piexif',
        '--hidden-import=asyncio',
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=pydantic',
        '--clean',
        '--optimize=2',
        'app.py'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✓ Build işlemi başarıyla tamamlandı!")
            
            # EXE dosyasının yeri
            exe_path = os.path.join('dist', 'PythonToolbox.exe')
            if os.path.exists(exe_path):
                print(f"\n3. EXE dosyası oluşturuldu: {exe_path}")
                print(f"   Dosya boyutu: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
                
                # Taşı
                desktop_exe = os.path.join(os.path.expanduser('~'), 'Desktop', 'PythonToolbox.exe')
                shutil.copy2(exe_path, desktop_exe)
                print(f"   ✓ EXE dosyası Masaüstüne kopyalandı: {desktop_exe}")
                
        else:
            print("   ✗ Build işlemi başarısız!")
            print("\nHata detayları:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"   ✗ Build hatası: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("Build işlemi tamamlandı!")
    print("\nKullanım:")
    print("1. Masaüstündeki PythonToolbox.exe dosyasını çalıştırın")
    print("2. İlk çalıştırmada Windows Defender uyarısı gelebilir")
    print("3. 'Daha fazla bilgi' -> 'Çalıştır' diyerek devam edin")
    
    return True

def build_with_spec():
    """Spec dosyası kullanarak build"""
    print("Spec dosyası kullanarak build işlemi...")
    
    try:
        result = subprocess.run(['pyinstaller', 'build.spec'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✓ Spec ile build başarılı!")
            return True
        else:
            print("   ✗ Spec ile build başarısız!")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"   ✗ Spec build hatası: {e}")
        return False

if __name__ == "__main__":
    print("Build seçenekleri:")
    print("1. Basit build (önerilen)")
    print("2. Spec dosyası ile build")
    
    choice = input("\nSeçiminiz (1/2): ").strip()
    
    if choice == "2":
        build_with_spec()
    else:
        build_exe()