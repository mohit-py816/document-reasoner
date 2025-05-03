import tkinter as tk
from tkinter import ttk, scrolledtext
from core.document_manager import DocumentManager
from core.llm.openai_manager import OpenAIManager
from core.llm.local_llm import LocalLLM
from core.vector_manager import VectorManager
from config.settings import VectorConfig

class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.document_manager = DocumentManager()
        self.vector_manager = VectorManager()
        self.llm = None
        self.current_model = None
        self.loading_label = ttk.Label(self, text="Processing...", foreground="gray")

        # Chat History
        self.chat_history = scrolledtext.ScrolledText(
            self, 
            state="disabled", 
            wrap=tk.WORD, 
            font=("Arial", 12)
        )
        self.chat_history.pack(fill="both", expand=True, padx=10, pady=10)

        # Input Area
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.user_input = ttk.Entry(input_frame, font=("Arial", 12))
        self.user_input.pack(side="left", fill="x", expand=True)

        send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_btn.pack(side="left", padx=5)

        back_btn = ttk.Button(input_frame, text="Back",
                             command=lambda: self.controller.show_page("UploadPage"))
        back_btn.pack(side="right", padx=5)

        # NEW: Document info display
        self.doc_info_label = ttk.Label(self, font=("Arial", 10), anchor="w")
        self.doc_info_label.pack(fill="x", padx=10, pady=5)

        # NEW: Model selection
        model_frame = tk.Frame(self)
        model_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(model_frame, text="Model:").pack(side="left")
        self.model_var = tk.StringVar()
        model_selector = ttk.Combobox(model_frame, 
                                    textvariable=self.model_var,
                                    values=["GPT-4", "Mistral-7B"],
                                    state="readonly")
        model_selector.pack(side="left", padx=5)
        model_selector.bind("<<ComboboxSelected>>", self.change_model)
        model_selector.current(0)

    def change_model(self, event):
        model_name = self.model_var.get()
        if model_name == "GPT-4":
            self.llm = OpenAIManager()
        elif model_name == "Mistral-7B":
            self.llm = LocalLLM()
        self.current_model = model_name

    def send_message(self):
        message = self.user_input.get()
        try:
            self.loading_label.pack()
            self.update_idletasks()

            if message.strip():
                self._display_message(f"You: {message}", "user")
                self.user_input.delete(0, tk.END)

                # NEW: Get document content for processing
                if self.controller.active_doc_id:
                    doc_content = self.document_manager.get_document_content(
                        self.controller.active_doc_id
                    )
                    # TODO: Add actual AI processing with doc_content
                    ai_response = f"AI: [Mock Response] I have read {len(doc_content)} characters"
                    self._display_message(ai_response, "ai")

            if self.controller.active_doc_id and self.llm:
                # NEW: Retrieve relevant context
                query_embedding = self.vector_manager.generate_embeddings([message])[0]
                search_results = self.vector_manager.client.search(
                    collection_name=VectorConfig.COLLECTION_NAME,
                    query_vector=query_embedding,
                    limit=3,
                    with_payload=True
                )
                context = "\n".join([result.payload["chunk_text"] 
                                   for result in search_results])

                # Get chat history
                chat_history = self._get_chat_history()

                # Generate response
                ai_response = self.llm.generate(context, message, chat_history)
                self._display_message(f"AI ({self.current_model}): {ai_response}", "ai")

        finally:
            self.loading_label.pack_forget()

    def _get_chat_history(self):
        """Extract chat history in LLM format"""
        history = []
        text = self.chat_history.get("1.0", tk.END)
        for line in text.split("\n"):
            if line.startswith("You:"):
                history.append({"role": "user", "content": line[4:]})
            elif line.startswith("AI ("):
                history.append({"role": "assistant", "content": line.split("): ")[1]})
        return history

    def _display_message(self, text, sender):
        tag_config = {
            "user": {"foreground": "blue"},
            "ai": {"foreground": "green"}
        }
        self.chat_history.configure(state="normal")
        self.chat_history.insert(tk.END, f"{text}\n\n")
        self.chat_history.tag_configure(sender, **tag_config[sender])
        self.chat_history.tag_add(sender, "end-2l linestart", "end-1c")
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)

        # Create custom tags
        self.chat_history.tag_configure("user_bubble", 
                                       background="#e3f2fd",
                                       relief="solid",
                                       borderwidth=1,
                                       spacing3=5)
        self.chat_history.tag_configure("ai_bubble", 
                                       background="#f5f5f5",
                                       relief="solid",
                                       borderwidth=1)

        # Insert message with appropriate tags
        self.chat_history.insert(tk.END, f"{text}\n", 
                                ("user_bubble" if sender == "user" else "ai_bubble"))
        self.chat_history.configure(state="disabled")
        self.chat_history.see(tk.END)


    # NEW: Update document info when page is shown
    def on_page_show(self):
        if self.controller.active_doc_id:
            doc_data = self.document_manager.loaded_documents.get(
                self.controller.active_doc_id, {}
            )
            self.doc_info_label.config(
                text=f"Active Document: {doc_data.get('meta', {}).get('filename', 'Unknown')}"
            )
        else:
            self.doc_info_label.config(text="No active document selected")
