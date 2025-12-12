import requests
import speedtest
import re
from urllib.parse import urlparse
import json

class NetTools:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def download_youtube_thumbnail(self, youtube_url, output_path=None):
        video_id = self._extract_youtube_id(youtube_url)
        if not video_id:
            raise ValueError("Geçerli bir YouTube URL'si değil")
        
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        try:
            response = self.session.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            
            if output_path is None:
                output_path = f"youtube_thumbnail_{video_id}.jpg"
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
        except requests.RequestException as e:
            raise Exception(f"Thumbnail indirme hatası: {str(e)}")

    def _extract_youtube_id(self, url):
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:v\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None

    def shorten_url_bitly(self, long_url, access_token):
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'long_url': long_url
        }
        
        try:
            response = requests.post(
                'https://api-ssl.bitly.com/v4/shorten',
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('link', result.get('id'))
        except requests.RequestException as e:
            raise Exception(f"URL kısaltma hatası: {str(e)}")

    def shorten_url_tinyurl(self, long_url):
        try:
            response = self.session.post(
                'https://tinyurl.com/api-create.php',
                data={'url': long_url},
                timeout=10
            )
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            raise Exception(f"URL kısaltma hatası: {str(e)}")

    def test_internet_speed(self):
        st = speedtest.Speedtest()
        
        st.get_best_server()
        
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000  # Mbps
        ping = st.results.ping
        
        results = {
            'download_mbps': round(download_speed, 2),
            'upload_mbps': round(upload_speed, 2),
            'ping_ms': round(ping, 2),
            'server': st.results.server['sponsor'],
            'server_location': f"{st.results.server['name']}, {st.results.server['country']}"
        }
        
        return results

    def check_website_status(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            return {
                'url': url,
                'status_code': response.status_code,
                'is_up': response.status_code < 400,
                'response_time': response.elapsed.total_seconds()
            }
        except requests.RequestException as e:
            return {
                'url': url,
                'status_code': None,
                'is_up': False,
                'error': str(e)
            }

    def get_website_info(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            
            info = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'encoding': response.encoding,
                'content_length': len(response.content),
                'server': response.headers.get('Server', 'Unknown'),
                'content_type': response.headers.get('Content-Type', 'Unknown')
            }
            
            return info
        except requests.RequestException as e:
            return {
                'url': url,
                'error': str(e)
            }

    def download_file(self, url, output_path=None):
        try:
            response = self.session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            if output_path is None:
                filename = url.split('/')[-1]
                output_path = filename
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {
                'success': True,
                'output_path': output_path,
                'size': os.path.getsize(output_path) if os.path.exists(output_path) else 0
            }
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_public_ip(self):
        try:
            response = self.session.get('https://api.ipify.org', timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException:
            try:
                response = self.session.get('https://httpbin.org/ip', timeout=5)
                response.raise_for_status()
                return response.json()['origin']
            except requests.RequestException as e:
                raise Exception(f"IP adresi alınamadı: {str(e)}")

import os