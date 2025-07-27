import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys

class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")
        self.root.geometry("500x300")
        self.root.resizable(True, True)
        
        # Selected folder path
        self.selected_folder = ""
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="File Renamer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Choose folder section
        folder_label = ttk.Label(main_frame, text="Selected Folder:")
        folder_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.folder_display = ttk.Label(main_frame, text="No folder selected", 
                                       foreground="gray", wraplength=350)
        self.folder_display.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        choose_folder_btn = ttk.Button(main_frame, text="Choose Folder", 
                                      command=self.choose_folder)
        choose_folder_btn.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Add text section
        text_label = ttk.Label(main_frame, text="Text to add to front of filenames:")
        text_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_entry = ttk.Entry(main_frame, width=40)
        self.text_entry.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        add_text_btn = ttk.Button(main_frame, text="Add Text to Filenames", 
                                 command=self.add_text_to_files)
        add_text_btn.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
        # Status/Results area
        self.result_text = tk.Text(main_frame, height=8, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        scrollbar.grid(row=7, column=2, sticky=(tk.N, tk.S))
        
        main_frame.rowconfigure(7, weight=1)
        
    def choose_folder(self):
        """Open folder selection dialog"""
        folder_path = filedialog.askdirectory(title="Select folder containing files to rename")
        
        if folder_path:
            self.selected_folder = folder_path
            self.folder_display.config(text=folder_path, foreground="black")
            
            # Show files in the folder
            try:
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Found {len(files)} files in selected folder:\n\n")
                for file in files:
                    self.result_text.insert(tk.END, f"• {file}\n")
            except Exception as e:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, f"Error reading folder: {str(e)}")
    
    def add_text_to_files(self):
        """Add text to the beginning of all filenames in the selected folder"""
        if not self.selected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return
        
        prefix_text = self.text_entry.get().strip()
        if not prefix_text:
            messagebox.showerror("Error", "Please enter text to add to filenames!")
            return
        
        try:
            files = [f for f in os.listdir(self.selected_folder) 
                    if os.path.isfile(os.path.join(self.selected_folder, f))]
            
            if not files:
                messagebox.showinfo("Info", "No files found in the selected folder!")
                return
            
            # Confirm the operation
            result = messagebox.askyesno("Confirm", 
                                       f"Are you sure you want to add '{prefix_text}' to the beginning of {len(files)} filenames?")
            if not result:
                return
            
            renamed_count = 0
            errors = []
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Renaming files with prefix '{prefix_text}'...\n\n")
            
            for filename in files:
                try:
                    old_path = os.path.join(self.selected_folder, filename)
                    new_filename = prefix_text + filename
                    new_path = os.path.join(self.selected_folder, new_filename)
                    
                    # Check if new filename already exists
                    if os.path.exists(new_path):
                        errors.append(f"File '{new_filename}' already exists - skipping '{filename}'")
                        continue
                    
                    os.rename(old_path, new_path)
                    renamed_count += 1
                    self.result_text.insert(tk.END, f"✓ {filename} → {new_filename}\n")
                    
                except Exception as e:
                    errors.append(f"Error renaming '{filename}': {str(e)}")
            
            # Show summary
            self.result_text.insert(tk.END, f"\n--- Summary ---\n")
            self.result_text.insert(tk.END, f"Successfully renamed: {renamed_count} files\n")
            
            if errors:
                self.result_text.insert(tk.END, f"Errors: {len(errors)}\n\n")
                for error in errors:
                    self.result_text.insert(tk.END, f"⚠ {error}\n")
            
            messagebox.showinfo("Complete", 
                              f"Operation completed!\nRenamed: {renamed_count} files\nErrors: {len(errors)}")
                              
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()