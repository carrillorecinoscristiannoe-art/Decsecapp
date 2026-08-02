import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import json
import os
import random

DB_FILE = "usuarios.json"

def generar_id_unico(usuarios_existentes):
    """Genera un ID aleatorio único de 6 dígitos que no se repita en la base de datos"""
    while True:
        nuevo_id = str(random.randint(100000, 999999))
        id_usado = False
        for datos in usuarios_existentes.values():
            if isinstance(datos, dict) and datos.get("id_unico") == nuevo_id:
                id_usado = True
                break
        if not id_usado:
            return nuevo_id

def cargar_usuarios():
    usuarios = {}
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                usuarios = json.load(f)
        except Exception:
            usuarios = {}

    # Garantizar cuenta Admin
    if "admin" not in usuarios or not isinstance(usuarios["admin"], dict):
        usuarios["admin"] = {
            "pass": "mr9026548",
            "foto": None,
            "id_unico": "902654",
            "amigos": []
        }
    elif "id_unico" not in usuarios["admin"]:
        usuarios["admin"]["id_unico"] = "902654"

    return usuarios

def guardar_usuarios(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DedSec System")
        
        self.ancho = self.root.winfo_screenwidth()
        self.alto = self.root.winfo_screenheight()
        self.root.geometry(f"{self.ancho}x{self.alto}")
        self.root.configure(bg="#0a0a0a")
        
        self.usuario_actual = None
        self.foto_img_tk = None
        
        self.pantalla_login()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # 1. LOGIN (REPARACIÓN AUTOMÁTICA DE ID)
    # ==========================================
    def pantalla_login(self):
        self.limpiar_pantalla()
        
        canvas = tk.Canvas(self.root, width=self.ancho, height=self.alto, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cx = self.ancho // 2
        cy = self.alto // 2

        canvas.create_text(cx, cy - 280, text="DedSec", font=("Consolas", 32, "bold"), fill="#00FF66")
        canvas.create_text(cx, cy - 230, text="SISTEMA DE ACCESO", font=("Arial", 10, "bold"), fill="#888888")
        
        lbl_u = tk.Label(self.root, text="Usuario:", font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#0a0a0a")
        ent_user = tk.Entry(self.root, font=("Arial", 12), bg="#1a1a1a", fg="#00FF66", insertbackground="white", bd=1, width=22)
        ent_user.insert(0, "admin")
        
        lbl_p = tk.Label(self.root, text="Contraseña:", font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#0a0a0a")
        ent_pass = tk.Entry(self.root, show="*", font=("Arial", 12), bg="#1a1a1a", fg="#00FF66", insertbackground="white", bd=1, width=22)
        
        btn_login = tk.Button(self.root, text="Iniciar Sesión", bg="#00FF66", fg="#000000", font=("Arial", 11, "bold"),
                              command=lambda: self.validar_login(ent_user.get(), ent_pass.get()), width=18, bd=0)
        
        btn_reg = tk.Button(self.root, text="Registrar otra cuenta", bg="#2196F3", fg="#FFFFFF", font=("Arial", 10, "bold"),
                             command=self.pantalla_registro, width=18, bd=0)

        canvas.create_window(cx, cy - 160, window=lbl_u)
        canvas.create_window(cx, cy - 120, window=ent_user)
        
        canvas.create_window(cx, cy - 50, window=lbl_p)
        canvas.create_window(cx, cy - 10, window=ent_pass)
        
        canvas.create_window(cx, cy + 80, window=btn_login)
        canvas.create_window(cx, cy + 150, window=btn_reg)

    def validar_login(self, u, p):
        u, p = u.strip(), p.strip()
        usuarios = cargar_usuarios()
        
        if u in usuarios and isinstance(usuarios[u], dict) and usuarios[u].get("pass") == p:
            # SI EL USUARIO NO TIENE ID O ESTÁ VACÍO, SE LE ASIGNA UNO DE INMEDIATO
            if "id_unico" not in usuarios[u] or not usuarios[u]["id_unico"]:
                nuevo_id = generar_id_unico(usuarios)
                usuarios[u]["id_unico"] = nuevo_id
                guardar_usuarios(usuarios)
                messagebox.showinfo("Sistema DedSec", f"Se asignó un nuevo ID de Operativo a tu cuenta: #{nuevo_id}")

            if "amigos" not in usuarios[u]:
                usuarios[u]["amigos"] = []
                guardar_usuarios(usuarios)

            self.usuario_actual = u
            self.pantalla_menu_principal()
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")

    # ==========================================
    # 2. REGISTRO
    # ==========================================
    def pantalla_registro(self):
        self.limpiar_pantalla()
        
        canvas = tk.Canvas(self.root, width=self.ancho, height=self.alto, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cx = self.ancho // 2
        cy = self.alto // 2

        canvas.create_text(cx, cy - 280, text="DedSec", font=("Consolas", 30, "bold"), fill="#00FF66")
        canvas.create_text(cx, cy - 230, text="CREAR NUEVO OPERATIVO", font=("Arial", 10, "bold"), fill="#888888")
        
        lbl_u = tk.Label(self.root, text="Nuevo Usuario:", font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#0a0a0a")
        reg_user = tk.Entry(self.root, font=("Arial", 12), bg="#1a1a1a", fg="#00FF66", insertbackground="white", bd=1, width=22)
        
        lbl_p = tk.Label(self.root, text="Nueva Contraseña:", font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#0a0a0a")
        reg_pass = tk.Entry(self.root, show="*", font=("Arial", 12), bg="#1a1a1a", fg="#00FF66", insertbackground="white", bd=1, width=22)
        
        btn_save = tk.Button(self.root, text="Guardar Registro", bg="#2196F3", fg="#FFFFFF", font=("Arial", 11, "bold"),
                             command=lambda: self.guardar_registro(reg_user.get(), reg_pass.get()), width=18, bd=0)
        
        btn_back = tk.Button(self.root, text="<- Volver al Login", bg="#0a0a0a", fg="#00FF66", font=("Arial", 10, "underline"),
                             command=self.pantalla_login, bd=0)

        canvas.create_window(cx, cy - 160, window=lbl_u)
        canvas.create_window(cx, cy - 120, window=reg_user)
        
        canvas.create_window(cx, cy - 50, window=lbl_p)
        canvas.create_window(cx, cy - 10, window=reg_pass)
        
        canvas.create_window(cx, cy + 80, window=btn_save)
        canvas.create_window(cx, cy + 150, window=btn_back)

    def guardar_registro(self, u, p):
        u, p = u.strip(), p.strip()
        if not u or not p:
            messagebox.showwarning("Atención", "Completa todos los campos.")
            return
            
        usuarios = cargar_usuarios()
        if u in usuarios:
            messagebox.showerror("Error", "El usuario ya existe.")
        else:
            nuevo_id = generar_id_unico(usuarios)
            usuarios[u] = {
                "pass": p,
                "foto": None,
                "id_unico": nuevo_id,
                "amigos": []
            }
            guardar_usuarios(usuarios)
            messagebox.showinfo("DedSec", f"¡Cuenta registrada con éxito!\nTu ID asignado es: #{nuevo_id}")
            self.pantalla_login()

    # ==========================================
    # 3. MENÚ PRINCIPAL
    # ==========================================
    def pantalla_menu_principal(self):
        self.limpiar_pantalla()
        
        canvas = tk.Canvas(self.root, width=self.ancho, height=self.alto, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cx = self.ancho // 2
        cy = self.alto // 2

        usuarios = cargar_usuarios()
        datos_u = usuarios.get(self.usuario_actual, {})
        mi_id = datos_u.get("id_unico", "SIN ID")

        canvas.create_text(cx, cy - 320, text="PANEL CENTRAL DEDSEC", font=("Consolas", 18, "bold"), fill="#00FF66")
        canvas.create_text(cx, cy - 280, text=f"OPERATIVO: {self.usuario_actual.upper()}", font=("Arial", 11, "bold"), fill="#FFFFFF")
        canvas.create_text(cx, cy - 255, text=f"ID: #{mi_id}", font=("Arial", 11, "bold"), fill="#00BCD4")
        
        self.lbl_foto = tk.Label(self.root, text="[ SIN FOTO DE PERFIL ]", bg="#1a1a1a", fg="#666666", font=("Arial", 9), width=18, height=6)
        self.cargar_foto_ui()

        btn_foto = tk.Button(self.root, text="Cambiar Foto de Perfil", bg="#FF9800", fg="#000000", font=("Arial", 11, "bold"),
                             command=self.pantalla_foto, width=22, bd=0)
        
        btn_chat = tk.Button(self.root, text="Chat Global en Vivo", bg="#9C27B0", fg="#FFFFFF", font=("Arial", 11, "bold"),
                             command=self.pantalla_chat, width=22, bd=0)
        
        btn_amigos = tk.Button(self.root, text="Agregar por ID", bg="#00BCD4", fg="#000000", font=("Arial", 11, "bold"),
                               command=self.pantalla_agregar_amigos, width=22, bd=0)
        
        btn_logout = tk.Button(self.root, text="Cerrar Sesión", bg="#f44336", fg="#FFFFFF", font=("Arial", 10, "bold"),
                               command=self.pantalla_login, width=16, bd=0)

        canvas.create_window(cx, cy - 170, window=self.lbl_foto)
        canvas.create_window(cx, cy - 60, window=btn_foto)
        canvas.create_window(cx, cy + 20, window=btn_chat)
        canvas.create_window(cx, cy + 100, window=btn_amigos)
        canvas.create_window(cx, cy + 200, window=btn_logout)

    # ==========================================
    # 4. AGREGAR CONTACTO
    # ==========================================
    def pantalla_agregar_amigos(self):
        self.limpiar_pantalla()
        
        canvas = tk.Canvas(self.root, width=self.ancho, height=self.alto, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cx = self.ancho // 2
        cy = self.alto // 2

        canvas.create_text(cx, cy - 280, text="RED DE OPERATIVOS DEDSEC", font=("Consolas", 16, "bold"), fill="#00BCD4")
        
        lbl_buscar = tk.Label(self.root, text="Ingresa el ID del usuario (6 dígitos):", font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#0a0a0a")
        ent_buscar = tk.Entry(self.root, font=("Arial", 12), bg="#1a1a1a", fg="#00BCD4", insertbackground="white", bd=1, width=22)
        
        btn_add = tk.Button(self.root, text="+ Agregar por ID", bg="#00BCD4", fg="#000000", font=("Arial", 10, "bold"),
                            command=lambda: self.agregar_contacto_por_id(ent_buscar.get()), width=18, bd=0)

        canvas.create_text(cx, cy + 20, text="Mis Contactos Registrados:", font=("Arial", 10, "bold"), fill="#888888")
        
        lst_amigos = tk.Listbox(self.root, bg="#121212", fg="#00FF66", font=("Arial", 10), width=34, height=5, bd=1)
        
        usuarios = cargar_usuarios()
        mis_amigos = usuarios.get(self.usuario_actual, {}).get("amigos", [])
        if mis_amigos:
            for amigo_info in mis_amigos:
                lst_amigos.insert("end", f"  • {amigo_info}")
        else:
            lst_amigos.insert("end", "  (No has agregado contactos aún)")

        btn_back = tk.Button(self.root, text="<- Volver al Menú", bg="#0a0a0a", fg="#00FF66", font=("Arial", 10, "underline"),
                             command=self.pantalla_menu_principal, bd=0)

        canvas.create_window(cx, cy - 220, window=lbl_buscar)
        canvas.create_window(cx, cy - 180, window=ent_buscar)
        canvas.create_window(cx, cy - 120, window=btn_add)
        canvas.create_window(cx, cy + 90, window=lst_amigos)
        canvas.create_window(cx, cy + 200, window=btn_back)

    def agregar_contacto_por_id(self, id_ingresado):
        id_ingresado = id_ingresado.strip().replace("#", "")
        if not id_ingresado:
            messagebox.showwarning("Atención", "Escribe el ID de 6 dígitos.")
            return

        usuarios = cargar_usuarios()
        mi_id = usuarios.get(self.usuario_actual, {}).get("id_unico")

        if id_ingresado == mi_id:
            messagebox.showwarning("Atención", "No puedes agregarte a ti mismo.")
            return

        usuario_encontrado = None
        for u, datos in usuarios.items():
            if isinstance(datos, dict) and datos.get("id_unico") == id_ingresado:
                usuario_encontrado = u
                break

        if not usuario_encontrado:
            messagebox.showerror("Error", f"No existe ningún usuario con el ID #{id_ingresado}")
            return

        contacto_formato = f"{usuario_encontrado.upper()} (#{id_ingresado})"
        mis_amigos = usuarios[self.usuario_actual].get("amigos", [])
        
        if contacto_formato in mis_amigos:
            messagebox.showinfo("Información", f"'{usuario_encontrado}' ya está en tus contactos.")
            return

        mis_amigos.append(contacto_formato)
        usuarios[self.usuario_actual]["amigos"] = mis_amigos
        guardar_usuarios(usuarios)

        messagebox.showinfo("Éxito", f"¡Se agregó a {usuario_encontrado} (#{id_ingresado}) a tus contactos!")
        self.pantalla_agregar_amigos()

    # ==========================================
    # 5. CHAT
    # ==========================================
    def pantalla_chat(self):
        self.limpiar_pantalla()
        
        canvas = tk.Canvas(self.root, width=self.ancho, height=self.alto, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        cx = self.ancho // 2
        cy = self.alto // 2

        canvas.create_text(cx, cy - 280, text="CHAT DEDSEC EN VIVO", font=("Consolas", 18, "bold"), fill="#9C27B0")
        
        txt_chat = tk.Text(self.root, bg="#121212", fg="#00FF66", font=("Arial", 10), width=42, height=9, bd=1)
        txt_chat.insert("end", "[SISTEMA]: Canal encriptado DedSec activo.\n")
        txt_chat.config(state="disabled")
        
        ent_msg = tk.Entry(self.root, font=("Arial", 11), bg="#1a1a1a", fg="#FFFFFF", insertbackground="white", bd=1, width=28)
        
        btn_send = tk.Button(self.root, text="Enviar ->", bg="#9C27B0", fg="#FFFFFF", font=("Arial", 10, "bold"),
                             command=lambda: self.enviar_mensaje(txt_chat, ent_msg), bd=0)
        
        btn_back = tk.Button(self.root, text="<- Volver al Menú", bg="#0a0a0a", fg="#00FF66", font=("Arial", 10, "underline"),
                             command=self.pantalla_menu_principal, bd=0)

        canvas.create_window(cx, cy - 110, window=txt_chat)
        canvas.create_window(cx - 45, cy + 60, window=ent_msg)
        canvas.create_window(cx + 145, cy + 60, window=btn_send)
        canvas.create_window(cx, cy + 160, window=btn_back)

    def enviar_mensaje(self, txt_widget, ent_widget):
        mensaje = ent_widget.get().strip()
        if mensaje:
            txt_widget.config(state="normal")
            txt_widget.insert("end", f"{self.usuario_actual}: {mensaje}\n")
            txt_widget.config(state="disabled")
            txt_widget.see("end")
            ent_widget.delete(0, "end")

    def pantalla_foto(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar foto de perfil",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            usuarios = cargar_usuarios()
            usuarios[self.usuario_actual]["foto"] = file_path
            guardar_usuarios(usuarios)
            messagebox.showinfo("DedSec", "¡Foto de perfil actualizada!")
            self.pantalla_menu_principal()

    def cargar_foto_ui(self):
        usuarios = cargar_usuarios()
        ruta_foto = usuarios.get(self.usuario_actual, {}).get("foto")
        
        if ruta_foto and os.path.exists(ruta_foto):
            try:
                img = Image.open(ruta_foto)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                self.foto_img_tk = ImageTk.PhotoImage(img)
                self.lbl_foto.config(image=self.foto_img_tk, text="", width=120, height=120)
            except Exception:
                self.lbl_foto.config(text="Error al cargar foto")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
          
