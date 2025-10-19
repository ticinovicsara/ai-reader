import customtkinter as ctk
from file_reader import read_file
from components import show_qa_modal, show_summary_modal
from ai_utils import summarize, ask_question
from tkinter import messagebox, filedialog
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AI Reader")
app.geometry("600x400")

current_document_text = ""
loading_label = None

def show_loading(message):
    global loading_label
    if loading_label:
        loading_label.configure(text=message)
    else:
        loading_label = ctk.CTkLabel(app, text=message, font=("Arial", 14))
        loading_label.pack(pady=10)

def hide_loading():
    global loading_label
    if loading_label:
        loading_label.destroy()
        loading_label = None

def open_file():
    global current_document_text
    file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx *.txt")])
    if not file_path:
        return

    load_button.configure(state="disabled")
    qa_button.configure(state="disabled")
    show_loading("📖 Reading document...")

    def worker():
        global current_document_text
        try:
            current_document_text = read_file(file_path)
            app.after(0, lambda: show_loading("🤖 Summarizing... (may take 30–60s)"))
            summary = summarize(current_document_text)

            app.after(0, hide_loading)
            app.after(0, lambda: show_summary_modal(app, summary, on_qa_click))
        except Exception as e:
            app.after(0, hide_loading)
            app.after(0, lambda: messagebox.showerror("Error", str(e)))

    threading.Thread(target=worker, daemon=True).start()

def on_qa_click():
    if current_document_text:
        show_qa_modal(app, current_document_text)
    else:
        messagebox.showwarning("No Document", "Please load a document first.")

load_button = ctk.CTkButton(app, text="📂 Load Document", command=open_file, width=200, height=40)
load_button.pack(pady=50)

qa_button = ctk.CTkButton(app, text="💬 Ask Questions", command=on_qa_click, width=200, height=40)
qa_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="Ready", font=("Arial", 10), text_color="gray")
status_label.pack(side="bottom", pady=10)

app.mainloop()
