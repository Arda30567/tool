import os
import fitz
from PIL import Image
import io
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import pikepdf

class PDFTools:
    def __init__(self):
        pass

    def merge_pdfs(self, pdf_files, output_path):
        merger = PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        merger.write(output_path)
        merger.close()
        return output_path

    def split_pdf(self, pdf_file, output_dir, split_type="pages", pages_per_split=1):
        reader = PdfReader(pdf_file)
        total_pages = len(reader.pages)
        output_files = []
        
        if split_type == "pages":
            for i in range(0, total_pages, pages_per_split):
                writer = PdfWriter()
                for j in range(i, min(i + pages_per_split, total_pages)):
                    writer.add_page(reader.pages[j])
                output_file = os.path.join(output_dir, f"split_{i+1}-{min(i+pages_per_split, total_pages)}.pdf")
                with open(output_file, "wb") as f:
                    writer.write(f)
                output_files.append(output_file)
        
        return output_files

    def pdf_to_jpg(self, pdf_file, output_dir, dpi=300):
        doc = fitz.open(pdf_file)
        image_files = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            output_file = os.path.join(output_dir, f"page_{page_num+1}.jpg")
            img.save(output_file, "JPEG", quality=95)
            image_files.append(output_file)
        
        doc.close()
        return image_files

    def jpg_to_pdf(self, image_files, output_path):
        doc = fitz.open()
        for image_file in image_files:
            img = fitz.open(image_file)
            pdf_bytes = img.convert_to_pdf()
            pdf_doc = fitz.open("pdf", pdf_bytes)
            doc.insert_pdf(pdf_doc)
            img.close()
            pdf_doc.close()
        doc.save(output_path)
        doc.close()
        return output_path

    def compress_pdf(self, pdf_file, output_path, quality="/ebook"):
        with pikepdf.open(pdf_file) as pdf:
            pdf.save(output_path, compress_streams=True, object_stream_mode=pikepdf.ObjectStreamMode.generate)
        return output_path

    def add_watermark_text(self, pdf_file, output_path, text, position=(100, 100), opacity=0.5):
        doc = fitz.open(pdf_file)
        for page in doc:
            rect = page.rect
            page.insert_text(position, text, fontsize=40, rotate=45, color=(0.8, 0.8, 0.8), opacity=opacity)
        doc.save(output_path)
        doc.close()
        return output_path

    def add_watermark_image(self, pdf_file, output_path, watermark_image, position=(100, 100), opacity=0.5):
        doc = fitz.open(pdf_file)
        for page in doc:
            rect = page.rect
            page.insert_image(rect, filename=watermark_image, overlay=True, opacity=opacity)
        doc.save(output_path)
        doc.close()
        return output_path