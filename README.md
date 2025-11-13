# 📄 PDF Converter

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/Version-1.0-orange.svg)

**🚀 A powerful and user-friendly tool to convert multiple file formats to PDF**

[English](#english) | [Türkçe](#turkish)

</div>

---

## <a name="english"></a>🇬🇧 English

### ✨ Features

- 🖼️ **Image to PDF**: Convert PNG, JPG, JPEG, BMP, GIF images to PDF
- 📝 **Document to PDF**: Convert Word, Excel, PowerPoint, and other office documents to PDF
- 🔗 **Multi-file Merging**: Combine multiple files into a single PDF
- 🖥️ **Cross-platform**: Works on Windows, macOS, and Linux
- 🎯 **Simple GUI**: Easy-to-use interface with file selection dialogs
- 💾 **Desktop Output**: Automatically saves PDFs to your desktop

### 📋 Requirements

#### Required Dependencies
```bash
pip install Pillow
```

#### Optional Dependencies
- **LibreOffice**: Required for converting non-image files (Word, Excel, PowerPoint, etc.)
  - [Download LibreOffice](https://www.libreoffice.org/download/download/)
- **PyPDF2**: Required for merging multiple files
  ```bash
  pip install PyPDF2
  ```

### 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-converter.git
   cd pdf-converter
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install LibreOffice** (for document conversion)
   - Download and install from [LibreOffice official website](https://www.libreoffice.org/)

### 💻 Usage

1. **Run the application**
   ```bash
   python pdf_converter.py
   ```

2. **Select files** to convert using the file dialog

3. **Enter a name** for your PDF file

4. **Done!** Your PDF will be saved to your desktop

### 📦 Supported File Formats

| Category | Formats |
|----------|---------|
| **Images** | PNG, JPG, JPEG, BMP, GIF |
| **Documents** | DOC, DOCX, ODT, RTF |
| **Spreadsheets** | XLS, XLSX, ODS, CSV |
| **Presentations** | PPT, PPTX, ODP |
| **Other** | TXT, HTML, and more |

### 🛠️ How It Works

1. **Image Files**: Uses Pillow (PIL) to convert and merge images into a single PDF
2. **Document Files**: Leverages LibreOffice command-line tools for conversion
3. **Multiple Files**: PyPDF2 merges individual PDFs into one final document

### ⚠️ Error Handling

The application includes comprehensive error handling:
- ✅ Checks for LibreOffice installation
- ✅ Validates file formats
- ✅ Provides clear error messages
- ✅ Cleans up temporary files automatically

### 📝 License

© 2025 Emil Veliyev. All rights reserved.

### 🤝 Contributing

Contributions, issues, and feature requests are welcome!

### 📧 Contact

Created by **Emil Veliyev**

---

## <a name="turkish"></a>🇹🇷 Türkçe

### ✨ Özellikler

- 🖼️ **Resimden PDF'e**: PNG, JPG, JPEG, BMP, GIF resimlerini PDF'e dönüştürün
- 📝 **Belgeden PDF'e**: Word, Excel, PowerPoint ve diğer ofis belgelerini PDF'e dönüştürün
- 🔗 **Çoklu Dosya Birleştirme**: Birden fazla dosyayı tek bir PDF'de birleştirin
- 🖥️ **Platformlar arası**: Windows, macOS ve Linux'ta çalışır
- 🎯 **Basit Arayüz**: Dosya seçim diyalogları ile kullanımı kolay arayüz
- 💾 **Masaüstü Çıktı**: PDF'leri otomatik olarak masaüstünüze kaydeder

### 📋 Gereksinimler

#### Zorunlu Bağımlılıklar
```bash
pip install Pillow
```

#### İsteğe Bağlı Bağımlılıklar
- **LibreOffice**: Resim olmayan dosyaları dönüştürmek için gereklidir (Word, Excel, PowerPoint, vb.)
  - [LibreOffice'i İndir](https://www.libreoffice.org/download/download/)
- **PyPDF2**: Birden fazla dosyayı birleştirmek için gereklidir
  ```bash
  pip install PyPDF2
  ```

### 🚀 Kurulum

1. **Depoyu klonlayın**
   ```bash
   git clone https://github.com/yourusername/pdf-converter.git
   cd pdf-converter
   ```

2. **Gerekli paketleri yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

3. **LibreOffice'i yükleyin** (belge dönüştürme için)
   - [LibreOffice resmi web sitesinden](https://www.libreoffice.org/) indirip yükleyin

### 💻 Kullanım

1. **Uygulamayı çalıştırın**
   ```bash
   python pdf_converter.py
   ```

2. Dosya diyalogu ile dönüştürülecek **dosyaları seçin**

3. PDF dosyanız için **bir isim girin**

4. **Tamamlandı!** PDF'niz masaüstünüze kaydedilecek

### 📦 Desteklenen Dosya Formatları

| Kategori | Formatlar |
|----------|-----------|
| **Resimler** | PNG, JPG, JPEG, BMP, GIF |
| **Belgeler** | DOC, DOCX, ODT, RTF |
| **Tablolar** | XLS, XLSX, ODS, CSV |
| **Sunumlar** | PPT, PPTX, ODP |
| **Diğer** | TXT, HTML ve daha fazlası |

### 🛠️ Nasıl Çalışır

1. **Resim Dosyaları**: Pillow (PIL) kullanarak resimleri tek bir PDF'e dönüştürür ve birleştirir
2. **Belge Dosyaları**: Dönüştürme için LibreOffice komut satırı araçlarından yararlanır
3. **Çoklu Dosyalar**: PyPDF2 tek tek PDF'leri tek bir nihai belgede birleştirir

### ⚠️ Hata Yönetimi

Uygulama kapsamlı hata yönetimi içerir:
- ✅ LibreOffice kurulumunu kontrol eder
- ✅ Dosya formatlarını doğrular
- ✅ Net hata mesajları sağlar
- ✅ Geçici dosyaları otomatik olarak temizler

### 📝 Lisans

© 2025 Emil Veliyev. Tüm hakları saklıdır.

### 🤝 Katkıda Bulunma

Katkılar, sorunlar ve özellik istekleri memnuniyetle karşılanır!

### 📧 İletişim

**Emil Veliyev** tarafından oluşturuldu

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! | If you like this project, don't forget to give it a star! ⭐**

</div>
