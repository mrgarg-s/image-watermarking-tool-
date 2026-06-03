import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib
import base64
import os
import platform
import subprocess
from PIL import Image

# --- Feature Flags & Imports ---
try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

class VulcanDecrypterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vulcan Meta Decrypter")
        self.root.geometry("600x550")
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon1.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Could not set icon: {e}")
        
        # Dark theme colors
        self.bg_color = "#121212"
        self.panel_color = "#1e1e1e"
        self.text_color = "#ffffff"
        self.accent_color = "#03DAC6" 
        
        self.root.configure(bg=self.bg_color)
        self.file_path = None
        
        self.setup_ui()
        
        # Register Drag and Drop if library is available
        if HAS_DND:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.handle_drop)

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Arial", 10))
        style.configure("TButton", background="#333333", foreground=self.text_color, font=("Arial", 10, "bold"), padding=5)
        style.map("TButton", background=[("active", self.accent_color)])
        
        # Header
        header = tk.Label(self.root, text="VULCAN SECURE DECRYPTER", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.accent_color)
        header.pack(pady=(20, 5))
        
        if HAS_DND:
            tk.Label(self.root, text="[ Drag and Drop Supported ]", font=("Arial", 9, "italic"), bg=self.bg_color, fg="#888888").pack()

        # File Upload Section
        frame_file = ttk.Frame(self.root)
        frame_file.pack(fill=tk.X, padx=30, pady=15)
        
        ttk.Label(frame_file, text="Step 1: Select File (PNG, DOCX, JPG, PDF, ENC)").pack(anchor=tk.W)
        self.lbl_filename = ttk.Label(frame_file, text="No file selected...", foreground="#888888")
        self.lbl_filename.pack(side=tk.LEFT, pady=5)
        
        ttk.Button(frame_file, text="Browse Files", command=self.browse_file).pack(side=tk.RIGHT)

        # Password Section
        frame_pwd = ttk.Frame(self.root)
        frame_pwd.pack(fill=tk.X, padx=30, pady=10)
        
        ttk.Label(frame_pwd, text="Step 2: Enter Password (if encrypted)").pack(anchor=tk.W)
        
        pwd_inner = ttk.Frame(frame_pwd)
        pwd_inner.pack(fill=tk.X, pady=5)
        
        self.pwd_var = tk.StringVar()
        self.entry_pwd = ttk.Entry(pwd_inner, textvariable=self.pwd_var, show="*", font=("Arial", 12))
        self.entry_pwd.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.show_pwd = tk.BooleanVar(value=False)
        ttk.Checkbutton(pwd_inner, text="👁 Show", style="Toolbutton", variable=self.show_pwd, command=self.toggle_pwd).pack(side=tk.RIGHT, padx=(5,0))

        # Action Button
        ttk.Button(self.root, text="READ & DECRYPT", command=self.process_file).pack(fill=tk.X, padx=30, pady=20)

        # Output Text Box
        ttk.Label(self.root, text="Extracted Information:").pack(anchor=tk.W, padx=30)
        self.txt_output = tk.Text(self.root, height=10, bg=self.panel_color, fg=self.text_color, font=("Consolas", 10), bd=0, padx=10, pady=10)
        self.txt_output.pack(fill=tk.BOTH, expand=True, padx=30, pady=(5, 20))
        self.txt_output.config(state=tk.DISABLED)

    def toggle_pwd(self):
        if self.show_pwd.get():
            self.entry_pwd.config(show="")
        else:
            self.entry_pwd.config(show="*")

    def handle_drop(self, event):
        filepath = event.data
        if filepath.startswith('{') and filepath.endswith('}'):
            filepath = filepath[1:-1]
        self.set_file(filepath)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("All Supported", "*.png *.docx *.jpg *.jpeg *.pdf *.enc"),
                       ("PNG Images", "*.png"), 
                       ("Word Documents", "*.docx"),
                       ("Encrypted Files", "*.enc"),
                       ("JPEG / PDF", "*.jpg *.jpeg *.pdf")]
        )
        if filepath:
            self.set_file(filepath)

    def set_file(self, filepath):
        self.file_path = filepath
        short_name = os.path.basename(filepath)
        self.lbl_filename.config(text=short_name, foreground=self.accent_color)
        self.write_output(f"File loaded: {short_name}\nReady to read data.")

    def write_output(self, text):
        self.txt_output.config(state=tk.NORMAL)
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, text)
        self.txt_output.config(state=tk.DISABLED)

    def process_file(self):
        if not self.file_path:
            messagebox.showwarning("Missing File", "Please select a file or drag and drop one first!")
            return
            
        target_path = self.file_path
        pwd = self.pwd_var.get().strip()

        # --- FULL FILE DECRYPTION LOGIC ---
        is_full_encrypted = False
        try:
            with open(target_path, 'rb') as f:
                header = f.read(10)
            if header.startswith(b'gAAAAA'):
                is_full_encrypted = True
        except Exception:
            pass

        if is_full_encrypted:
            if not pwd:
                self.write_output("STATUS: FULL FILE ENCRYPTION DETECTED\n\nYou must enter a password to decrypt and open this file.")
                return
            if not HAS_CRYPTO:
                self.write_output("ERROR: cryptography library is missing. Cannot decrypt file.")
                return
                
            try:
                pwd_bytes = pwd.encode()
                key = base64.urlsafe_b64encode(hashlib.sha256(pwd_bytes).digest())
                f_crypto = Fernet(key)
                
                with open(target_path, 'rb') as f:
                    encrypted_data = f.read()
                    
                decrypted_data = f_crypto.decrypt(encrypted_data)
                
                # Setup decrypted file path
                base_name = target_path
                if base_name.endswith(".enc"):
                    base_name = base_name[:-4]
                else:
                    base_name = base_name + ".decrypted"
                
                dir_name = os.path.dirname(target_path)
                file_name = os.path.basename(base_name)
                target_path = os.path.join(dir_name, "decrypted_" + file_name)
                
                with open(target_path, 'wb') as f:
                    f.write(decrypted_data)
                    
                self.write_output(f"STATUS: FILE DECRYPTED SUCCESSFULLY.\nSaved to: {target_path}\nReading Metadata...\n")
            except Exception as e:
                self.write_output("ERROR: Failed to decrypt file. Wrong password?\n" + str(e))
                return


        # --- METADATA EXTRACTION LOGIC ---
        ext = target_path.lower()
        auth_txt = ""
        copy_txt = ""

        try:
            # 1. Handle JPEGs and PDFs (Vulcan limitation)
            if ext.endswith(('.jpg', '.jpeg', '.pdf')):
                # Only warn if it wasn't a fully encrypted file that we just cracked open
                if not is_full_encrypted:
                    self.write_output("STATUS: FORMAT LIMITATION\n\nBased on the Vulcan software's export logic, hidden metadata is NOT saved into JPEG or PDF files. Vulcan only embeds secure data inside PNG files or writes it visibly into Word documents.")
                    return
                else:
                    output_text = self.txt_output.get("1.0", tk.END).strip() + "\n\nSTATUS: METADATA EXTRACTION SKIPPED\nFile is a JPEG/PDF which does not hold Vulcan metadata."

            # 2. Handle Word Documents
            elif ext.endswith('.docx'):
                if not HAS_DOCX:
                    self.write_output("ERROR: python-docx library is missing.\nPlease install it to read Word documents.")
                    return
                doc = docx.Document(target_path)
                for para in doc.paragraphs:
                    text = para.text
                    if text.startswith("Author: "):
                        auth_txt = text.replace("Author: ", "").strip()
                    elif text.startswith("Copyright: "):
                        copy_txt = text.replace("Copyright: ", "").strip()

            # 3. Handle PNG Images
            elif ext.endswith('.png'):
                img = Image.open(target_path)
                auth_txt = img.info.get("Author", "")
                copy_txt = img.info.get("Copyright", "")
            
            else:
                self.write_output("ERROR: Unsupported file format for metadata read.")
                return

            # --- METADATA DECRYPTION LOGIC ---
            output_text = self.txt_output.get("1.0", tk.END).strip() + "\n\n" if is_full_encrypted else ""

            if not auth_txt and not copy_txt:
                if not ext.endswith(('.jpg', '.jpeg', '.pdf')):
                    output_text += "STATUS: No metadata found in file.\nThis file does not contain Vulcan watermark data."
            else:
                is_meta_encrypted = "gAAAAA" in auth_txt or "gAAAAA" in copy_txt

                if is_meta_encrypted:
                    if not pwd:
                        output_text += f"STATUS: ENCRYPTED METADATA DETECTED\nYou must enter a password to decrypt this data.\n\nRaw Data Preview:\n{auth_txt[:30]}..."
                    elif not HAS_CRYPTO:
                        output_text += "ERROR: cryptography library is missing. Cannot decrypt data."
                    else:
                        pwd_bytes = pwd.encode()
                        key = base64.urlsafe_b64encode(hashlib.sha256(pwd_bytes).digest())
                        f_crypto = Fernet(key)
                        
                        output_text += "STATUS: METADATA DECRYPTED SECURELY\n" + "-"*35 + "\n"
                        try:
                            dec_auth = f_crypto.decrypt(auth_txt.encode()).decode()
                            output_text += f"AUTHOR    : {dec_auth}\n"
                        except:
                            output_text += "AUTHOR    : [Decryption Failed - Wrong Password?]\n"
                            
                        try:
                            dec_copy = f_crypto.decrypt(copy_txt.encode()).decode()
                            output_text += f"COPYRIGHT : {dec_copy}\n"
                        except:
                            output_text += "COPYRIGHT : [Decryption Failed - Wrong Password?]\n"
                else:
                    output_text += "STATUS: PLAIN TEXT METADATA\n" + "-"*35 + "\n"
                    output_text += f"AUTHOR    : {auth_txt}\n"
                    output_text += f"COPYRIGHT : {copy_txt}\n"

            self.write_output(output_text.strip())

        except Exception as e:
            self.write_output(self.txt_output.get("1.0", tk.END) + f"\n\nERROR: Could not process file metadata.\n{str(e)}")

        # --- AUTO-LAUNCH DECRYPTED FILE ---
        if is_full_encrypted:
            try:
                if platform.system() == 'Darwin':       # macOS
                    subprocess.call(('open', target_path))
                elif platform.system() == 'Windows':    # Windows
                    os.startfile(target_path)
                else:                                   # Linux variants
                    subprocess.call(('xdg-open', target_path))
            except Exception as e:
                self.write_output(self.txt_output.get("1.0", tk.END) + f"\n\n[Warning] Could not auto-launch the decrypted file in the viewer: {e}")


if __name__ == "__main__":
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        print("Warning: tkinterdnd2 missing. Drag and drop disabled.")
        
    app = VulcanDecrypterApp(root)
    root.mainloop()