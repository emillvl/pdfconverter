import os
import platform
import shutil
import subprocess
import tempfile
from tkinter import Tk, filedialog, messagebox, simpledialog

from PIL import Image


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")


def get_desktop_path():
    """Return the user's desktop directory, falling back to the home directory."""
    home = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            ) as key:
                desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
            desktop_path = os.path.expandvars(desktop_path)
            if os.path.isdir(desktop_path):
                return desktop_path
        except (OSError, ImportError):
            pass

    if system == "Linux":
        xdg_user_dir = shutil.which("xdg-user-dir")
        if xdg_user_dir:
            try:
                result = subprocess.run(
                    [xdg_user_dir, "DESKTOP"],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                desktop_path = result.stdout.strip()
                if os.path.isdir(desktop_path):
                    return desktop_path
            except (OSError, subprocess.SubprocessError):
                pass

    desktop_path = os.path.join(home, "Desktop")
    return desktop_path if os.path.isdir(desktop_path) else home


def find_libreoffice():
    """Find a LibreOffice executable on supported desktop platforms."""
    for executable_name in ("soffice", "libreoffice"):
        executable = shutil.which(executable_name)
        if executable:
            return executable

    system = platform.system()
    candidates = []

    if system == "Windows":
        for env_name in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
            base_dir = os.environ.get(env_name)
            if base_dir:
                candidates.append(
                    os.path.join(base_dir, "LibreOffice", "program", "soffice.exe")
                )
    elif system == "Darwin":
        candidates.append("/Applications/LibreOffice.app/Contents/MacOS/soffice")

    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate

    return None


def check_libreoffice():
    """Return the LibreOffice executable path when it is available and runnable."""
    executable = find_libreoffice()
    if not executable:
        messagebox.showerror(
            "LibreOffice Bulunamadı",
            "Bilgisayarınızda LibreOffice bulunamadı.\n"
            "Resim dosyaları dışındaki dosyaları PDF'e dönüştürmek için "
            "LibreOffice yüklemeniz gerekmektedir.",
        )
        return None

    try:
        result = subprocess.run(
            [executable, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if not result.stdout.strip() and not result.stderr.strip():
            raise RuntimeError("LibreOffice sürümü doğrulanamadı.")
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        messagebox.showerror(
            "LibreOffice Başlatılamadı",
            "LibreOffice bulundu ancak çalıştırılamadı.\n\n"
            f"{exc}",
        )
        return None

    return executable


def images_to_pdf(image_files, output_pdf):
    images = []

    try:
        for image_file in image_files:
            try:
                with Image.open(image_file) as image:
                    images.append(image.convert("RGB"))
            except Exception as exc:
                messagebox.showerror(
                    "Hata",
                    f"Resim açılırken hata oluştu:\n{image_file}\n\n{exc}",
                )
                return False

        if not images:
            messagebox.showerror("Hata", "Hiçbir resim açılamadı.")
            return False

        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"Resimler başarıyla PDF'e dönüştürüldü: {output_pdf}")
        messagebox.showinfo(
            "Başarılı",
            f"Dosya başarıyla dönüştürüldü!\n\n{output_pdf}",
        )
        return True
    except Exception as exc:
        messagebox.showerror(
            "Hata",
            f"Resimler PDF'e dönüştürülürken hata oluştu:\n{exc}",
        )
        return False
    finally:
        for image in images:
            try:
                image.close()
            except Exception:
                pass


def _convert_file_with_libreoffice(executable, input_file, output_dir):
    result = subprocess.run(
        [
            executable,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            output_dir,
            input_file,
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    expected_pdf = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(input_file))[0] + ".pdf",
    )

    if result.returncode != 0 or not os.path.isfile(expected_pdf):
        details = (result.stderr or result.stdout).strip()
        if not details:
            details = "LibreOffice PDF çıktısı oluşturmadı."
        raise RuntimeError(details)

    return expected_pdf


def convert_with_libreoffice(input_files, output_pdf):
    executable = check_libreoffice()
    if not executable:
        return False

    try:
        with tempfile.TemporaryDirectory(prefix="pdfconverter_") as temp_root:
            converted_pdfs = []

            for index, input_file in enumerate(input_files):
                output_dir = os.path.join(temp_root, str(index))
                os.makedirs(output_dir, exist_ok=True)

                try:
                    converted_pdf = _convert_file_with_libreoffice(
                        executable,
                        input_file,
                        output_dir,
                    )
                    converted_pdfs.append(converted_pdf)
                except Exception as exc:
                    messagebox.showerror(
                        "Hata",
                        f"Dosya dönüştürülürken hata oluştu:\n"
                        f"{input_file}\n\n{exc}",
                    )
                    return False

            if len(converted_pdfs) > 1:
                try:
                    from PyPDF2 import PdfMerger
                except ImportError:
                    messagebox.showwarning(
                        "PyPDF2 Gerekli",
                        "Birden fazla dosyayı birleştirmek için PyPDF2 "
                        "kütüphanesi gereklidir.\n"
                        "Komut: pip install PyPDF2",
                    )
                    return False

                merger = PdfMerger()
                try:
                    for pdf in converted_pdfs:
                        merger.append(pdf)
                    merger.write(output_pdf)
                except Exception as exc:
                    messagebox.showerror(
                        "Hata",
                        f"PDF'ler birleştirilirken hata oluştu:\n{exc}",
                    )
                    return False
                finally:
                    merger.close()

                print(f"Dosyalar başarıyla birleştirildi: {output_pdf}")
                messagebox.showinfo(
                    "Başarılı",
                    "Dosyalar başarıyla dönüştürüldü ve birleştirildi!"
                    f"\n\n{output_pdf}",
                )
                return True

            shutil.copyfile(converted_pdfs[0], output_pdf)
            print(f"Dosya başarıyla dönüştürüldü: {output_pdf}")
            messagebox.showinfo(
                "Başarılı",
                f"Dosya başarıyla dönüştürüldü!\n\n{output_pdf}",
            )
            return True

    except Exception as exc:
        messagebox.showerror(
            "Hata",
            f"Dönüştürme sırasında beklenmeyen hata oluştu:\n{exc}",
        )
        return False


def main():
    root = Tk()
    root.withdraw()

    messagebox.showinfo(
        "PDF Dönüştürücü",
        "PDF Dönüştürücü v1.0\n\n© 2025 Emil Veliyev. Tüm hakları saklıdır.",
    )

    files = filedialog.askopenfilenames(
        title="PDF'e dönüştürülecek dosyaları seç"
    )
    if not files:
        print("Dosya seçilmedi.")
        return

    pdf_name = simpledialog.askstring(
        "PDF Adı",
        "Kaydedilecek PDF dosya adını girin:",
    )
    if not pdf_name:
        print("PDF adı girilmedi.")
        return

    pdf_name = pdf_name.strip()
    if not pdf_name:
        print("PDF adı girilmedi.")
        return

    if not pdf_name.lower().endswith(".pdf"):
        pdf_name += ".pdf"

    desktop = get_desktop_path()
    output_pdf = os.path.join(desktop, pdf_name)

    print(f"Kaydetme Yolu: {output_pdf}")

    if all(file.lower().endswith(IMAGE_EXTENSIONS) for file in files):
        images_to_pdf(list(files), output_pdf)
        return

    convert_with_libreoffice(list(files), output_pdf)


if __name__ == "__main__":
    main()
