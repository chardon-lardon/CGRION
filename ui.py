"""Première interface de CGRION, construite avec Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from assistant import respond
from config import APP_NAME
from memory import load_history, new_session, clear_history


class ChatWindow:
    """Regroupe les éléments de la fenêtre et leurs actions."""

    def __init__(self, root):
        self.root = root
        self.history_windows = []
        root.title(APP_NAME)
        root.geometry("760x560")
        root.minsize(520, 400)
        root.configure(bg="#f3f5f8")

        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Send.TButton", font=("Segoe UI", 11, "bold"),
                        foreground="white", background="#2458a6", padding=(18, 10))
        style.map("Send.TButton", background=[("active", "#1c4480")])

        # Le cadre organise la page avec des marges autour du contenu.
        frame = tk.Frame(root, bg="#f3f5f8", padx=24, pady=24)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(2, weight=1)

        tk.Label(frame, text=APP_NAME, font=("Segoe UI", 24, "bold"),
                 bg="#f3f5f8", fg="#17253b").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text="Assistant local · modèle IA non connecté",
                 font=("Segoe UI", 10), bg="#f3f5f8", fg="#526176").grid(
                     row=1, column=0, sticky="w", pady=(4, 18))

        # La conversation peut défiler, mais ne peut pas être modifiée à la main.
        self.conversation = ScrolledText(
            frame, wrap="word", font=("Segoe UI", 11), bg="white",
            fg="#17253b", relief="flat", padx=16, pady=16, state="disabled")
        self.conversation.grid(row=2, column=0, sticky="nsew")
        self.conversation.tag_configure("speaker", font=("Segoe UI", 11, "bold"))

        tk.Label(frame, text="Ta demande", font=("Segoe UI", 10),
                 bg="#f3f5f8", fg="#17253b").grid(
                     row=3, column=0, sticky="w", pady=(18, 6))
        composer = tk.Frame(frame, bg="#f3f5f8")
        composer.grid(row=4, column=0, sticky="ew")
        composer.columnconfigure(0, weight=1)
        self.request = ttk.Entry(composer, font=("Segoe UI", 11))
        self.request.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.request.bind("<Return>", self.send_message)
        ttk.Button(composer, text="Envoyer", style="Send.TButton",
                   command=self.send_message).grid(row=0, column=1)
        toolbar = tk.Frame(frame, bg="#f3f5f8")
        toolbar.grid(row=5, column=0, sticky="w", pady=(12, 0))
        for title, action in (("Effacer", self.clear_conversation),
                              ("Historique", self.show_history),
                              ("Nouvelle conversation", self.new_conversation)):
            ttk.Button(toolbar, text=title, command=action).pack(side="left", padx=(0, 8))
        tk.Label(frame, text="Effacer vide l'écran. Les échanges restent dans l'historique.",
                 bg="#f3f5f8", fg="#526176", font=("Segoe UI", 9)).grid(
                     row=6, column=0, sticky="w", pady=(8, 0))
        ttk.Button(
            frame, text="Épurer l’historique", command=self.purge_history,
        ).grid(row=7, column=0, sticky="w", pady=(12, 0))
        self.welcome()
        self.request.focus_set()

    def welcome(self):
        self.append_message(APP_NAME, "Bienvenue ! Écris ta demande puis clique sur Envoyer. "
                            "Le modèle IA n'est pas encore connecté.")

    def clear_conversation(self):
        """Vide l'écran uniquement, sans toucher au fichier d'historique."""
        self.conversation.configure(state="normal")
        self.conversation.delete("1.0", "end")
        self.conversation.configure(state="disabled")
        self.request.delete(0, "end")
        self.request.focus_set()

    def new_conversation(self):
        new_session()
        self.clear_conversation()
        self.welcome()

    def show_history(self):
        """Ouvre une fenêtre de consultation des échanges enregistrés."""
        try:
            items = load_history()
        except (OSError, ValueError) as error:
            messagebox.showerror("Historique inaccessible", str(error), parent=self.root)
            return
        window = tk.Toplevel(self.root)
        self.history_windows.append(window)
        window.title("CGRION — Historique")
        window.geometry("680x480")
        window.minsize(400, 300)
        view = ScrolledText(window, wrap="word", font=("Segoe UI", 11), padx=16, pady=16)
        view.pack(fill="both", expand=True, padx=16, pady=16)
        if not items:
            view.insert("end", "Aucun échange enregistré pour le moment.")
        previous_session = None
        for item in items:
            if item["session"] != previous_session:
                view.insert("end", "— Conversation —\n")
                previous_session = item["session"]
            view.insert("end", f"{item['date']}\nToi : {item['message']}\n"
                        f"CGRION : {item['response']}\n\n")
        view.configure(state="disabled")
        view.see("end")

    def purge_history(self):
        """Demande confirmation avant de supprimer l'historique."""
        confirmed = messagebox.askyesno(
            title="Épurer l’historique",
            message="Voulez-vous supprimer définitivement tous les échanges de l’historique ?",
            detail="La conversation actuellement affichée sera conservée.",
            default=messagebox.NO,
            icon=messagebox.WARNING,
            parent=self.root,
        )
        if not confirmed:
            return
        try:
            clear_history()
        except OSError as error:
            messagebox.showerror(
                "Suppression impossible",
                f"L’historique n’a pas pu être supprimé.\n\n{error}",
                parent=self.root,
            )
            return
        for window in self.history_windows:
            if window.winfo_exists():
                window.destroy()
        self.history_windows.clear()
        messagebox.showinfo(
            "Historique épuré",
            "Tous les échanges enregistrés ont été supprimés.",
            parent=self.root,
        )

    def append_message(self, speaker, message):
        """Ajoute un échange et fait défiler jusqu'au dernier message."""
        self.conversation.configure(state="normal")
        self.conversation.insert("end", f"{speaker}\n", "speaker")
        self.conversation.insert("end", f"{message}\n\n")
        self.conversation.configure(state="disabled")
        self.conversation.see("end")

    def send_message(self, event=None):
        """Lit la demande, appelle l'assistant puis affiche sa réponse."""
        message = self.request.get().strip()
        if not message:
            return
        self.request.delete(0, "end")
        self.append_message("Toi", message)
        try:
            response = respond(message)
        except (OSError, ValueError) as error:
            self.append_message(APP_NAME, "L'échange n'a pas pu être enregistré.")
            messagebox.showerror("Erreur d'historique", str(error), parent=self.root)
        else:
            self.append_message(APP_NAME, response)
        self.request.focus_set()


def launch():
    """Ouvre la fenêtre et attend les actions de l'utilisateur."""
    root = tk.Tk()
    ChatWindow(root)
    root.mainloop()
