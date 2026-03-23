import tkinter as tk
from tkinter import messagebox
import time
import random

CLAVE = "1234"  # ← CAMBIA ESTO CUANDO QUIERAS

historial = []

def liberar():
    usuario = entry_usuario.get()
    monto = entry_monto.get()
    clave = entry_clave.get()

    if usuario == "" or monto == "" or clave == "":
        messagebox.showerror("Error", "Faltan datos")
        return

    if clave != CLAVE:
        messagebox.showerror("Error", "Clave incorrecta")
        return

    label_estado.config(text="❌ Saldo insuficiente para liberar", fg="red")
    root.update()
    time.sleep(1.2)

    label_estado.config(text="🔍 Verificando fondos...")
    root.update()
    time.sleep(1.2)

    label_estado.config(text="🔄 Procesando transferencia...")
    root.update()
    time.sleep(1.2)

    label_estado.config(text="✅ Transferencia completada", fg="green")

    folio = random.randint(100000,999999)
    fecha = time.strftime("%d/%m/%Y %H:%M:%S")

    nombre = f"comprobante_{folio}.txt"
    with open(nombre, "w") as f:
        f.write("====== COMPROBANTE DE TRANSFERENCIA ======\n")
        f.write(f"Folio: {folio}\n")
        f.write(f"Usuario destino: {usuario}\n")
        f.write(f"Monto: ${monto} MXN\n")
        f.write("Estado: COMPLETADA\n")
        f.write("Banco: Sistema MX\n")
        f.write(f"Fecha: {fecha}\n")
        f.write("=========================================\n")

    registro = f"{fecha} | {usuario} | ${monto} MXN | Folio {folio}"
    historial.append(registro)
    lista_historial.insert(tk.END, registro)

    messagebox.showinfo("Listo", f"Transferencia completada\n\nComprobante:\n{nombre}")

# --- VENTANA ---
root = tk.Tk()
root.title("Sistema Supremo de Transferencias MX")
root.geometry("400x550")
root.configure(bg="#111")

titulo = tk.Label(root, text="💸 SISTEMA DE TRANSFERENCIAS MX 💸", fg="lime", bg="#111", font=("Consolas",12))
titulo.pack(pady=10)

tk.Label(root, text="Usuario destino:", fg="white", bg="#111").pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Monto (MXN):", fg="white", bg="#111").pack()
entry_monto = tk.Entry(root)
entry_monto.pack()

tk.Label(root, text="Clave de liberación:", fg="white", bg="#111").pack()
entry_clave = tk.Entry(root, show="*")
entry_clave.pack()

btn = tk.Button(root, text="LIBERAR TRANSFERENCIA", bg="green", fg="black", command=liberar)
btn.pack(pady=10)

label_estado = tk.Label(root, text="", fg="white", bg="#111")
label_estado.pack(pady=5)

tk.Label(root, text="📜 HISTORIAL", fg="cyan", bg="#111").pack(pady=5)
lista_historial = tk.Listbox(root, width=50)
lista_historial.pack(pady=5)

root.mainloop()