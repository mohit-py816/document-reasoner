import tkinter as tk

class HistoryPanel(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")

        # Header
        header = tk.Frame(self, bg="#2c3e50")
        tk.Label(header, text="Chat History", fg="white", bg="#2c3e50",
                font=("Arial", 12, "bold")).pack(pady=10)
        header.pack(fill="x")

        # History List
        self.history_list = tk.Listbox(
            self,
            bg="white",
            relief="flat",
            font=("Arial", 11),
            selectbackground="#3498db"
        )
        self.history_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Sample Data (Replace with actual data later)
        for i in range(1, 21):
            self.history_list.insert(tk.END, f"Document {i} - Last chat: 2024-03-15")
