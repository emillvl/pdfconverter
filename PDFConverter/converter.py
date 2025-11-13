import os
import platform
import subprocess
from tkinter import Tk, filedialog, simpledialog, messagebox
from PIL import Image

def get_desktop_path():
    system = platform.system()
    if system == "Windows":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        desktop_path = winreg.QueryValueEx(key, 'Desktop')[0]
        winreg.CloseKey(key)
        return desktop_path
    elif system in ("Linux", "Darwin"): 
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        return os.path.expanduser("~")

def check_libreoffice():
    try:
        result = subprocess.run(
            [r"C:\Program Files\LibreOffice\program\soffice.exe", "--version"], 
            capture_output=True 
        )
        if result.returncode != 0:
            raise FileNotFoundError
        return True
    except (FileNotFoundError, Exception):
        messagebox.showerror(
            "LibreOffice Bulunamadı",
            "Bilgisayarınızda LibreOffice bulunamadı.\n"
            "Resim dosyaları dışındaki dosyaları PDF'e dönüştürmek için LibreOffice yüklemeniz gerekmektedir."
        )
        return False

def images_to_pdf(image_files, output_pdf):
    try:
        images = []
        for img_file in image_files:
            try:
                img = Image.open(img_file).convert("RGB")
                images.append(img)
            except Exception as e:
                messagebox.showerror("Hata", f"Resim açılırken hata oluştu:\n{img_file}\n\n{str(e)}")
                return False
        
        if not images:
            messagebox.showerror("Hata", "Hiçbir resim açılamadı.")
            return False
            
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"Resimler başarıyla PDF'e dönüştürüldü: {output_pdf}")
        messagebox.showinfo("Başarılı", f"Dosya başarıyla dönüştürüldü!\n\n{output_pdf}")
        return True
    except Exception as e:
        messagebox.showerror("Hata", f"Resimler PDF'e dönüştürülürken hata oluştu:\n{str(e)}")
        return False

def convert_with_libreoffice(input_files, output_pdf):
    if not check_libreoffice():
        return False

    try:
        input_dir = os.path.dirname(input_files[0])
        temp_pdfs = []
        
        for input_file in input_files:
            try:
                result = subprocess.run([
                    r"C:\Program Files\LibreOffice\program\soffice.exe", 
                    "--convert-to", "pdf",
                    "--outdir", input_dir, input_file
                ], check=True)
                
                temp_pdf = os.path.join(input_dir, os.path.splitext(os.path.basename(input_file))[0] + ".pdf")
                
                if not os.path.exists(temp_pdf):
                    raise FileNotFoundError(f"PDF oluşturulamadı: {temp_pdf}")
                    
                temp_pdfs.append(temp_pdf)
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya dönüştürülürken hata oluştu:\n{input_file}\n\n{str(e)}")
                for pdf in temp_pdfs:
                    if os.path.exists(pdf):
                        try:
                            os.remove(pdf)
                        except:
                            pass
                return False
        
        if len(temp_pdfs) > 1:
            try:
                from PyPDF2 import PdfMerger
                merger = PdfMerger()
                
                for pdf in temp_pdfs:
                    try:
                        merger.append(pdf)
                    except Exception as e:
                        merger.close()
                        raise Exception(f"PDF birleştirme hatası ({pdf}): {str(e)}")
                
                merger.write(output_pdf)
                merger.close()
                
                for pdf in temp_pdfs:
                    if os.path.exists(pdf):
                        try:
                            os.remove(pdf)
                        except Exception as e:
                            print(f"Geçici dosya silinemedi: {pdf} - {str(e)}")
                            
                print(f"Dosyalar başarıyla birleştirildi: {output_pdf}")
                messagebox.showinfo("Başarılı", f"Dosyalar başarıyla dönüştürüldü ve birleştirildi!\n\n{output_pdf}")
            except ImportError:
                messagebox.showwarning(
                    "PyPDF2 Gerekli",
                    "Birden fazla dosyayı birleştirmek için PyPDF2 kütüphanesi gereklidir.\n"
                    "Komut: pip install PyPDF2\n\n"
                    f"Dosyalar ayrı ayrı kaydedildi:\n" + "\n".join(temp_pdfs)
                )
                return False
            except Exception as e:
                messagebox.showerror("Hata", f"PDF'ler birleştirilirken hata oluştu:\n{str(e)}")
                for pdf in temp_pdfs:
                    if os.path.exists(pdf):
                        try:
                            os.remove(pdf)
                        except:
                            pass
                return False
        else:
            if temp_pdfs[0] != output_pdf:
                try:
                    import shutil
                    shutil.move(temp_pdfs[0], output_pdf)
                    print(f"Dosya başarıyla dönüştürüldü: {output_pdf}")
                    messagebox.showinfo("Başarılı", f"Dosya başarıyla dönüştürüldü!\n\n{output_pdf}")
                except Exception as e:
                    messagebox.showerror("Hata", f"Dosya taşınırken hata oluştu:\n{str(e)}")
                    return False
            else:
                print(f"Dosya başarıyla dönüştürüldü: {output_pdf}")
                messagebox.showinfo("Başarılı", f"Dosya başarıyla dönüştürüldü!\n\n{output_pdf}")
        
        return True
    except Exception as e:
        messagebox.showerror("Hata", f"Dönüştürme sırasında beklenmeyen hata oluştu:\n{str(e)}")
        return False

def main():
    root = Tk()
    root.withdraw()
    
    messagebox.showinfo(
        "PDF Dönüştürücü",
        "PDF Dönüştürücü v1.0\n\n© 2025 Emil Veliyev. Tüm hakları saklıdır."
    )
    
    files = filedialog.askopenfilenames(title="PDF'e dönüştürülecek dosyaları seç")
    if not files:
        print("Dosya seçilmedi.")
        return

    pdf_name = simpledialog.askstring("PDF Adı", "Kaydedilecek PDF dosya adını girin :")
    if not pdf_name:
        print("PDF adı girilmedi.")
        return
    if not pdf_name.lower().endswith(".pdf"):
        pdf_name += ".pdf"

    desktop = get_desktop_path()
    output_pdf = os.path.join(desktop, pdf_name)
    
    print(f"Kaydetme Yolu: {output_pdf}")

    if all(f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")) for f in files):
        images_to_pdf(list(files), output_pdf)
        return

    convert_with_libreoffice(list(files), output_pdf)

if __name__ == "__main__":
    main()