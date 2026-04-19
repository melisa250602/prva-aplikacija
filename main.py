import customtkinter as ctk
import csv
import os
from tkinter import messagebox

# Podešavanja izgleda
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Manager - Claude Code Demo")
        self.geometry("850x550")
        self.filename = 'baza_studenata.csv'
       
        # Kreiranje CSV fajla sa zaglavljem ako ne postoji
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Ime', 'Prezime', 'Indeks'])

        # --- GRID KONFIGURACIJA ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- LIJEVI PANEL (Input polja) ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
       
        self.label_title = ctk.CTkLabel(self.sidebar, text="UNOS PODATAKA", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=20)

        self.entry_id = ctk.CTkEntry(self.sidebar, placeholder_text="ID (obavezan)")
        self.entry_id.grid(row=1, column=0, padx=20, pady=10)

        self.entry_ime = ctk.CTkEntry(self.sidebar, placeholder_text="Ime")
        self.entry_ime.grid(row=2, column=0, padx=20, pady=10)

        self.entry_prezime = ctk.CTkEntry(self.sidebar, placeholder_text="Prezime")
        self.entry_prezime.grid(row=3, column=0, padx=20, pady=10)

        self.entry_indeks = ctk.CTkEntry(self.sidebar, placeholder_text="Broj Indeksa")
        self.entry_indeks.grid(row=4, column=0, padx=20, pady=10)

        # Dugmad
        self.btn_add = ctk.CTkButton(self.sidebar, text="Dodaj studenta", command=self.add_student)
        self.btn_add.grid(row=5, column=0, padx=20, pady=10)

        self.btn_update = ctk.CTkButton(self.sidebar, text="Ažuriraj po ID-u", command=self.update_student, fg_color="#D68910")
        self.btn_update.grid(row=6, column=0, padx=20, pady=10)

        self.btn_delete = ctk.CTkButton(self.sidebar, text="Obriši po ID-u", command=self.delete_student, fg_color="#C0392B")
        self.btn_delete.grid(row=7, column=0, padx=20, pady=10)

        # --- DESNI PANEL (Prikaz podataka) ---
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)

        self.btn_refresh = ctk.CTkButton(self.main_content, text="Osvježi tabelu", command=self.load_data)
        self.btn_refresh.grid(row=0, column=0, padx=20, pady=10)

        self.textbox = ctk.CTkTextbox(self.main_content, font=("Courier", 12))
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
       
        self.load_data()

    # --- CRUD LOGIKA ---

    def load_data(self):
        """Čitanje iz CSV i prikaz (Read)"""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        header = f"{'ID':<7} | {'Ime':<15} | {'Prezime':<15} | {'Indeks':<10}\n"
        self.textbox.insert("end", header)
        self.textbox.insert("end", "-" * 55 + "\n")
       
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    line = f"{row['ID']:<7} | {row['Ime']:<15} | {row['Prezime']:<15} | {row['Indeks']:<10}\n"
                    self.textbox.insert("end", line)
        except Exception as e:
            print(f"Greška pri čitanju: {e}")
       
        self.textbox.configure(state="disabled")

    def add_student(self):
        """Dodavanje novog reda (Create)"""
        s_id = self.entry_id.get()
        ime = self.entry_ime.get()
        prezime = self.entry_prezime.get()
        indeks = self.entry_indeks.get()

        if s_id and ime and prezime and indeks:
            with open(self.filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([s_id, ime, prezime, indeks])
            self.clear_entries()
            self.load_data()
            messagebox.showinfo("Uspjeh", "Student uspješno dodat!")
        else:
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena!")

    def delete_student(self):
        """Brisanje na osnovu ID-a (Delete)"""
        target_id = self.entry_id.get()
        if not target_id:
            messagebox.showwarning("Greška", "Unesite ID za brisanje!")
            return

        rows = []
        found = False
        with open(self.filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row[0] != target_id: # Provjera ID kolone
                    rows.append(row)
                else:
                    found = True

        if found:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
            self.load_data()
            messagebox.showinfo("Uspjeh", f"ID {target_id} je obrisan.")
        else:
            messagebox.showerror("Greška", "ID nije pronađen u bazi.")

    def update_student(self):
        """Izmjena podataka na osnovu ID-a (Update)"""
        target_id = self.entry_id.get()
        if not target_id:
            messagebox.showwarning("Greška", "Unesite ID koji želite mijenjati!")
            return

        rows = []
        found = False
        with open(self.filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row[0] == target_id:
                    # Uzmi nove vrijednosti ili zadrži stare ako su polja prazna
                    novo_ime = self.entry_ime.get() if self.entry_ime.get() else row[1]
                    novo_prezime = self.entry_prezime.get() if self.entry_prezime.get() else row[2]
                    novi_indeks = self.entry_indeks.get() if self.entry_indeks.get() else row[3]
                    rows.append([target_id, novo_ime, novo_prezime, novi_indeks])
                    found = True
                else:
                    rows.append(row)

        if found:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
            self.load_data()
            messagebox.showinfo("Uspjeh", "Podaci su ažurirani.")
        else:
            messagebox.showerror("Greška", "ID nije pronađen.")

    def clear_entries(self):
        self.entry_id.delete(0, 'end')
        self.entry_ime.delete(0, 'end')
        self.entry_prezime.delete(0, 'end')
        self.entry_indeks.delete(0, 'end')

if __name__ == "__main__":
    app = App()
    app.mainloop()
