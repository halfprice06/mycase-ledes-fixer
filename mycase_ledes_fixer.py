import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, StringVar, BooleanVar
import os
import threading
import logging
from tkinterdnd2 import DND_FILES, TkinterDnD
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
import sys

# Set up logging
app_data = os.path.join(os.getenv('APPDATA'), 'MyCase LEDES Fixer')
if not os.path.exists(app_data):
    os.makedirs(app_data)

logging.basicConfig(
    filename=os.path.join(app_data, 'mycase_ledes_fixer.log'),
    level=logging.ERROR
)

# Design system
DESIGN = {
    'colors': {
        'primary': '#2563eb',
        'surface': '#1e293b',
        'background': '#0f172a',
        'text': '#f8fafc',
        'text_secondary': '#94a3b8',
        'success': '#22c55e',
        'error': '#ef4444',
        'border': '#334155'
    },
    'spacing': {
        'xs': 8,
        'sm': 16,
        'md': 24,
        'lg': 32,
        'xl': 48
    },
    'fonts': {
        'heading': ('Segoe UI', 28, 'bold'),
        'subheading': ('Segoe UI', 16),
        'body': ('Segoe UI', 13),
        'small': ('Segoe UI', 11)
    }
}

def transform_timekeeper_name(name):
    parts = name.strip().split()
    if len(parts) >= 2:
        last_name = parts[-1]
        first_middle = ' '.join(parts[:-1])
        return f"{last_name}, {first_middle}"
    return name

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_tkdnd_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle
        base_path = sys._MEIPASS
        tkdnd_path = os.path.join(base_path, 'tkinterdnd2', 'tkdnd')
        os.environ['TKDND_LIBRARY'] = tkdnd_path

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEDES Name Switcher")
        self.root.geometry("800x800")
        self.root.configure(bg=DESIGN['colors']['background'])
        
        # Variables
        self.overwrite_original = BooleanVar(value=False)
        self.progress_var = tk.DoubleVar()
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style(theme="darkly")
        
        # Configure custom styles
        self.style.configure('Card.TFrame',
            background=DESIGN['colors']['surface'],
            borderwidth=1,
            relief='solid'
        )
        
        self.style.configure('Header.TLabel',
            font=DESIGN['fonts']['heading'],
            foreground=DESIGN['colors']['text'],
            background=DESIGN['colors']['surface']
        )
        
        self.style.configure('Subheader.TLabel',
            font=DESIGN['fonts']['subheading'],
            foreground=DESIGN['colors']['text_secondary'],
            background=DESIGN['colors']['surface']
        )
        
        self.style.configure('Modern.TButton',
            font=DESIGN['fonts']['body'],
            padding=10
        )
        
    def create_widgets(self):
        # Header
        header = ttk.Frame(self.root, style='Card.TFrame')
        header.pack(fill=X, padx=DESIGN['spacing']['lg'], 
                   pady=(DESIGN['spacing']['lg'], DESIGN['spacing']['md']))
        
        ttk.Label(
            header,
            text="MyCase LEDES Fixer",
            style='Header.TLabel'
        ).pack(pady=DESIGN['spacing']['sm'])
        
        ttk.Label(
            header,
            text="Transform TIMEKEEPER_NAME fields in LEDES files",
            style='Subheader.TLabel'
        ).pack(pady=(0, DESIGN['spacing']['sm']))
        
        # File List Card
        files_card = ttk.Frame(self.root, style='Card.TFrame')
        files_card.pack(fill=BOTH, expand=TRUE, padx=DESIGN['spacing']['lg'],
                       pady=DESIGN['spacing']['sm'])
        
        # File Listbox
        self.file_list = tk.Listbox(
            files_card,
            height=8,
            selectmode=EXTENDED,
            font=DESIGN['fonts']['body'],
            bg=DESIGN['colors']['surface'],
            fg=DESIGN['colors']['text'],
            selectbackground=DESIGN['colors']['primary'],
            selectforeground=DESIGN['colors']['text'],
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=DESIGN['colors']['border']
        )
        self.file_list.pack(fill=BOTH, expand=TRUE, padx=DESIGN['spacing']['sm'],
                           pady=DESIGN['spacing']['sm'])
        
        # Enable drag and drop
        self.file_list.drop_target_register(DND_FILES)
        self.file_list.dnd_bind('<<Drop>>', self.drop_files)
        
        # Buttons Frame
        btn_frame = ttk.Frame(files_card)
        btn_frame.pack(pady=DESIGN['spacing']['sm'])
        
        ttk.Button(
            btn_frame,
            text="Add Files",
            command=self.select_files,
            style='Modern.TButton'
        ).pack(side=LEFT, padx=DESIGN['spacing']['xs'])
        
        ttk.Button(
            btn_frame,
            text="Remove Selected",
            command=self.remove_selected_files,
            style='Modern.TButton'
        ).pack(side=LEFT, padx=DESIGN['spacing']['xs'])
        
        # Options Card
        options_card = ttk.Frame(self.root, style='Card.TFrame')
        options_card.pack(fill=X, padx=DESIGN['spacing']['lg'],
                         pady=DESIGN['spacing']['sm'])
        
        ttk.Checkbutton(
            options_card,
            text="Overwrite Original Files",
            variable=self.overwrite_original,
            style='Modern.TCheckbutton'
        ).pack(padx=DESIGN['spacing']['sm'], pady=DESIGN['spacing']['sm'])
        
        # Process Button and Progress
        process_card = ttk.Frame(self.root, style='Card.TFrame')
        process_card.pack(fill=X, padx=DESIGN['spacing']['lg'],
                         pady=DESIGN['spacing']['sm'])
        
        self.process_button = ttk.Button(
            process_card,
            text="Process Files",
            command=self.start_processing,
            style='Modern.TButton'
        )
        self.process_button.pack(pady=DESIGN['spacing']['sm'])
        
        self.progress_bar = ttk.Progressbar(
            process_card,
            variable=self.progress_var,
            maximum=100,
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=X, padx=DESIGN['spacing']['lg'])
        
        self.status_label = ttk.Label(
            process_card,
            text="No files selected",
            font=DESIGN['fonts']['small'],
            foreground=DESIGN['colors']['text_secondary']
        )
        self.status_label.pack(pady=DESIGN['spacing']['sm'])
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select LEDES Files",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        self.add_files(files)
        
    def add_files(self, files):
        for file in files:
            if file not in self.file_list.get(0, tk.END):
                self.file_list.insert(tk.END, file)
        self.update_status()
        
    def drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
        
    def remove_selected_files(self):
        selected = self.file_list.curselection()
        for idx in reversed(selected):
            self.file_list.delete(idx)
        self.update_status()
        
    def update_status(self):
        count = self.file_list.size()
        self.status_label.configure(text=f"{count} file(s) selected")
        
    def start_processing(self):
        files = self.file_list.get(0, tk.END)
        if not files:
            messagebox.showwarning("No Files", "Please select files to process.")
            return
            
        if self.overwrite_original.get():
            if not messagebox.askyesno("Confirm Overwrite",
                "This will overwrite the original files. Continue?"):
                return
            output_dir = None
        else:
            output_dir = filedialog.askdirectory(title="Select Output Directory")
            if not output_dir:
                return
                
        self.process_button.configure(state='disabled')
        threading.Thread(target=self.process_files,
                        args=(files, output_dir),
                        daemon=True).start()
        
    def process_files(self, files, output_dir):
        total = len(files)
        successful = 0
        
        for idx, file in enumerate(files):
            try:
                self.process_file(file, output_dir)
                successful += 1
            except Exception as e:
                logging.error(f"Error processing {file}: {e}")
                
            progress = ((idx + 1) / total) * 100
            self.progress_var.set(progress)
            self.status_label.configure(
                text=f"Processing {idx + 1} of {total}: {os.path.basename(file)}"
            )
            self.root.update_idletasks()
            
        self.progress_var.set(0)
        self.process_button.configure(state='normal')
        self.status_label.configure(
            text=f"Complete: {successful}/{total} files processed successfully"
        )
        messagebox.showinfo("Complete",
            f"Processed {successful}/{total} files successfully")
        
    def process_file(self, file_path, output_dir):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        header_idx = None
        timekeeper_idx = None
        
        for idx, line in enumerate(lines):
            if 'TIMEKEEPER_NAME' in line:
                header_idx = idx
                fields = line.strip().split('|')
                for field_name in ['TIMEKEEPER_NAME', 'TIMEKEEPER_NAME[]']:
                    try:
                        timekeeper_idx = fields.index(field_name)
                        break
                    except ValueError:
                        continue
                break
                
        if header_idx is None or timekeeper_idx is None:
            raise ValueError("TIMEKEEPER_NAME field not found")
            
        for i in range(header_idx + 1, len(lines)):
            if not lines[i].strip():
                continue
            fields = lines[i].strip().split('|')
            if len(fields) == len(lines[header_idx].strip().split('|')):
                fields[timekeeper_idx] = transform_timekeeper_name(
                    fields[timekeeper_idx]
                )
                lines[i] = '|'.join(fields) + '\n'
                
        if self.overwrite_original.get():
            output_path = file_path
        else:
            base = os.path.basename(file_path)
            name, ext = os.path.splitext(base)
            output_path = os.path.join(output_dir, f"{name}_corrected{ext}")
            
        with open(output_path, 'w') as f:
            f.writelines(lines)

if __name__ == '__main__':
    setup_tkdnd_path()
    root = TkinterDnD.Tk()
    app = ModernApp(root)
    root.mainloop()
        