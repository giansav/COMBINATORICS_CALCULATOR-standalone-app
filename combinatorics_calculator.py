import sys
import os

if getattr(sys, 'frozen', False):
    # Percorso quando il codice è impacchettato in un eseguibile
    BASE_DIR = sys._MEIPASS
else:
    # Percorso normale durante l'esecuzione da script Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGES_DIR = os.path.join(BASE_DIR, "images")


import tkinter as tk
from tkinter import ttk, messagebox
from itertools import permutations, combinations, combinations_with_replacement, product
import math
from PIL import Image, ImageTk


# Funzione per calcolare il numero totale di combinazioni/permutazioni
def calculate_total_count(n, r, calculation_type):
    try:
        n, r = int(n), int(r)
        if calculation_type == "permutazioni":
            return math.factorial(n) // math.factorial(n - r)
        elif calculation_type == "disposizioni_semplici":
            return math.factorial(n) // math.factorial(n - r)
        elif calculation_type == "disposizioni_con_ripetizioni":
            return n ** r
        elif calculation_type == "combinazioni_semplici":
            return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
        elif calculation_type == "combinazioni_con_ripetizioni":
            return math.factorial(n + r - 1) // (math.factorial(r) * math.factorial(n - 1))
    except ValueError:
        return 0
    return 0

# Funzione per generare combinazioni/permutazioni
def calculate():
    result_text.set("")
    result_display.config(state=tk.NORMAL)  # Abilita la modifica del widget Text
    result_display.delete("1.0", tk.END)  # Pulisce il contenuto precedente
    
    num_objects = num_objects_entry.get()
    objects_list = objects_list_entry.get()
    r = combinations_number_entry.get()
    calculation_type = calculation_type_combobox.get()
    
    if not r:
        messagebox.showerror("Errore", "Inserire la lunghezza della sequenza (k).")
        return

    try:
        r = int(r)
        if num_objects and objects_list:
            messagebox.showerror("Errore", "Inserire solo il numero di oggetti OPPURE una lista di oggetti, non entrambi.")
            return
        elif num_objects:
            n = int(num_objects)
            total_count = calculate_total_count(n, r, calculation_type)
            result_text.set(f"Numero totale di combinazioni: {total_count}")
        elif objects_list:
            obj_list = objects_list.split(",")
            n = len(obj_list)

            if show_only_count_var.get():
                total_count = calculate_total_count(n, r, calculation_type)
                result_text.set(f"Numero totale di combinazioni: {total_count}")
            else:
                # Generiamo le sequenze corrette in base alla scelta dell'utente
                if calculation_type == "permutazioni":
                    raw_result = list(permutations(obj_list, r))  # Permutazioni esatte di lunghezza r
                elif calculation_type == "disposizioni_semplici":
                    raw_result = list(permutations(obj_list, r))  # Disposizioni senza ripetizioni = permutazioni di lunghezza r
                elif calculation_type == "disposizioni_con_ripetizioni":
                    raw_result = list(product(obj_list, repeat=r))  # Disposizioni con ripetizione = prodotto cartesiano
                elif calculation_type == "combinazioni_semplici":
                    raw_result = list(combinations(obj_list, r))  # Combinazioni senza ripetizioni di lunghezza r
                elif calculation_type == "combinazioni_con_ripetizioni":
                    raw_result = list(combinations_with_replacement(obj_list, r))  # Combinazioni con ripetizioni

                total_count = len(raw_result)
                result_text.set(f"Numero totale di combinazioni: {total_count}")

                # Calcoliamo il numero di colonne in base alla larghezza del widget
                widget_width = result_display.winfo_width()  # Larghezza attuale del Text
                char_width = 10  # Stimiamo che ogni combinazione occupi circa 10 caratteri
                num_columns = max(1, widget_width // char_width)  # Numero di colonne dinamico

                for i, item in enumerate(raw_result, start=1):
                    result_display.insert(tk.END, " ".join(item) + "   ", "center")  # Applica il tag "center"
                    if i % num_columns == 0:  # Vai a capo dinamicamente
                        result_display.insert(tk.END, "\n", "center")

    except ValueError:
        messagebox.showerror("Errore", "Inserire valori numerici validi.")
    
    result_display.config(state=tk.DISABLED)  # Blocca il widget per evitare modifiche manuali


# Creazione della finestra principale
root = tk.Tk()
root.title("Calcolo Combinatorio")
root.geometry("800x600")
root.configure(bg="#f0f8ff")

# Titolo
title_label = tk.Label(root, text="Calcolo Combinatorio", font=("Arial", 20, "bold"), bg="white", fg="#0066cc")
title_label.pack(fill=tk.X, pady=5)

# Contenitore principale
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Sezione form (sinistra)
form_frame = tk.Frame(main_frame, bg="#f0f8ff")
form_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)

tk.Label(form_frame, text="Numero di oggetti (n):", bg="#f0f8ff").pack(anchor="w")
num_objects_entry = tk.Entry(form_frame)
num_objects_entry.pack(fill=tk.X)

tk.Label(form_frame, text="Lista di oggetti (separati da virgola):", bg="#f0f8ff").pack(anchor="w")
objects_list_entry = tk.Entry(form_frame)
objects_list_entry.pack(fill=tk.X)

tk.Label(form_frame, text="Lunghezza della sequenza (k):", bg="#f0f8ff").pack(anchor="w")
combinations_number_entry = tk.Entry(form_frame)
combinations_number_entry.pack(fill=tk.X)

tk.Label(form_frame, text="Tipo di calcolo:", bg="#f0f8ff").pack(anchor="w")
calculation_type_combobox = ttk.Combobox(form_frame, values=[
    "permutazioni",
    "disposizioni_semplici",
    "disposizioni_con_ripetizioni",
    "combinazioni_semplici",
    "combinazioni_con_ripetizioni"
])
calculation_type_combobox.pack(fill=tk.X)
calculation_type_combobox.current(0)

show_only_count_var = tk.BooleanVar()
show_only_count_checkbox = tk.Checkbutton(form_frame, text="Mostra solo il numero totale", variable=show_only_count_var, bg="#f0f8ff")
show_only_count_checkbox.pack(anchor="w")

calculate_button = tk.Button(form_frame, text="Calcola", command=calculate, bg="#0066cc", fg="white")
calculate_button.pack(pady=10, fill=tk.X)

# Sezione legenda (destra)
legend_frame = tk.Frame(main_frame, bg="#f0f8ff")
legend_frame.pack(side=tk.RIGHT, padx=20, fill=tk.BOTH, expand=True)

tk.Label(legend_frame, text="Tipi di Calcolo", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#0066cc").pack()

image_refs = []  # Lista globale per memorizzare le immagini e non farle eliminare da Python

base_height = 50  # Altezza fissa per le immagini normali
small_base_height = 30  # Altezza fissa per le immagini più piccole (prima e terza)

# Diciamo che vogliamo ridimensionare le immagini a dimensioni personalizzate
image_dimensions = {
    "perm.png": (250, 30),  # Esempio: larghezza 250px, altezza 30px per 'perm.png'
    "arrang.png": (300, 50),  # Esempio per 'arrang.png'
    "arrang_rep.png": (90, 30),  # Esempio per 'arrang_rep.png'
    "comb.png": (310, 60),  # Esempio per 'comb.png'
    "comb_rep.png": (310, 50)  # Esempio per 'comb_rep.png'
}

for idx, (title, img_name) in enumerate([
    ("Permutazioni", "perm.png"),
    ("Disposizioni senza ripetizioni", "arrang.png"),
    ("Disposizioni con ripetizioni", "arrang_rep.png"),
    ("Combinazioni senza ripetizioni", "comb.png"),
    ("Combinazioni con ripetizioni", "comb_rep.png"),
]):
    tk.Label(legend_frame, text=title, font=("Arial", 12, "bold"), bg="#f0f8ff").pack()

    img_path = os.path.join(IMAGES_DIR, img_name)
    
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            
            # Ottieni le dimensioni personalizzate per l'immagine corrente
            custom_width, custom_height = image_dimensions.get(img_name, (100, 50))  # Usa 100x50 come default
            
            # Ridimensiona l'immagine con le dimensioni specificate
            img = img.resize((custom_width, custom_height), Image.Resampling.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img)
            
            image_refs.append(img_tk)  # Salva il riferimento per evitare che l'immagine venga cancellata
            tk.Label(legend_frame, image=img_tk, bg="#f0f8ff").pack()
            
        except Exception as e:
            tk.Label(legend_frame, text=f"[Errore: {e}]", bg="#f0f8ff").pack()
    else:
        tk.Label(legend_frame, text=f"[Immagine non trovata: {img_name}]", bg="#f0f8ff").pack()


# Sezione risultati (in basso)
result_frame = tk.Frame(root, bg="#e0f7fa")
result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(result_frame, textvariable=result_text, bg="#e0f7fa", font=("Arial", 12, "bold"))
result_label.pack()

# Creazione del frame per il Text e la scrollbar
text_frame = tk.Frame(result_frame, bg="#e0f7fa")
text_frame.pack(fill=tk.BOTH, expand=True)

# Creazione del widget Text per i risultati
result_display = tk.Text(text_frame, height=10, wrap="word", bg="white", font=("Arial", 12))
result_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Creazione della scrollbar verticale
scrollbar = tk.Scrollbar(text_frame, command=result_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_display.config(yscrollcommand=scrollbar.set)  # Collega il Text alla scrollbar

# Configuriamo un tag per centrare il testo
result_display.tag_configure("center", justify="center")
result_display.config(state=tk.DISABLED)  # Bloccare il widget inizialmente




# Avvio dell'interfaccia
root.mainloop()