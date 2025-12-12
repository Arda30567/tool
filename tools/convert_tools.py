import pandas as pd
import json
import csv
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

class ConvertTools:
    def __init__(self):
        pass

    def excel_to_json(self, excel_file, output_path=None):
        df = pd.read_excel(excel_file)
        json_data = df.to_json(orient="records", indent=2, force_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            return output_path
        return json_data

    def json_to_excel(self, json_file, output_path):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False, engine='openpyxl')
        return output_path

    def csv_to_excel(self, csv_file, output_path):
        df = pd.read_csv(csv_file)
        df.to_excel(output_path, index=False, engine='openpyxl')
        return output_path

    def txt_to_pdf(self, txt_file, output_path):
        with open(txt_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        margin = 50
        y_position = height - margin
        
        lines = text.split('\n')
        
        for line in lines:
            if y_position < margin:
                c.showPage()
                y_position = height - margin
            
            wrapped_lines = simpleSplit(line, 'Helvetica', 12, width - 2 * margin)
            
            for wrapped_line in wrapped_lines:
                c.drawString(margin, y_position, wrapped_line)
                y_position -= 15
        
        c.save()
        return output_path

    def word_to_pdf(self, docx_file, output_path):
        from docx2pdf import convert
        convert(docx_file, output_path)
        return output_path

    def batch_convert(self, input_dir, output_dir, conversion_type):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)
            
            if conversion_type == "excel_to_json" and filename.endswith(('.xlsx', '.xls')):
                output_filename = os.path.splitext(filename)[0] + '.json'
                output_path = os.path.join(output_dir, output_filename)
                self.excel_to_json(input_path, output_path)
                results.append(output_path)
            
            elif conversion_type == "json_to_excel" and filename.endswith('.json'):
                output_filename = os.path.splitext(filename)[0] + '.xlsx'
                output_path = os.path.join(output_dir, output_filename)
                self.json_to_excel(input_path, output_path)
                results.append(output_path)
            
            elif conversion_type == "csv_to_excel" and filename.endswith('.csv'):
                output_filename = os.path.splitext(filename)[0] + '.xlsx'
                output_path = os.path.join(output_dir, output_filename)
                self.csv_to_excel(input_path, output_path)
                results.append(output_path)
            
            elif conversion_type == "txt_to_pdf" and filename.endswith('.txt'):
                output_filename = os.path.splitext(filename)[0] + '.pdf'
                output_path = os.path.join(output_dir, output_filename)
                self.txt_to_pdf(input_path, output_path)
                results.append(output_path)
            
            elif conversion_type == "word_to_pdf" and filename.endswith('.docx'):
                output_filename = os.path.splitext(filename)[0] + '.pdf'
                output_path = os.path.join(output_dir, output_filename)
                self.word_to_pdf(input_path, output_path)
                results.append(output_path)
        
        return results

    def convert_format(self, input_file, output_path, input_format=None, output_format=None):
        if not input_format:
            input_format = os.path.splitext(input_file)[1].lower()
        if not output_format:
            output_format = os.path.splitext(output_path)[1].lower()
        
        conversion_map = {
            ('.xlsx', '.json'): self.excel_to_json,
            ('.xls', '.json'): self.excel_to_json,
            ('.json', '.xlsx'): self.json_to_excel,
            ('.csv', '.xlsx'): self.csv_to_excel,
            ('.txt', '.pdf'): self.txt_to_pdf,
            ('.docx', '.pdf'): self.word_to_pdf
        }
        
        for (inp_fmt, out_fmt), func in conversion_map.items():
            if input_format == inp_fmt and output_format == out_fmt:
                return func(input_file, output_path)
        
        raise ValueError(f"Conversion from {input_format} to {output_format} not supported")