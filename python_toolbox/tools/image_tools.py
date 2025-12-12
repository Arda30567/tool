from PIL import Image, ImageDraw, ImageFont
import os
import piexif
from concurrent.futures import ThreadPoolExecutor

class ImageTools:
    def __init__(self):
        self.supported_formats = ['PNG', 'JPG', 'JPEG', 'WEBP', 'BMP', 'TIFF']

    def convert_image(self, input_path, output_path, output_format):
        with Image.open(input_path) as img:
            if output_format.upper() == 'JPG' and img.mode in ('RGBA', 'LA'):
                img = img.convert('RGB')
            img.save(output_path, format=output_format.upper())
        return output_path

    def batch_convert(self, input_dir, output_dir, output_format):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(tuple(['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'])):
                input_path = os.path.join(input_dir, filename)
                output_filename = os.path.splitext(filename)[0] + f'.{output_format.lower()}'
                output_path = os.path.join(output_dir, output_filename)
                self.convert_image(input_path, output_path, output_format)
                results.append(output_path)
        
        return results

    def resize_image(self, input_path, output_path, size, maintain_aspect=True):
        with Image.open(input_path) as img:
            if maintain_aspect:
                img.thumbnail(size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(output_path)
        return output_path

    def batch_resize(self, input_dir, output_dir, size, maintain_aspect=True):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(tuple(['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'])):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                self.resize_image(input_path, output_path, size, maintain_aspect)
                results.append(output_path)
        
        return results

    def add_text_watermark(self, input_path, output_path, text, position=(50, 50), opacity=128, font_size=36):
        with Image.open(input_path) as img:
            watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = position[0]
            y = position[1]
            
            draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
            
            watermarked = Image.alpha_composite(img.convert('RGBA'), watermark)
            watermarked.save(output_path)
        return output_path

    def add_image_watermark(self, input_path, output_path, watermark_path, position=(50, 50), opacity=0.5):
        with Image.open(input_path) as img:
            with Image.open(watermark_path) as watermark:
                watermark = watermark.convert('RGBA')
                watermark = watermark.resize((int(watermark.width * 0.3), int(watermark.height * 0.3)))
                
                alpha = watermark.split()[-1]
                alpha = alpha.point(lambda p: int(p * opacity))
                watermark.putalpha(alpha)
                
                img.paste(watermark, position, watermark)
                img.save(output_path)
        return output_path

    def batch_add_watermark(self, input_dir, output_dir, watermark_type, watermark_data, position=(50, 50), opacity=128):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(tuple(['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'])):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                
                if watermark_type == "text":
                    self.add_text_watermark(input_path, output_path, watermark_data, position, opacity)
                elif watermark_type == "image":
                    self.add_image_watermark(input_path, output_path, watermark_data, position, opacity/255.0)
                
                results.append(output_path)
        
        return results

    def get_image_info(self, image_path):
        with Image.open(image_path) as img:
            info = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height
            }
            
            if hasattr(img, 'info') and 'dpi' in img.info:
                info["dpi"] = img.info['dpi']
            
            try:
                exif_dict = piexif.load(img.info.get('exif', b''))
                info["exif"] = exif_dict
            except:
                info["exif"] = None
            
            return info

    def optimize_image(self, input_path, output_path, quality=85):
        with Image.open(input_path) as img:
            if img.format == 'JPEG':
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
            elif img.format == 'PNG':
                img.save(output_path, 'PNG', optimize=True)
            else:
                img.save(output_path, optimize=True)
        return output_path

    def batch_optimize(self, input_dir, output_dir, quality=85):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(tuple(['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'])):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                self.optimize_image(input_path, output_path, quality)
                results.append(output_path)
        
        return results