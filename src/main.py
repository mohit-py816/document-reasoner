import logging
import tkinter as tk
import json
from tkinter import messagebox, filedialog
from gui.upload_page import UploadPage
from gui.chat_page import ChatPage
from gui.history_panel import HistoryPanel
from core.file_manager import FileManager
from core.llm.local_llm import LocalLLM
from core.llm.openai_manager import OpenAIManager
from config.settings import LLMConfig

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DocumentReasoner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Document Reasoner")
        self.geometry("1200x800")
        self.file_manager = FileManager()
        self.llm_manager = None
        self.active_doc_id = None
        self.current_chat = []

        self._init_llm()
        self._bind_shortcuts()

        # Container for all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (UploadPage, ChatPage, HistoryPanel):
            page_name = PageClass.__name__
            page = PageClass(parent=container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("UploadPage")
        self.active_doc_id = None	#Track Current document

    def _init_llm(self):
        """Initialize default LLM based on config"""
        try:
            self.llm_manager = OpenAIManager() if LLMConfig.OPENAI_API_KEY else LocalLLM()
        except Exception as e:
            tk.messagebox.showerror("LLM Error", f"Failed to initialize AI engine: {str(e)}")

    def _bind_shortcuts(self):
        self.bind("<Control-s>", self.save_chat)
        self.bind("<Control-o>", self.load_chat)

    def save_chat(self, event=None):
        if not self.active_doc_id or not self.current_chat:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump({
                        "document_id": self.active_doc_id,
                        "chat_history": self.current_chat
                    }, f, indent=2)
                messagebox.showinfo("Success", "Chat saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save chat: {str(e)}")

    def load_chat(self, event=None):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.active_doc_id = data.get("document_id")
                    self.current_chat = data.get("chat_history", [])

                    # Update chat display
                    self.pages["ChatPage"].chat_history.configure(state="normal")
                    self.pages["ChatPage"].chat_history.delete("1.0", tk.END)
                    for msg in self.current_chat:
                        self.pages["ChatPage"]._display_message(msg["content"], msg["role"])
                    messagebox.showinfo("Success", "Chat loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load chat: {str(e)}")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
        page.on_page_show()  # Initialize page content

    # Add to DocumentReasoner class:
    def toggle_history(self):
        current_x = self.history_panel.winfo_x()
        if current_x < 0:
            self.animate_panel(0)
        else:
            self.animate_panel(-300)

    def animate_panel(self, target_x):
        current_x = self.history_panel.winfo_x()
        move_by = 10 if target_x > current_x else -10
        if (move_by > 0 and current_x < target_x) or (move_by < 0 and current_x > target_x):
            self.history_panel.place(x=current_x + move_by, y=0, relheight=1)
            self.after(10, lambda: self.animate_panel(target_x))


if __name__ == "__main__":
    app = DocumentReasoner()
    app.mainloop()
