from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
                               QWidget, QStackedWidget, QMenuBar, QMenu, QStatusBar,
                               QLabel, QProgressBar, QFileDialog, QMessageBox,
                               QGroupBox, QTextEdit, QLineEdit, QCheckBox, QSpinBox,
                               QComboBox, QSlider, QFrame, QSplitter, QToolButton,
                               QTabWidget, QGridLayout, QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QPixmap
import os
import sys
from tools.pdf_tools import PDFTools
from tools.qr_tools import QRTools
from tools.image_tools import ImageTools
from tools.convert_tools import ConvertTools
from tools.system_tools import SystemTools
from tools.net_tools import NetTools

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Toolbox - Profesyonel Araç Seti")
        self.setGeometry(100, 100, 1400, 900)
        
        self.pdf_tools = PDFTools()
        self.qr_tools = QRTools()
        self.image_tools = ImageTools()
        self.convert_tools = ConvertTools()
        self.system_tools = SystemTools()
        self.net_tools = NetTools()
        
        self.is_pro = False
        self.current_tool = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_statusbar()
        
        self.setStyleSheet(self.get_stylesheet())

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 1)
        
        self.create_tool_pages()

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setMaximumWidth(250)
        sidebar.setMinimumWidth(200)
        
        layout = QVBoxLayout(sidebar)
        
        title = QLabel("Python\nToolbox")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 20px 0;")
        layout.addWidget(title)
        
        tools = [
            ("PDF Araçları", "pdf", self.show_pdf_tools),
            ("QR & Barkod", "qr", self.show_qr_tools),
            ("Görsel Araçları", "image", self.show_image_tools),
            ("Dosya Dönüştürücü", "convert", self.show_convert_tools),
            ("Sistem Araçları", "system", self.show_system_tools),
            ("İnternet Araçları", "net", self.show_net_tools)
        ]
        
        for tool_name, icon_name, callback in tools:
            btn = QPushButton(tool_name)
            btn.setIcon(QIcon(f":/icons/{icon_name}.png") if os.path.exists(f":/icons/{icon_name}.png") else QIcon())
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(callback)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 12px 20px;
                    margin: 2px 0;
                    border: none;
                    border-radius: 8px;
                    font-size: 13px;
                    font-weight: 500;
                    background-color: transparent;
                    color: #2c3e50;
                }
                QPushButton:hover {
                    background-color: #ecf0f1;
                }
                QPushButton:pressed {
                    background-color: #bdc3c7;
                }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        self.pro_label = QLabel("Free Version")
        self.pro_label.setAlignment(Qt.AlignCenter)
        self.pro_label.setStyleSheet("color: #7f8c8d; font-size: 11px; padding: 10px;")
        layout.addWidget(self.pro_label)
        
        return sidebar

    def create_tool_pages(self):
        self.pdf_page = self.create_pdf_page()
        self.qr_page = self.create_qr_page()
        self.image_page = self.create_image_page()
        self.convert_page = self.create_convert_page()
        self.system_page = self.create_system_page()
        self.net_page = self.create_net_page()
        
        self.content_area.addWidget(self.pdf_page)
        self.content_area.addWidget(self.qr_page)
        self.content_area.addWidget(self.image_page)
        self.content_area.addWidget(self.convert_page)
        self.content_area.addWidget(self.system_page)
        self.content_area.addWidget(self.net_page)

    def create_pdf_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("PDF Araçları")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        merge_tab = self.create_pdf_merge_tab()
        split_tab = self.create_pdf_split_tab()
        convert_tab = self.create_pdf_convert_tab()
        compress_tab = self.create_pdf_compress_tab()
        watermark_tab = self.create_pdf_watermark_tab()
        
        tabs.addTab(merge_tab, "Birleştirme")
        tabs.addTab(split_tab, "Ayırma")
        tabs.addTab(convert_tab, "Dönüştürme")
        tabs.addTab(compress_tab, "Sıkıştırma")
        tabs.addTab(watermark_tab, "Filigran")
        
        layout.addWidget(tabs)
        return page

    def create_pdf_merge_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        
        self.pdf_merge_files = []
        
        self.pdf_merge_list = QTextEdit()
        self.pdf_merge_list.setReadOnly(True)
        self.pdf_merge_list.setMaximumHeight(150)
        layout.addWidget(QLabel("PDF Dosyaları:"), 0, 0)
        layout.addWidget(self.pdf_merge_list, 1, 0, 1, 2)
        
        add_btn = QPushButton("Dosya Ekle")
        add_btn.clicked.connect(self.add_pdf_files)
        layout.addWidget(add_btn, 2, 0)
        
        merge_btn = QPushButton("PDF'leri Birleştir")
        merge_btn.clicked.connect(self.merge_pdfs)
        layout.addWidget(merge_btn, 2, 1)
        
        return tab

    def create_qr_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("QR & Barkod Araçları")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        generate_tab = self.create_qr_generate_tab()
        read_tab = self.create_qr_read_tab()
        barcode_tab = self.create_barcode_tab()
        
        tabs.addTab(generate_tab, "QR Üret")
        tabs.addTab(read_tab, "QR Oku")
        tabs.addTab(barcode_tab, "Barkod")
        
        layout.addWidget(tabs)
        return page

    def create_qr_generate_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        
        self.qr_text_input = QLineEdit()
        self.qr_text_input.setPlaceholderText("Metin, URL veya veri girin...")
        layout.addWidget(QLabel("Veri:"), 0, 0)
        layout.addWidget(self.qr_text_input, 0, 1)
        
        generate_btn = QPushButton("QR Kod Oluştur")
        generate_btn.clicked.connect(self.generate_qr)
        layout.addWidget(generate_btn, 1, 0, 1, 2)
        
        self.qr_result_label = QLabel()
        self.qr_result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.qr_result_label, 2, 0, 1, 2)
        
        return tab

    def create_image_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Görsel Araçları")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        convert_tab = self.create_image_convert_tab()
        resize_tab = self.create_image_resize_tab()
        watermark_tab = self.create_image_watermark_tab()
        optimize_tab = self.create_image_optimize_tab()
        
        tabs.addTab(convert_tab, "Dönüştürme")
        tabs.addTab(resize_tab, "Yeniden Boyutlandırma")
        tabs.addTab(watermark_tab, "Filigran")
        tabs.addTab(optimize_tab, "Optimize")
        
        layout.addWidget(tabs)
        return page

    def create_convert_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Dosya Dönüştürücü")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        excel_tab = self.create_excel_convert_tab()
        document_tab = self.create_document_convert_tab()
        
        tabs.addTab(excel_tab, "Excel/JSON/CSV")
        tabs.addTab(document_tab, "Doküman")
        
        layout.addWidget(tabs)
        return page

    def create_system_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Sistem Araçları")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        hash_tab = self.create_hash_tab()
        encrypt_tab = self.create_encrypt_tab()
        zip_tab = self.create_zip_tab()
        
        tabs.addTab(hash_tab, "Hash")
        tabs.addTab(encrypt_tab, "Şifreleme")
        tabs.addTab(zip_tab, "ZIP")
        
        layout.addWidget(tabs)
        return page

    def create_net_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("İnternet Araçları")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        tabs = QTabWidget()
        
        youtube_tab = self.create_youtube_tab()
        speed_tab = self.create_speed_test_tab()
        url_tab = self.create_url_tab()
        
        tabs.addTab(youtube_tab, "YouTube")
        tabs.addTab(speed_tab, "Hız Testi")
        tabs.addTab(url_tab, "URL Araçları")
        
        layout.addWidget(tabs)
        return page

    def setup_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("Dosya")
        file_menu.addAction("Lisans Yükle", self.load_license)
        file_menu.addSeparator()
        file_menu.addAction("Çıkış", self.close)
        
        help_menu = menubar.addMenu("Yardım")
        help_menu.addAction("Hakkında", self.show_about)

    def setup_statusbar(self):
        self.statusbar = self.statusBar()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.statusbar.addPermanentWidget(self.progress_bar)

    def show_pdf_tools(self):
        self.content_area.setCurrentIndex(0)
        self.current_tool = "PDF"

    def show_qr_tools(self):
        self.content_area.setCurrentIndex(1)
        self.current_tool = "QR"

    def show_image_tools(self):
        self.content_area.setCurrentIndex(2)
        self.current_tool = "Image"

    def show_convert_tools(self):
        self.content_area.setCurrentIndex(3)
        self.current_tool = "Convert"

    def show_system_tools(self):
        self.content_area.setCurrentIndex(4)
        self.current_tool = "System"

    def show_net_tools(self):
        self.content_area.setCurrentIndex(5)
        self.current_tool = "Net"

    def add_pdf_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "PDF Dosyaları Seç", "", "PDF Files (*.pdf)")
        if files:
            self.pdf_merge_files.extend(files)
            self.pdf_merge_list.setPlainText("\n".join(self.pdf_merge_files))

    def merge_pdfs(self):
        if not self.pdf_merge_files:
            QMessageBox.warning(self, "Uyarı", "Lütfen birleştirilecek PDF dosyalarını seçin!")
            return
        
        if not self.is_pro and len(self.pdf_merge_files) > 5:
            QMessageBox.warning(self, "Free Version", "Free versiyonda en fazla 5 PDF birleştirebilirsiniz!")
            return
        
        output_file, _ = QFileDialog.getSaveFileName(self, "Çıktı Dosyası", "", "PDF Files (*.pdf)")
        if output_file:
            try:
                self.pdf_tools.merge_pdfs(self.pdf_merge_files, output_file)
                QMessageBox.information(self, "Başarılı", "PDF dosyaları başarıyla birleştirildi!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Birleştirme hatası: {str(e)}")

    def generate_qr(self):
        text = self.qr_text_input.text()
        if not text:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir metin girin!")
            return
        
        try:
            output_path = "qr_code.png"
            self.qr_tools.generate_qr(text, output_path)
            pixmap = QPixmap(output_path)
            self.qr_result_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            QMessageBox.information(self, "Başarılı", f"QR kod oluşturuldu: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"QR oluşturma hatası: {str(e)}")

    def load_license(self):
        file, _ = QFileDialog.getOpenFileName(self, "Lisans Dosyası Seç", "", "JSON Files (*.json)")
        if file:
            try:
                import json
                with open(file, 'r') as f:
                    license_data = json.load(f)
                
                if self.verify_license(license_data):
                    self.is_pro = True
                    self.pro_label.setText("Pro Version")
                    self.pro_label.setStyleSheet("color: #27ae60; font-size: 11px; padding: 10px; font-weight: bold;")
                    QMessageBox.information(self, "Başarılı", "Pro lisans başarıyla yüklendi!")
                else:
                    QMessageBox.warning(self, "Hata", "Geçersiz lisans dosyası!")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Lisans yükleme hatası: {str(e)}")

    def verify_license(self, license_data):
        return True

    def show_about(self):
        QMessageBox.about(self, "Hakkında", "Python Toolbox v1.0\nProfesyonel Araç Seti\n\nTüm hakları saklıdır.")

    def create_pdf_split_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("PDF Ayırma Aracı - Yakında"), 0, 0)
        return tab

    def create_pdf_convert_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("PDF Dönüştürme Aracı - Yakında"), 0, 0)
        return tab

    def create_pdf_compress_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("PDF Sıkıştırma Aracı - Yakında"), 0, 0)
        return tab

    def create_pdf_watermark_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("PDF Filigran Aracı - Yakında"), 0, 0)
        return tab

    def create_qr_read_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("QR Okuma Aracı - Yakında"), 0, 0)
        return tab

    def create_barcode_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Barkod Aracı - Yakında"), 0, 0)
        return tab

    def create_image_convert_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Görsel Dönüştürme Aracı - Yakında"), 0, 0)
        return tab

    def create_image_resize_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Görsel Yeniden Boyutlandırma Aracı - Yakında"), 0, 0)
        return tab

    def create_image_watermark_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Görsel Filigran Aracı - Yakında"), 0, 0)
        return tab

    def create_image_optimize_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Görsel Optimize Aracı - Yakında"), 0, 0)
        return tab

    def create_excel_convert_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Excel/JSON/CSV Dönüştürme Aracı - Yakında"), 0, 0)
        return tab

    def create_document_convert_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Doküman Dönüştürme Aracı - Yakında"), 0, 0)
        return tab

    def create_hash_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Hash Hesaplama Aracı - Yakında"), 0, 0)
        return tab

    def create_encrypt_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("Şifreleme Aracı - Yakında"), 0, 0)
        return tab

    def create_zip_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("ZIP Aracı - Yakında"), 0, 0)
        return tab

    def create_youtube_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("YouTube Thumbnail İndirici - Yakında"), 0, 0)
        return tab

    def create_speed_test_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("İnternet Hız Testi - Yakında"), 0, 0)
        return tab

    def create_url_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.addWidget(QLabel("URL Araçları - Yakında"), 0, 0)
        return tab

    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #ffffff;
            }
            
            QFrame {
                border: none;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1f5f8b;
            }
            
            QLineEdit {
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
            }
            
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
            
            QTabWidget::pane {
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #ffffff;
            }
            
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            
            QLabel {
                color: #2c3e50;
                font-size: 13px;
            }
            
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                text-align: center;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """