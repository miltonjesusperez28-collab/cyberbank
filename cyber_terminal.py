import tkinter as tk
import random
import time
import tkinter as tk
from PIL import Image, ImageTk

saldo = 0
historial = []

# ================= MATRIX =================

def matrix_intro():

    root = tk.Tk()
    root.title("Inicializando")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root,bg="black")
    canvas.pack(fill="both",expand=True)

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    columns = int(width/20)
    drops = [random.randint(-height,0) for _ in range(columns)]

    chars = "0123456789ABCDEF"

    def lluvia():

        canvas.delete("all")

        for i in range(len(drops)):

            char = random.choice(chars)

            x = i*20
            y = drops[i]

            canvas.create_text(x,y,text=char,fill="#00ff00",font=("Consolas",14))

            drops[i]+=20

            if drops[i] > height:
                drops[i] = random.randint(-200,0)

        root.after(50,lluvia)

    lluvia()

    root.after(4000, lambda: abrir_login(root))

    root.mainloop()

# ================= LOGIN =================

def abrir_login(matrix):

    matrix.destroy()

    login = tk.Tk()
    login.title("CyberBank")
    login.geometry("300x250")
    login.configure(bg="#0b0b0b")

    def entrar():

        user = entry_user.get()

        if user == "":
            estado.config(text="Usuario inválido",fg="red")
            return

        login.destroy()
        dashboard(user)

    tk.Label(login,text="CYBER BANK",fg="#00ff9c",bg="#0b0b0b",font=("Consolas",18)).pack(pady=20)

    entry_user = tk.Entry(login)
    entry_user.pack()

    entry_pass = tk.Entry(login,show="*")
    entry_pass.pack(pady=5)

    tk.Button(login,text="Entrar",bg="#00ff9c",command=entrar).pack(pady=10)

    estado = tk.Label(login,text="",bg="#0b0b0b")
    estado.pack()

    login.mainloop()

# ================= DASHBOARD =================

def dashboard(user):

    global saldo

    app = tk.Tk()
    app.title("CyberBank Dashboard")
    app.geometry("650x520")
    app.configure(bg="#0b0b0b")

    # TARJETA
    tarjeta = tk.Frame(app,bg="#111",width=420,height=180)
    tarjeta.pack(pady=20)

    numero = " ".join(str(random.randint(1000,9999)) for _ in range(4))

    tk.Label(tarjeta,text="CYBER BANK",fg="#00ff9c",bg="#111",font=("Consolas",16)).place(x=20,y=20)

    tk.Label(tarjeta,text=numero,fg="white",bg="#111",font=("Consolas",18)).place(x=20,y=90)

    tk.Label(tarjeta,text=user.upper(),fg="#00ff9c",bg="#111").place(x=20,y=130)

    # SALDO
    saldo_label = tk.Label(app,text="Saldo: $0",fg="#00ff9c",bg="#0b0b0b",font=("Consolas",14))
    saldo_label.pack()

    # CREAR SALDO
    frame = tk.Frame(app,bg="#0b0b0b")
    frame.pack(pady=10)

    tk.Label(frame,text="Saldo inicial",fg="#00ff9c",bg="#0b0b0b").grid(row=0,column=0)

    entry_saldo = tk.Entry(frame)
    entry_saldo.grid(row=0,column=1)

    def crear():

        global saldo

        try:
            saldo = float(entry_saldo.get())
        except:
            estado.config(text="Saldo inválido")
            return

        saldo_label.config(text=f"Saldo: ${saldo}")
        estado.config(text="Cuenta creada")

    tk.Button(frame,text="Crear cuenta",bg="#00ff9c",command=crear).grid(row=1,columnspan=2,pady=10)

    # TRANSFERENCIA
    tk.Label(frame,text="Destino (CLABE/Tarjeta)",fg="#00ff9c",bg="#0b0b0b").grid(row=2,column=0)

    entry_dest = tk.Entry(frame)
    entry_dest.grid(row=2,column=1)

    tk.Label(frame,text="Monto",fg="#00ff9c",bg="#0b0b0b").grid(row=3,column=0)

    entry_monto = tk.Entry(frame)
    entry_monto.grid(row=3,column=1)

    def transferir():

        global saldo

        try:
            monto = float(entry_monto.get())
        except:
            estado.config(text="Monto inválido")
            return

        if monto > saldo:
            estado.config(text="Saldo insuficiente")
            return

        estado.config(text="Procesando transferencia...")
        app.update()
        time.sleep(1)

        saldo -= monto
        saldo_label.config(text=f"Saldo: ${saldo}")

        movimiento = f"Transferencia ${monto}"
        historial.append(movimiento)

        lista.insert(tk.END,movimiento)

        # comprobante
        with open("comprobante.txt","w") as f:
            f.write(f"TRANSFERENCIA CYBER BANK\nMonto: ${monto}\nUsuario: {user}")

        estado.config(text="Transferencia completada")

    tk.Button(frame,text="Transferir",bg="#00ff9c",command=transferir).grid(row=4,columnspan=2,pady=10)

   import tkinter as tk
import random
import time

saldo = 0
historial = []

# ================= MATRIX =================

def matrix_intro():

    root = tk.Tk()
    root.title("Inicializando")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    canvas = tk.Canvas(root,bg="black")
    canvas.pack(fill="both",expand=True)

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    columns = int(width/20)
    drops = [random.randint(-height,0) for _ in range(columns)]

    chars = "0123456789ABCDEF"

    def lluvia():

        canvas.delete("all")

        for i in range(len(drops)):

            char = random.choice(chars)

            x = i*20
            y = drops[i]

            canvas.create_text(x,y,text=char,fill="#00ff00",font=("Consolas",14))

            drops[i]+=20

            if drops[i] > height:
                drops[i] = random.randint(-200,0)

        root.after(50,lluvia)

    lluvia()

    root.after(4000, lambda: abrir_login(root))

    root.mainloop()

# ================= LOGIN =================

def abrir_login(matrix):

    matrix.destroy()

    login = tk.Tk()
    login.title("CyberBank")
    login.geometry("300x250")
    login.configure(bg="#0b0b0b")

    def entrar():

        user = entry_user.get()

        if user == "":
            estado.config(text="Usuario inválido",fg="red")
            return

        login.destroy()
        dashboard(user)

    tk.Label(login,text="CYBER BANK",fg="#00ff9c",bg="#0b0b0b",font=("Consolas",18)).pack(pady=20)

    entry_user = tk.Entry(login)
    entry_user.pack()

    entry_pass = tk.Entry(login,show="*")
    entry_pass.pack(pady=5)

    tk.Button(login,text="Entrar",bg="#00ff9c",command=entrar).pack(pady=10)

    estado = tk.Label(login,text="",bg="#0b0b0b")
    estado.pack()

    login.mainloop()

# ================= DASHBOARD =================

def dashboard(user):

    global saldo

    app = tk.Tk()
    app.title("CyberBank Dashboard")
    app.geometry("650x520")
    app.configure(bg="#0b0b0b")

    # TARJETA
    tarjeta = tk.Frame(app,bg="#111",width=420,height=180)
    tarjeta.pack(pady=20)

    numero = " ".join(str(random.randint(1000,9999)) for _ in range(4))

    tk.Label(tarjeta,text="CYBER BANK",fg="#00ff9c",bg="#111",font=("Consolas",16)).place(x=20,y=20)

    tk.Label(tarjeta,text=numero,fg="white",bg="#111",font=("Consolas",18)).place(x=20,y=90)

    tk.Label(tarjeta,text=user.upper(),fg="#00ff9c",bg="#111").place(x=20,y=130)

    # SALDO
    saldo_label = tk.Label(app,text="Saldo: $0",fg="#00ff9c",bg="#0b0b0b",font=("Consolas",14))
    saldo_label.pack()

    # CREAR SALDO
    frame = tk.Frame(app,bg="#0b0b0b")
    frame.pack(pady=10)

    tk.Label(frame,text="Saldo inicial",fg="#00ff9c",bg="#0b0b0b").grid(row=0,column=0)

    entry_saldo = tk.Entry(frame)
    entry_saldo.grid(row=0,column=1)

    def crear():

        global saldo

        try:
            saldo = float(entry_saldo.get())
        except:
            estado.config(text="Saldo inválido")
            return

        saldo_label.config(text=f"Saldo: ${saldo}")
        estado.config(text="Cuenta creada")

    tk.Button(frame,text="Crear cuenta",bg="#00ff9c",command=crear).grid(row=1,columnspan=2,pady=10)

    # TRANSFERENCIA
    tk.Label(frame,text="Destino (CLABE/Tarjeta)",fg="#00ff9c",bg="#0b0b0b").grid(row=2,column=0)

    entry_dest = tk.Entry(frame)
    entry_dest.grid(row=2,column=1)

    tk.Label(frame,text="Monto",fg="#00ff9c",bg="#0b0b0b").grid(row=3,column=0)

    entry_monto = tk.Entry(frame)
    entry_monto.grid(row=3,column=1)

    def transferir():

        global saldo

        try:
            monto = float(entry_monto.get())
        except:
            estado.config(text="Monto inválido")
            return

        if monto > saldo:
            estado.config(text="Saldo insuficiente")
            return

        estado.config(text="Procesando transferencia...")
        app.update()
        time.sleep(1)

        saldo -= monto
        saldo_label.config(text=f"Saldo: ${saldo}")

        movimiento = f"Transferencia ${monto}"
        historial.append(movimiento)

        lista.insert(tk.END,movimiento)

        # comprobante
        with open("comprobante.txt","w") as f:
            f.write(f"TRANSFERENCIA CYBER BANK\nMonto: ${monto}\nUsuario: {user}")

        estado.config(text="Transferencia completada")

    tk.Button(frame,text="Transferir",bg="#00ff9c",command=transferir).grid(row=4,columnspan=2,pady=10)

    estado = tk.Label(app,text="Sistema listo",fg="#00ff9c",bg="#0b0b0b")
    estado.pack()

    # HISTORIAL
    tk.Label(app,text="Historial",fg="#00ff9c",bg="#0b0b0b").pack()

    lista = tk.Listbox(app,width=60,height=10,bg="#111",fg="#00ff9c")
    lista.pack()

root = tk.Tk()
root.geometry("800x600")

# cargar imagen
img = Image.open("calavera.png")
img = img.resize((800, 600))
bg = ImageTk.PhotoImage(img)

label = tk.Label(root, image=bg, bg="black")
label.image = bg
label.place(x=0, y=0)

# texto estilo hacker
texto = tk.Label(root, text="ACCESS GRANTED", fg="#00ff00", bg="black", font=("Courier", 20))
texto.place(x=250, y=50)
root.mainloop()
    
# ================= START =================

mainloop()