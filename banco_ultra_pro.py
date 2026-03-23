import tkinter as tk
from tkinter import messagebox
import time
import random

NOMBRE_BANCO = "CYBER BANK MX"
CLAVE = "1234"

saldo = 15000
historial = []

def login():
    if entry_login.get() == CLAVE:
        login_frame.pack_forget()
        app_frame.pack()
        actualizar_saldo()
    else:
        messagebox.showerror("Error", "Clave incorrecta")

def actualizar_saldo():
    lbl_saldo.config(text=f"Saldo: ${saldo} MXN")

def scan_animacion():
    estado.set("Escaneando red financiera...")
    root.update()
    time.sleep(0.7)

    estado.set("Conectando nodos bancarios...")
    root.update()
    time.sleep(0.7)

    estado.set("Validando transacción...")
    root.update()
    time.sleep(0.7)

def depositar():
    global saldo
    monto = entry_deposito.get()

    if not monto.isdigit():
        messagebox.showerror("Error", "Monto inválido")
        return

    monto = int(monto)
    saldo += monto

    fecha = time.strftime("%d/%m/%Y %H:%M:%S")
    registro = f"{fecha} | DEPÓSITO +${monto}"

    historial.append(registro)
    lista.insert(tk.END, registro)

    actualizar_saldo()

def transferir():
    global saldo

    usuario = entry_destino.get()
    monto = entry_transferencia.get()

    if usuario == "" or not monto.isdigit():
        messagebox.showerror("Error", "Datos inválidos")
        return

    monto = int(monto)

    if monto > saldo:
        messagebox.showwarning("Fondos insuficientes", "Saldo insuficiente")
        return

    scan_animacion()

    saldo -= monto

    folio = random.randint(100000,999999)
    fecha = time.strftime("%d/%m/%Y %H:%M:%S")

    registro = f"{fecha} | TRANSFERENCIA a {usuario} -${monto} | Folio {folio}"

    historial.append(registro)
    lista.insert(tk.END, registro)

    actualizar_saldo()

    nombre = f"comprobante_{folio}.txt"

    with open(nombre,"w") as f:
        f.write("=== COMPROBANTE BANCARIO ===\n")
        f.write(f"Banco: {NOMBRE_BANCO}\n")
        f.write(f"Destino: {usuario}\n")
        f.write(f"Monto: ${monto} MXN\n")
        f.write(f"Folio: {folio}\n")
        f.write(f"Fecha: {fecha}\n")
        f.write("Estado: COMPLETADO\n")

    estado.set("Transferencia completada")

    messagebox.showinfo("Operación exitosa",f"Transferencia completada\nFolio: {folio}")

root = tk.Tk()
root.title("Cyber Bank System")
root.geometry("500x600")
root.configure(bg="#0a0a0a")

# LOGIN
login_frame = tk.Frame(root,bg="#0a0a0a")
login_frame.pack(expand=True)

tk.Label(login_frame,text=NOMBRE_BANCO,
fg="#00ff9c",
bg="#0a0a0a",
font=("Consolas",18,"bold")).pack(pady=30)

tk.Label(login_frame,text="Clave de acceso",
fg="white",
bg="#0a0a0a").pack()

entry_login = tk.Entry(login_frame,show="*",width=20)
entry_login.pack(pady=10)

tk.Button(login_frame,
text="Entrar",
bg="#00ff9c",
command=login).pack()

# APP
app_frame = tk.Frame(root,bg="#0a0a0a")

tk.Label(app_frame,
text=NOMBRE_BANCO,
fg="#00ff9c",
bg="#0a0a0a",
font=("Consolas",16,"bold")).pack(pady=10)

lbl_saldo = tk.Label(app_frame,
text="",
fg="#00ff9c",
bg="#0a0a0a",
font=("Consolas",12))

lbl_saldo.pack()

# DEPÓSITO
dep = tk.LabelFrame(app_frame,text="Depositar",fg="white",bg="#0a0a0a")
dep.pack(pady=10)

entry_deposito = tk.Entry(dep)
entry_deposito.grid(row=0,column=0)

tk.Button(dep,text="Depositar",command=depositar).grid(row=0,column=1)

# TRANSFERENCIA
trans = tk.LabelFrame(app_frame,text="Transferencia",fg="white",bg="#0a0a0a")
trans.pack(pady=10)

tk.Label(trans,text="Destino",bg="#0a0a0a",fg="white").grid(row=0,column=0)
entry_destino = tk.Entry(trans)
entry_destino.grid(row=0,column=1)

tk.Label(trans,text="Monto",bg="#0a0a0a",fg="white").grid(row=1,column=0)
entry_transferencia = tk.Entry(trans)
entry_transferencia.grid(row=1,column=1)

tk.Button(trans,text="Enviar",command=transferir).grid(row=2,columnspan=2)

estado = tk.StringVar()
estado.set("Sistema listo")

tk.Label(app_frame,
textvariable=estado,
fg="#00ff9c",
bg="#0a0a0a").pack(pady=5)

tk.Label(app_frame,
text="Historial",
fg="white",
bg="#0a0a0a").pack()
lista = tk.Listbox(app_frame,width=55,height=12,bg="#111",fg="#00ff9c")
lista.pack()

root.mainloop()