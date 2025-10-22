"""
GUI version of createCustomIni - Creates a fallout76Custom.ini file from installed mods
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import subprocess
from tkinterdnd2 import DND_FILES, TkinterDnD

# Import the core logic from the original script
FILENAME = "Fallout76Custom.ini"


def find_fallout76_directory():
    """Find the Fallout 76 directory by checking multiple possible locations."""
    user_home = os.path.expanduser("~")
    
    possible_paths = [
        os.path.join(user_home, "OneDrive", "Documents", "My Games", "Fallout 76"),
        os.path.join(user_home, "Documents", "My Games", "Fallout 76"),
        os.path.join(user_home, "OneDrive - Personal", "Documents", "My Games", "Fallout 76"),
        os.path.join(user_home, "OneDrive", "My Games", "Fallout 76"),
        os.path.join(user_home, "OneDrive - Business", "Documents", "My Games", "Fallout 76"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return os.path.join(user_home, "Documents", "My Games", "Fallout 76")


RESOURCE_MAP = [
    {
        "filename": "sResourceStartUpArchiveList",
        "mods": [
            "BakaFile - Main.ba2",
            "IconTag.ba2",
            "IconSortingRatmonkeys.ba2",
            "MMM - Country Roads.ba2",
            "ImpUlt.ba2",
            "Quizzless Apalachia.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceArchiveList2",
        "mods": [
            "PerkLoadoutManager.ba2",
            "IUMesh.ba2",
            "MoreWhereThatCameFrom.ba2",
            "Prismatic_Lasers_76_Lightblue.ba2",
            "OptimizedSonar.ba2",
            "Silentchameleon.ba2",
            "CleanPip.ba2",
            "classicFOmus_76.ba2",
            "nootnoot.ba2",
            "MenuMusicReplacer.ba2",
            "BullBarrel.ba2",
            "EVB76NevernudeFemale - Meshes.ba2",
            "EVB76NevernudeFemale - Textures.ba2",
            "EVB76NevernudeMale - Meshes.ba2",
            "EVB76NevernudeMale - Textures.ba2",
            "EVB76 - Meshes.ba2",
            "EVB76 - Textures.ba2",
            "EVB76Nevernude - Meshes.ba2",
            "EVB76Nevernude - Textures.ba2",
            "BoxerShorts.ba2",
            "MaleUnderwear.ba2",
            "FemaleUnderwear.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceIndexFileList",
        "mods": [
            "UHDmap.ba2",
            "EnhancedBlood - Textures.ba2",
            "EnhancedBlood - Meshes.ba2",
            "MapMarkers.ba2",
            "Radiant_Clouds.ba2",
            "SpoilerFreeMap.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
    {
        "filename": "sResourceArchive2List",
        "mods": [
            "PerkLoadoutManager.ba2",
            "ChatMod.ba2",
            "ShowHealthReRedux.ba2",
            "ShowHealth.ba2",
            "CompatibleShowHealthRedux.ba2",
        ],
        "default_mods": [],
        "found_mods": [],
    },
]

SR_2LIST_INDEX = 3
MOD_TO_PLACE_LAST = "HUDModLoader.ba2"
SETTINGS_FILE = "createCustomIni_settings.json"


class CreateCustomIniGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fallout 76 Custom INI Creator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.data_folder = tk.StringVar(value=".")
        self.ini_folder = tk.StringVar(value=find_fallout76_directory())
        self.ini_filename = tk.StringVar(value=FILENAME)
        self.import_ini = tk.StringVar(value="")
        self.dark_mode = tk.BooleanVar(value=False)
        self.mod_count = tk.StringVar(value="Mods found: 0")
        self.last_created_path = None
        
        # Load saved settings
        self.load_settings()
        
        # Setup drag and drop
        self.setup_drag_drop()
        
        # Trace variables for validation
        self.data_folder.trace_add('write', self.validate_paths)
        self.ini_folder.trace_add('write', self.validate_paths)
        
        self.create_widgets()
        self.apply_theme()
        self.validate_paths()
        
    def create_widgets(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Top toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(toolbar, text="Dark Mode", variable=self.dark_mode, 
                       command=self.apply_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        
        # Data Folder with validation indicator
        row = 1
        ttk.Label(main_frame, text="Data Folder:").grid(row=row, column=0, sticky=tk.W, pady=5)
        data_frame = ttk.Frame(main_frame)
        data_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        data_frame.columnconfigure(0, weight=1)
        self.data_entry = ttk.Entry(data_frame, textvariable=self.data_folder)
        self.data_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.data_status = ttk.Label(data_frame, text="", width=3)
        self.data_status.grid(row=0, column=1, padx=(5, 0))
        ttk.Button(main_frame, text="Browse", command=self.browse_data_folder).grid(row=row, column=2, padx=5)
        
        # INI Folder with validation indicator
        row += 1
        ttk.Label(main_frame, text="INI Folder:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ini_frame = ttk.Frame(main_frame)
        ini_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ini_frame.columnconfigure(0, weight=1)
        self.ini_entry = ttk.Entry(ini_frame, textvariable=self.ini_folder)
        self.ini_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.ini_status = ttk.Label(ini_frame, text="", width=3)
        self.ini_status.grid(row=0, column=1, padx=(5, 0))
        ttk.Button(main_frame, text="Browse", command=self.browse_ini_folder).grid(row=row, column=2, padx=5)
        
        # INI Filename
        row += 1
        ttk.Label(main_frame, text="INI Filename:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.ini_filename).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Import INI (optional)
        row += 1
        ttk.Label(main_frame, text="Import INI (optional):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.import_ini).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_import_ini).grid(row=row, column=2, padx=5)
        
        # Mod count display
        row += 1
        ttk.Label(main_frame, textvariable=self.mod_count, font=('TkDefaultFont', 10, 'bold')).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Scan Mods", command=self.scan_mods).grid(row=row, column=2, padx=5)
        
        # Separator
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Notebook for tabs
        row += 1
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Tab 1: Mod Preview
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="Mod Preview")
        
        self.mod_tree = ttk.Treeview(preview_frame, columns=('Count',), height=12)
        self.mod_tree.heading('#0', text='Section / Mod Name')
        self.mod_tree.heading('Count', text='Count')
        self.mod_tree.column('Count', width=80)
        
        tree_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.mod_tree.yview)
        self.mod_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.mod_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tab 2: Output Log
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="Output Log")
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=70, state='disabled')
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        row += 1
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        self.create_btn = ttk.Button(button_frame, text="Create Custom INI", command=self.create_ini)
        self.create_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_folder_btn = ttk.Button(button_frame, text="Open Output Folder", 
                                         command=self.open_output_folder, state='disabled')
        self.open_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure row weight for notebook
        main_frame.rowconfigure(row - 1, weight=1)
        
    def setup_drag_drop(self):
        """Setup drag and drop for folder entries"""
        try:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except:
            # tkinterdnd2 not available, drag and drop disabled
            pass
    
    def on_drop(self, event):
        """Handle drag and drop events"""
        path = event.data.strip('{}')
        if os.path.isdir(path):
            # Determine which field to update based on cursor position
            widget = event.widget.winfo_containing(event.x_root, event.y_root)
            if widget == self.data_entry:
                self.data_folder.set(path)
            elif widget == self.ini_entry:
                self.ini_folder.set(path)
    
    def validate_paths(self, *args):
        """Validate folder paths and show visual feedback"""
        # Validate data folder
        data_path = self.data_folder.get()
        if os.path.exists(data_path) and os.path.isdir(data_path):
            self.data_status.config(text="✓", foreground="green")
        else:
            self.data_status.config(text="✗", foreground="red")
        
        # Validate ini folder (can be created, so just check parent)
        ini_path = self.ini_folder.get()
        if ini_path and (os.path.exists(ini_path) or os.path.exists(os.path.dirname(ini_path))):
            self.ini_status.config(text="✓", foreground="green")
        else:
            self.ini_status.config(text="✗", foreground="red")
    
    def load_settings(self):
        """Load saved settings from file"""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.data_folder.set(settings.get('data_folder', '.'))
                    self.ini_folder.set(settings.get('ini_folder', find_fallout76_directory()))
                    self.ini_filename.set(settings.get('ini_filename', FILENAME))
                    self.import_ini.set(settings.get('import_ini', ''))
                    self.dark_mode.set(settings.get('dark_mode', False))
        except Exception as e:
            print(f"Could not load settings: {e}")
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'data_folder': self.data_folder.get(),
                'ini_folder': self.ini_folder.get(),
                'ini_filename': self.ini_filename.get(),
                'import_ini': self.import_ini.get(),
                'dark_mode': self.dark_mode.get()
            }
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {e}")
    
    def apply_theme(self):
        """Apply dark or light theme"""
        style = ttk.Style()
        
        if self.dark_mode.get():
            # Dark mode colors
            bg_color = '#2b2b2b'
            fg_color = '#ffffff'
            text_bg = '#1e1e1e'
            text_fg = '#d4d4d4'
            
            self.root.configure(bg=bg_color)
            style.theme_use('clam')
            
            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TButton', background='#404040', foreground=fg_color)
            style.configure('TCheckbutton', background=bg_color, foreground=fg_color)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background='#404040', foreground=fg_color)
            style.configure('Treeview', background=text_bg, foreground=text_fg, fieldbackground=text_bg)
            
            self.output_text.configure(bg=text_bg, fg=text_fg, insertbackground=text_fg)
        else:
            # Light mode (default)
            style.theme_use('vista' if sys.platform == 'win32' else 'default')
            style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
            
            self.output_text.configure(bg='white', fg='black', insertbackground='black')
    
    def scan_mods(self):
        """Scan for mods and update preview"""
        thread = threading.Thread(target=self._scan_mods_thread, daemon=True)
        thread.start()
    
    def _scan_mods_thread(self):
        """Thread worker for scanning mods"""
        try:
            mods_dir = self.data_folder.get()
            
            if not os.path.exists(mods_dir):
                self.mod_count.set("Mods found: 0 (Invalid path)")
                return
            
            # Reset found_mods
            for resource in RESOURCE_MAP:
                resource["found_mods"] = []
            
            total_mods = 0
            
            # Scan for mods
            for _, _, filenames in os.walk(mods_dir):
                for file in filenames:
                    if not file.startswith("SeventySix") and file.lower().endswith(".ba2"):
                        total_mods += 1
                        found = False
                        for resource in RESOURCE_MAP:
                            if file in resource["mods"]:
                                resource["found_mods"].append(file)
                                found = True
                                break
                        if not found:
                            RESOURCE_MAP[SR_2LIST_INDEX]["found_mods"].append(file)
                break
            
            self.mod_count.set(f"Mods found: {total_mods}")
            self.update_mod_tree()
            
        except Exception as e:
            self.mod_count.set(f"Error scanning: {e}")
    
    def update_mod_tree(self):
        """Update the mod tree view with found mods"""
        # Clear existing items
        for item in self.mod_tree.get_children():
            self.mod_tree.delete(item)
        
        # Add sections and mods
        for resource in RESOURCE_MAP:
            if resource["found_mods"]:
                section_name = resource["filename"]
                count = len(resource["found_mods"])
                parent = self.mod_tree.insert('', 'end', text=section_name, values=(count,), open=True)
                
                # Sort mods for display
                sorted_mods = sorted(resource["found_mods"])
                for mod in sorted_mods:
                    self.mod_tree.insert(parent, 'end', text=f"  {mod}", values=('',))
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        if self.last_created_path:
            folder = os.path.dirname(self.last_created_path)
            if os.path.exists(folder):
                if sys.platform == 'win32':
                    os.startfile(folder)
                elif sys.platform == 'darwin':
                    subprocess.run(['open', folder])
                else:
                    subprocess.run(['xdg-open', folder])
    
    def browse_data_folder(self):
        folder = filedialog.askdirectory(title="Select Fallout 76 Data Folder", 
                                        initialdir=self.data_folder.get())
        if folder:
            self.data_folder.set(folder)
            
    def browse_ini_folder(self):
        folder = filedialog.askdirectory(title="Select INI Output Folder",
                                        initialdir=self.ini_folder.get())
        if folder:
            self.ini_folder.set(folder)
            
    def browse_import_ini(self):
        file = filedialog.askopenfilename(title="Select INI File to Import", 
                                         filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")])
        if file:
            self.import_ini.set(file)
            
    def log(self, message):
        """Add message to output log"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        self.root.update_idletasks()
        
    def create_ini(self):
        """Create the custom INI file"""
        # Run in a separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._create_ini_thread, daemon=True)
        thread.start()
        
    def _create_ini_thread(self):
        """Thread worker for creating INI file"""
        try:
            # Disable button during processing
            self.create_btn.config(state='disabled')
            
            # Clear output
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state='disabled')
            
            mods_dir = self.data_folder.get()
            ini_folder = self.ini_folder.get()
            filename = self.ini_filename.get()
            import_ini_path = self.import_ini.get()
            
            ini_file_path = os.path.join(ini_folder, filename)
            
            # Validate data folder
            if not os.path.exists(mods_dir):
                self.log(f"Error: Data folder '{mods_dir}' does not exist!")
                messagebox.showerror("Error", f"Data folder '{mods_dir}' does not exist!")
                return
                
            # Create output folder if needed
            os.makedirs(os.path.dirname(ini_file_path), exist_ok=True)
            
            self.log(f"Scanning for mods in: {mods_dir}")
            self.log(f"Creating ini file at: {ini_file_path}")
            
            # Reset found_mods for each resource
            for resource in RESOURCE_MAP:
                resource["found_mods"] = []
            
            # Scan for mods
            for _, _, filenames in os.walk(mods_dir):
                for file in filenames:
                    if not file.startswith("SeventySix") and file.lower().endswith(".ba2"):
                        found = False
                        for resource in RESOURCE_MAP:
                            if file in resource["mods"]:
                                resource["found_mods"].append(file)
                                found = True
                                break
                        if not found:
                            RESOURCE_MAP[SR_2LIST_INDEX]["found_mods"].append(file)
                break
            
            # Write INI file
            with open(ini_file_path, "w+", encoding="utf-8") as custom_ini_file:
                custom_ini_file.write("[Archive]\r\n")
                
                for resource in RESOURCE_MAP:
                    if resource["found_mods"]:
                        found_mods = set(resource["found_mods"])
                        mods = resource["mods"]
                        mod_list = ", ".join(mod for mod in mods if mod in found_mods)
                        
                        diff_list = [item for item in found_mods if item not in mods]
                        if diff_list:
                            diff_list.sort()
                            
                            if MOD_TO_PLACE_LAST in diff_list:
                                diff_list.remove(MOD_TO_PLACE_LAST)
                                diff_list.append(MOD_TO_PLACE_LAST)
                            
                            diff_list = ", " + ", ".join(diff_list)
                        else:
                            diff_list = ""
                        
                        default_mods = ", ".join(resource["default_mods"])
                        line_content = "{}{}".format(default_mods, mod_list + diff_list)
                        
                        if line_content.startswith(", "):
                            line_content = line_content[2:]
                        
                        custom_ini_file.write(f"{resource['filename']} = {line_content}\r\n")
                        self.log(f"Added {len(found_mods)} mods to {resource['filename']}")
                
                # Import additional INI contents
                if import_ini_path and os.path.exists(import_ini_path):
                    with open(import_ini_path, "r", encoding="utf-8") as import_file:
                        custom_ini_file.write(import_file.read())
                    self.log(f"Imported contents from: {import_ini_path}")
                elif import_ini_path:
                    self.log(f"Warning: Import file '{import_ini_path}' not found!")
            
            self.log(f"\nSuccessfully created {ini_file_path}")
            self.last_created_path = ini_file_path
            self.open_folder_btn.config(state='normal')
            
            # Switch to output log tab
            self.notebook.select(1)
            
            messagebox.showinfo("Success", f"Successfully created {ini_file_path}")
            
        except PermissionError:
            error_msg = f"Permission denied writing to '{ini_file_path}'. Try running as administrator."
            self.log(f"Error: {error_msg}")
            messagebox.showerror("Permission Error", error_msg)
        except Exception as e:
            error_msg = f"Error creating ini file: {e}"
            self.log(f"Error: {error_msg}")
            messagebox.showerror("Error", error_msg)
        finally:
            # Re-enable button
            self.create_btn.config(state='normal')


def main():
    try:
        # Try to use TkinterDnD for drag and drop support
        root = TkinterDnD.Tk()
    except:
        # Fall back to regular Tk if TkinterDnD is not available
        root = tk.Tk()
    
    app = CreateCustomIniGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
