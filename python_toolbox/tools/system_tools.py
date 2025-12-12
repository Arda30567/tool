import hashlib
import os
import zipfile
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets

class SystemTools:
    def __init__(self):
        pass

    def generate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def generate_sha256(self, file_path):
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def generate_sha512(self, file_path):
        hash_sha512 = hashlib.sha512()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()

    def generate_key_from_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_bytes(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def encrypt_file(self, file_path, password, output_path=None):
        key, salt = self.generate_key_from_password(password)
        f = Fernet(key)
        
        if output_path is None:
            output_path = file_path + '.encrypted'
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = f.encrypt(file_data)
        
        with open(output_path, 'wb') as file:
            file.write(salt + encrypted_data)
        
        return output_path

    def decrypt_file(self, encrypted_file_path, password, output_path=None):
        with open(encrypted_file_path, 'rb') as file:
            salt = file.read(16)
            encrypted_data = file.read()
        
        key, _ = self.generate_key_from_password(password, salt)
        f = Fernet(key)
        
        try:
            decrypted_data = f.decrypt(encrypted_data)
            
            if output_path is None:
                output_path = encrypted_file_path.replace('.encrypted', '')
            
            with open(output_path, 'wb') as file:
                file.write(decrypted_data)
            
            return output_path
        except Exception as e:
            raise ValueError("Şifre çözme başarısız. Yanlış şifre veya dosya bozuk.")

    def create_zip(self, files, output_path, password=None):
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                if os.path.isfile(file):
                    zipf.write(file, os.path.basename(file))
                elif os.path.isdir(file):
                    for root, dirs, filenames in os.walk(file):
                        for filename in filenames:
                            filepath = os.path.join(root, filename)
                            arcname = os.path.relpath(filepath, file)
                            zipf.write(filepath, arcname)
        
        if password:
            encrypted_zip = output_path + '.encrypted'
            return self.encrypt_file(output_path, password, encrypted_zip)
        
        return output_path

    def extract_zip(self, zip_path, extract_to, password=None):
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            if password:
                zipf.setpassword(password.encode())
            zipf.extractall(extract_to)
        return extract_to

    def get_file_info(self, file_path):
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        info = {
            "size": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "modified": stat.st_mtime,
            "created": stat.st_ctime,
            "is_file": os.path.isfile(file_path),
            "is_dir": os.path.isdir(file_path),
            "extension": os.path.splitext(file_path)[1],
            "name": os.path.basename(file_path),
            "path": os.path.abspath(file_path)
        }
        
        return info

    def batch_hash_files(self, directory, hash_type="sha256"):
        results = {}
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                if hash_type == "md5":
                    results[filename] = self.generate_md5(file_path)
                elif hash_type == "sha256":
                    results[filename] = self.generate_sha256(file_path)
                elif hash_type == "sha512":
                    results[filename] = self.generate_sha512(file_path)
        
        return results

    def generate_secure_password(self, length=16):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def verify_hash(self, file_path, expected_hash, hash_type="sha256"):
        if hash_type == "md5":
            calculated_hash = self.generate_md5(file_path)
        elif hash_type == "sha256":
            calculated_hash = self.generate_sha256(file_path)
        elif hash_type == "sha512":
            calculated_hash = self.generate_sha512(file_path)
        else:
            raise ValueError("Unsupported hash type")
        
        return calculated_hash == expected_hash