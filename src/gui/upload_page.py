import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from pathlib import Path
from core.document_manager import DocumentManager

class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.document_manager = DocumentManager()
        self.current_doc_id = None

        # Background Image
        self.bg_image = ImageTk.PhotoImage(Image.open("assets/default_bg.jpg"))
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Upload Widgets
        upload_frame = tk.Frame(self, bg="white", bd=2, relief="ridge")
        upload_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(upload_frame, text="Drag & Drop Files or", font=("Arial", 14)).pack(pady=10)
        upload_btn = ttk.Button(upload_frame, text="Browse Files", command=self.handle_upload)
        upload_btn.pack(pady=10, padx=20)

        self.file_list = tk.Listbox(upload_frame, width=50, height=10)
        self.file_list.pack(pady=10)

        # NEW: Process button instead of direct navigation
        process_btn = ttk.Button(upload_frame, 
                               text="Process Selected",
                               command=self.process_files)
        process_btn.pack(pady=10)

        # Navigation now happens after processing
        nav_btn = ttk.Button(upload_frame, 
                            text="Go to Chat",
                            command=lambda: controller.show_page("ChatPage"))
        nav_btn.pack(pady=10)

    def handle_upload(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Documents", "*.pdf *.docx *.xml *.yml")]
        )
        for f in files:
            self.file_list.insert(tk.END, f)

    # NEW: File processing method
    def process_files(self):
        selected_files = self.file_list.get(0, tk.END)
        if not selected_files:
            messagebox.showwarning("No Files", "Please select files first")
            return

        # Process first file (we'll handle multiple files later)
        first_file = selected_files[0]
        self.current_doc_id = self.document_manager.add_document(first_file)

        if self.current_doc_id:
            # Store active document in controller
            self.controller.active_doc_id = self.current_doc_id
            messagebox.showinfo("Success", "Document processed successfully!\nYou can now chat with the document.")
        else:
            messagebox.showerror("Error", "Failed to process document")

    def on_page_show(self):
        self.file_list.delete(0, tk.END)
        self.current_doc_id = None  # Reset on return to upload page
