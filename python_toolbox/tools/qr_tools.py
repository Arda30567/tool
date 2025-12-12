import qrcode
import barcode
from barcode.writer import ImageWriter
from pyzbar import pyzbar
from PIL import Image
import csv
import os

class QRTools:
    def __init__(self):
        pass

    def generate_qr(self, data, output_path, version=1, box_size=10, border=5, fill_color="black", back_color="white"):
        qr = qrcode.QRCode(version=version, box_size=box_size, border=border)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(output_path)
        return output_path

    def generate_wifi_qr(self, ssid, password, security_type="WPA", output_path="wifi_qr.png"):
        wifi_string = f"WIFI:T:{security_type};S:{ssid};P:{password};;"
        return self.generate_qr(wifi_string, output_path)

    def generate_phone_qr(self, phone_number, output_path="phone_qr.png"):
        phone_string = f"tel:{phone_number}"
        return self.generate_qr(phone_string, output_path)

    def read_qr(self, image_path):
        image = Image.open(image_path)
        decoded_objects = pyzbar.decode(image)
        results = []
        for obj in decoded_objects:
            results.append({
                "type": obj.type,
                "data": obj.data.decode("utf-8")
            })
        return results

    def batch_generate_qr(self, csv_file, output_dir):
        results = []
        with open(csv_file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if 'data' in row and 'filename' in row:
                    output_path = os.path.join(output_dir, f"{row['filename']}.png")
                    self.generate_qr(row['data'], output_path)
                    results.append(output_path)
        return results

    def generate_barcode(self, data, barcode_type="code128", output_path="barcode.png"):
        if barcode_type.lower() == "ean13":
            barcode_class = barcode.EAN13
        elif barcode_type.lower() == "code128":
            barcode_class = barcode.Code128
        else:
            barcode_class = barcode.Code128
        
        code = barcode_class(data, writer=ImageWriter())
        code.save(output_path.replace('.png', ''))
        return output_path

    def generate_bulk_barcodes(self, data_list, barcode_type="code128", output_dir="barcodes"):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        for i, data in enumerate(data_list):
            output_path = os.path.join(output_dir, f"barcode_{i+1}.png")
            self.generate_barcode(data, barcode_type, output_path)
            results.append(output_path)
        return results