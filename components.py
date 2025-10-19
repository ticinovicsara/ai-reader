import customtkinter as ctk
import threading

def show_summary_modal(master, summary_text, on_qa_callback=None):
    modal = ctk.CTkToplevel(master)
    modal.title("Document Summary")
    modal.geometry("500x400")
    modal.grab_set()

    ctk.CTkLabel(modal, text=summary_text, wraplength=450, justify="left").pack(padx=20, pady=20)

    frame = ctk.CTkFrame(modal)
    frame.pack(pady=10)

    if on_qa_callback:
        ctk.CTkButton(frame, text="Ask Questions", command=lambda: [modal.destroy(), on_qa_callback()]).pack(side="left", padx=5)
    ctk.CTkButton(frame, text="Close", command=modal.destroy).pack(side="left", padx=5)


def show_qa_modal(master, document_text):
    modal = ctk.CTkToplevel(master)
    modal.title("Chat About Document")
    modal.geometry("500x450")
    modal.grab_set()

    chat = ctk.CTkTextbox(modal, width=480, height=300, state="disabled")
    chat.pack(padx=10, pady=10)

    frame = ctk.CTkFrame(modal)
    frame.pack(fill="x", padx=10, pady=10)

    entry = ctk.CTkEntry(frame, width=380)
    entry.pack(side="left", padx=(0, 5))

    def update_chat(text):
        chat.configure(state="normal")
        chat.insert("end", text + "\n\n")
        chat.configure(state="disabled")
        chat.see("end")

    def ask():
        from ai_utils import ask_question
        q = entry.get().strip()
        if not q:
            return
        entry.delete(0, "end")
        update_chat(f"You: {q}")

        thinking_index = chat.index("end-1c")
        update_chat("AI: Thinking...")

        def worker():
            try:
                a = ask_question(document_text, q)

                def replace_thinking():
                    chat.configure(state="normal")
                    chat.delete(thinking_index, "end")
                    chat.insert("end", f"A: {a}\n\n")
                    chat.configure(state="disabled")
                    chat.see("end")

                modal.after(0, lambda: update_chat(f"A: {a}"))
            except Exception as e:
                modal.after(0, lambda: update_chat(f"Error: {e}"))

        threading.Thread(target=worker, daemon=True).start()

    ctk.CTkButton(frame, text="Send", command=ask, width=80).pack(side="left")
    entry.bind("<Return>", lambda e: ask())
