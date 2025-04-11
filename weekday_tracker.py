import tkinter as tk
from tkinter import messagebox
import keyboard  # Zum Erfassen von globalen Hotkeys

class WeekdayTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Weekday Tracker")
        self.root.geometry("350x300")  # Fenstergröße etwas größer
        self.root.resizable(False, False)  # Fenstergröße nicht veränderbar

        # Wochentage und Startwert
        self.current_day = 1  # Montag
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.darkmode = False
        self.global_hotkey_enabled = False  # Zustand für den Global Hotkey

        # Initialisierung des Hotkeys
        self.hotkey = "n"  # Default hotkey (set 'n' by default for "Next Day")
        self.root.bind(self.hotkey, self.handle_hotkey)

        # Label zur Anzeige des aktuellen Tages
        self.label = tk.Label(root, text=self.days[self.current_day - 1], font=("Helvetica", 24))
        self.label.pack(pady=20)

        # Next Day Button
        self.next_day_button = tk.Button(root, text="Next Day", font=("Helvetica", 14), command=self.next_day)
        self.next_day_button.pack(pady=10)

        # Set Hotkey Button
        self.set_hotkey_button = tk.Button(root, text="Set Hotkey", font=("Helvetica", 14), command=self.set_hotkey)
        self.set_hotkey_button.pack(pady=5)

        # Label zur Anzeige des aktuellen Hotkeys
        self.hotkey_label = tk.Label(root, text=f"Hotkey: {self.hotkey}", font=("Helvetica", 12))
        self.hotkey_label.pack(pady=5)

        # Darkmode Button und Global Hotkey Button
        self.global_hotkey_button = tk.Button(root, text="Global Hotkey On/Off", font=("Helvetica", 10), command=self.toggle_global_hotkey)
        self.global_hotkey_button.pack(pady=5, side="bottom", fill="x")

        self.darkmode_button = tk.Button(root, text="Toggle Darkmode", font=("Helvetica", 10), command=self.toggle_darkmode)
        self.darkmode_button.pack(pady=5, side="bottom", fill="x")

        # Global Hotkey Überprüfung
        if self.global_hotkey_enabled:
            keyboard.add_hotkey(self.hotkey, self.next_day)

    def next_day(self):
        self.current_day = (self.current_day % 7) + 1
        self.label.config(text=self.days[self.current_day - 1])

    def toggle_darkmode(self):
        self.darkmode = not self.darkmode
        if self.darkmode:
            self.root.config(bg="black")
            self.label.config(bg="black", fg="white")
            self.next_day_button.config(bg="gray", fg="white")
            self.set_hotkey_button.config(bg="gray", fg="white")
            self.hotkey_label.config(bg="black", fg="white")
            self.global_hotkey_button.config(bg="gray", fg="white")
            self.darkmode_button.config(bg="gray", fg="white")
        else:
            self.root.config(bg="white")
            self.label.config(bg="white", fg="black")
            self.next_day_button.config(bg="lightgray", fg="black")
            self.set_hotkey_button.config(bg="lightgray", fg="black")
            self.hotkey_label.config(bg="white", fg="black")
            self.global_hotkey_button.config(bg="lightgray", fg="black")
            self.darkmode_button.config(bg="lightgray", fg="black")

    def set_hotkey(self):
        # Hotkey setzen ohne Bestätigung, der Benutzer drückt eine Taste
        self.root.config(cursor="crosshair")  # Zeigt den Crosshair-Cursor an, um dem Benutzer zu signalisieren, dass er eine Taste drücken soll
        self.hotkey = None  # Hotkey zurücksetzen
        self.root.bind("<KeyPress>", self.on_hotkey_selected)  # Event-Handler für die Taste

        # Popup sichtbar, in dem der Hotkey geändert werden kann
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Press Your New Hotkey")
        self.popup.geometry("300x150")  # Popup größer gemacht
        self.popup.config(bg="lightgray" if not self.darkmode else "black")
        label = tk.Label(self.popup, text="Press the key you want to set for 'Next Day'", font=("Helvetica", 12), bg="lightgray" if not self.darkmode else "black", fg="black" if not self.darkmode else "white")
        label.pack(pady=30)  # Etwas mehr Platz für den Text

    def on_hotkey_selected(self, event):
        # Überprüfen, ob eine Taste gedrückt wurde, und den Hotkey nur dann ändern
        self.hotkey = event.char.lower()  # Setze den neuen Hotkey (Kleinbuchstaben)
        self.root.bind(self.hotkey, self.handle_hotkey)  # Binde den neuen Hotkey zum "Next Day"
        self.hotkey_label.config(text=f"Hotkey: {self.hotkey.upper()}")  # Update der Hotkey-Anzeige
        self.root.config(cursor="arrow")  # Setze den Cursor zurück
        self.popup.destroy()  # Schließe das Popup nach dem Setzen des Hotkeys

        # Wenn der globale Hotkey aktiviert wird, füge ihn hinzu
        if self.global_hotkey_enabled:
            keyboard.add_hotkey(self.hotkey, self.next_day)

        # Entferne den Event-Handler, der immer wieder den Hotkey setzen würde
        self.root.unbind("<KeyPress>")

    def handle_hotkey(self, event):
        self.next_day()

    def toggle_global_hotkey(self):
        self.global_hotkey_enabled = not self.global_hotkey_enabled
        status = "enabled" if self.global_hotkey_enabled else "disabled"
        messagebox.showinfo("Global Hotkey", f"Global Hotkey is now {status}")
        
        # Wenn der globale Hotkey aktiviert wird, setze ihn
        if self.global_hotkey_enabled:
            keyboard.add_hotkey(self.hotkey, self.next_day)
        else:
            keyboard.remove_hotkey(self.hotkey)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeekdayTracker(root)
    root.mainloop()
