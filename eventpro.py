import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ═══════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════
DB_CONFIG = {"host": "localhost", "user": "root", "password": "", "port": 3306, "database": "eventpro"}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def call_sp(sp_name, params=()):
    """Ejecuta un SP que no retorna filas (INSERT, UPDATE, DELETE)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.callproc(sp_name, params)
    conn.commit()
    cur.close()
    conn.close()

def call_sp_fetch(sp_name, params=()):
    """Ejecuta un SP que retorna filas (SELECT)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.callproc(sp_name, params)
    rows = []
    for result in cur.stored_results():
        rows = result.fetchall()
    cur.close()
    conn.close()
    return rows

# ═══════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
root = tk.Tk()
root.geometry('900x620')
root.title("EventPro – Espacios Magníficos S.A.")

nb = ttk.Notebook(root)
tab1=ttk.Frame(nb); tab2=ttk.Frame(nb); tab3=ttk.Frame(nb); tab4=ttk.Frame(nb)
nb.add(tab1, text="Recintos")
nb.add(tab2, text="Clientes")
nb.add(tab3, text="Eventos")
nb.add(tab4, text="Personal")
nb.pack(expand=True, fill="both")

FT=("Arial",16,"bold"); FL=("Arial",12); FE=("Arial",12); FB=("Arial",12)

# ─── placeholder helpers ──────────────────────────────────────────
def add_ph(e, ph):
    e._ph = ph
    e.insert(0, ph)
    e.config(fg="gray")
    e.bind("<FocusIn>",  lambda _: (e.delete(0,tk.END), e.config(fg="black")) if e.get()==ph else None)
    e.bind("<FocusOut>", lambda _: (e.insert(0,ph), e.config(fg="gray")) if e.get()=="" else None)

def gv(e):
    return "" if e.get()==getattr(e,"_ph","") else e.get()

def sv(e, v):
    e.delete(0, tk.END)
    if v:
        e.insert(0, v)
        e.config(fg="black")
    else:
        e.insert(0, getattr(e,"_ph",""))
        e.config(fg="gray")

def cv(e): sv(e, "")

# ─── widget builders ──────────────────────────────────────────────
def mke(parent, ph, row, col=1, w=30):
    e = tk.Entry(parent, width=w, font=FE, relief="solid", bd=1)
    e.grid(row=row, column=col, sticky="w", pady=8)
    add_ph(e, ph)
    return e

def mkl(parent, txt, row, col=0):
    tk.Label(parent, text=txt, font=FL).grid(row=row, column=col, sticky="w", padx=(0,10), pady=8)

def mkc(parent, vals, row, col=1, w=28):
    cb = ttk.Combobox(parent, values=vals, width=w, font=FE, state="readonly")
    cb.set(vals[0])
    cb.grid(row=row, column=col, sticky="w", pady=8)
    return cb

def mksearch(parent, color, fn):
    sf = tk.Frame(parent, bd=1, relief="groove", bg="#f0f0f0")
    sf.pack(fill="x", padx=50, pady=(6,0))
    tk.Label(sf, text="Buscar:", font=("Arial",11,"bold"), fg=color, bg="#f0f0f0").pack(side=tk.LEFT, padx=(10,4), pady=6)
    se = tk.Entry(sf, width=26, font=("Arial",11), relief="solid", bd=1)
    se.pack(side=tk.LEFT, padx=4, pady=6)
    add_ph(se, "Código o nombre...")
    tk.Button(sf, text="Buscar", font=("Arial",10,"bold"), bg=color, fg="white",
              relief="flat", padx=10, cursor="hand2",
              command=lambda: fn(gv(se))).pack(side=tk.LEFT, padx=6, pady=6)
    tk.Button(sf, text="Limpiar búsqueda", font=("Arial",10), bg="#9E9E9E", fg="white",
              relief="flat", padx=8, cursor="hand2",
              command=lambda: sv(se,"")).pack(side=tk.LEFT, padx=2, pady=6)

def mkbtns(parent, fs, fu, fd, fc):
    bf = tk.Frame(parent)
    bf.pack(pady=14)
    for txt, col, fn in [("Guardar","#4CAF50",fs), ("Actualizar","#2196F3",fu),
                          ("Eliminar","#f44336",fd), ("Limpiar","#FF9800",fc)]:
        tk.Button(bf, text=txt, font=FB, bg=col, fg="white", activebackground=col,
                  relief="flat", width=10, cursor="hand2", command=fn).pack(side=tk.LEFT, padx=5)

# ═══════════════════════════════════════════════════════════════════
#  TAB 1 – RECINTOS
# ═══════════════════════════════════════════════════════════════════
tk.Label(tab1, text="FORMULARIO DE RECINTOS", font=FT, fg="blue").pack(pady=(14,4))

def sr(t):
    if not t: return
    try:
        rows = call_sp_fetch("sp_buscar_recinto", (t,))
        if rows:
            r = rows[0]
            sv(r_cod, r[0]); sv(r_nom, r[1])
            r_tip.set(r[2] if r[2] in r_tip["values"] else r_tip["values"][0])
            sv(r_ubi, r[3]); sv(r_cap, str(r[4]) if r[4] else ""); sv(r_tar, r[5])
            r_dis.set(r[6] if r[6] in r_dis["values"] else r_dis["values"][0])
        else:
            messagebox.showinfo("Buscar", "No se encontró ningún recinto.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

mksearch(tab1, "blue", sr)
ff1 = tk.Frame(tab1); ff1.pack(pady=6, anchor="w", padx=50)
mkl(ff1,"Código Recinto:",0);     r_cod=mke(ff1,"Ej: RC-001",0)
mkl(ff1,"Nombre:",1);             r_nom=mke(ff1,"Ej: Salón Imperial",1)
mkl(ff1,"Tipo de Recinto:",2);    r_tip=mkc(ff1,["— Seleccionar —","Salón","Auditorio","Sala de reuniones"],2)
mkl(ff1,"Ubicación:",3);          r_ubi=mke(ff1,"Ej: Ala Norte, Piso 2",3)
mkl(ff1,"Capacidad (teatro):",4); r_cap=mke(ff1,"Ej: 500",4)
mkl(ff1,"Tarifa:",5);             r_tar=mke(ff1,"Ej: $350.000/hora",5)
mkl(ff1,"Disponibilidad:",6);     r_dis=mkc(ff1,["— Seleccionar —","Disponible","Reservado","En mantenimiento"],6)

def r_save():
    v = (gv(r_cod), gv(r_nom), r_tip.get(), gv(r_ubi), gv(r_cap) or None, gv(r_tar), r_dis.get())
    if not v[0] or not v[1]: messagebox.showwarning("Guardar","Código y Nombre son obligatorios."); return
    try:
        call_sp("sp_insertar_recinto", v)
        messagebox.showinfo("Guardar","Recinto guardado ✔")
    except mysql.connector.IntegrityError: messagebox.showerror("Error","Código ya existe.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def r_upd():
    cod = gv(r_cod)
    if not cod: messagebox.showwarning("Actualizar","Ingresa el código."); return
    try:
        call_sp("sp_actualizar_recinto", (cod, gv(r_nom), r_tip.get(), gv(r_ubi), gv(r_cap) or None, gv(r_tar), r_dis.get()))
        messagebox.showinfo("Actualizar","Recinto actualizado ✔")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def r_del():
    cod = gv(r_cod)
    if not cod: messagebox.showwarning("Eliminar","Ingresa el código."); return
    if not messagebox.askyesno("Eliminar", f"¿Eliminar recinto {cod}?"): return
    try:
        call_sp("sp_eliminar_recinto", (cod,))
        messagebox.showinfo("Eliminar","Recinto eliminado ✔"); r_clr()
    except Exception as ex: messagebox.showerror("Error", str(ex))

def r_clr():
    for e in [r_cod,r_nom,r_ubi,r_cap,r_tar]: cv(e)
    r_tip.set(r_tip["values"][0]); r_dis.set(r_dis["values"][0])

mkbtns(tab1, r_save, r_upd, r_del, r_clr)

# ═══════════════════════════════════════════════════════════════════
#  TAB 2 – CLIENTES
# ═══════════════════════════════════════════════════════════════════
tk.Label(tab2, text="FORMULARIO DE CLIENTES", font=FT, fg="green").pack(pady=(14,4))

def sc(t):
    if not t: return
    try:
        rows = call_sp_fetch("sp_buscar_cliente", (t,))
        if rows:
            r = rows[0]
            sv(c_cod, r[0])
            c_tip.set(r[1] if r[1] in c_tip["values"] else c_tip["values"][0])
            sv(c_raz, r[2]); sv(c_doc, r[3]); sv(c_tel, r[4]); sv(c_mail, r[5]); sv(c_con, r[6])
            c_cla.set(r[7] if r[7] in c_cla["values"] else c_cla["values"][0])
        else:
            messagebox.showinfo("Buscar","No se encontró ningún cliente.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

mksearch(tab2, "green", sc)
ff2 = tk.Frame(tab2); ff2.pack(pady=6, anchor="w", padx=50)
mkl(ff2,"Código Cliente:",0);        c_cod=mke(ff2,"Ej: CL-001",0)
mkl(ff2,"Tipo de Cliente:",1);       c_tip=mkc(ff2,["— Seleccionar —","Corporativo","Agencia","Particular"],1)
mkl(ff2,"Razón Social / Nombre:",2); c_raz=mke(ff2,"Ej: Tech Summit S.A.",2)
mkl(ff2,"Documento Fiscal:",3);      c_doc=mke(ff2,"NIT / RUT / Cédula",3)
mkl(ff2,"Teléfono:",4);              c_tel=mke(ff2,"Ej: +57 300 123 4567",4)
mkl(ff2,"Correo Electrónico:",5);    c_mail=mke(ff2,"contacto@empresa.com",5)
mkl(ff2,"Persona de Contacto:",6);   c_con=mke(ff2,"Nombre completo",6)
mkl(ff2,"Clasificación:",7);         c_cla=mkc(ff2,["— Seleccionar —","Cliente nuevo","Cliente frecuente","Cliente VIP"],7)

def c_save():
    v = (gv(c_cod), c_tip.get(), gv(c_raz), gv(c_doc), gv(c_tel), gv(c_mail), gv(c_con), c_cla.get())
    if not v[0] or not v[2]: messagebox.showwarning("Guardar","Código y Razón Social son obligatorios."); return
    try:
        call_sp("sp_insertar_cliente", v)
        messagebox.showinfo("Guardar","Cliente guardado ✔")
    except mysql.connector.IntegrityError: messagebox.showerror("Error","Código ya existe.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def c_upd():
    cod = gv(c_cod)
    if not cod: messagebox.showwarning("Actualizar","Ingresa el código."); return
    try:
        call_sp("sp_actualizar_cliente", (cod, c_tip.get(), gv(c_raz), gv(c_doc), gv(c_tel), gv(c_mail), gv(c_con), c_cla.get()))
        messagebox.showinfo("Actualizar","Cliente actualizado ✔")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def c_del():
    cod = gv(c_cod)
    if not cod: messagebox.showwarning("Eliminar","Ingresa el código."); return
    if not messagebox.askyesno("Eliminar", f"¿Eliminar cliente {cod}?"): return
    try:
        call_sp("sp_eliminar_cliente", (cod,))
        messagebox.showinfo("Eliminar","Cliente eliminado ✔"); c_clr()
    except Exception as ex: messagebox.showerror("Error", str(ex))

def c_clr():
    for e in [c_cod,c_raz,c_doc,c_tel,c_mail,c_con]: cv(e)
    c_tip.set(c_tip["values"][0]); c_cla.set(c_cla["values"][0])

mkbtns(tab2, c_save, c_upd, c_del, c_clr)

# ═══════════════════════════════════════════════════════════════════
#  TAB 3 – EVENTOS
# ═══════════════════════════════════════════════════════════════════
tk.Label(tab3, text="FORMULARIO DE EVENTOS", font=FT, fg="purple").pack(pady=(14,4))

def se(t):
    if not t: return
    try:
        rows = call_sp_fetch("sp_buscar_evento", (t,))
        if rows:
            r = rows[0]
            sv(e_num, r[0]); sv(e_tit, r[1])
            e_tip.set(r[2] if r[2] in e_tip["values"] else e_tip["values"][0])
            sv(e_cli, r[3]); sv(e_fi, r[4]); sv(e_ff, r[5])
            sv(e_asi, str(r[6]) if r[6] else "")
            e_est.set(r[7] if r[7] in e_est["values"] else e_est["values"][0])
        else:
            messagebox.showinfo("Buscar","No se encontró ningún evento.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

mksearch(tab3, "purple", se)
ff3 = tk.Frame(tab3); ff3.pack(pady=6, anchor="w", padx=50)
mkl(ff3,"N° Evento:",0);           e_num=mke(ff3,"Ej: EV-2026-001",0)
mkl(ff3,"Título:",1);              e_tit=mke(ff3,"Ej: Cumbre Tecnológica",1)
mkl(ff3,"Tipo de Evento:",2);      e_tip=mkc(ff3,["— Seleccionar —","Congreso","Boda","Feria","Concierto","Conferencia"],2)
mkl(ff3,"Cliente:",3);             e_cli=mke(ff3,"Código o nombre del cliente",3)
mkl(ff3,"Fecha Inicio:",4);        e_fi=mke(ff3,"AAAA-MM-DD  HH:MM",4)
mkl(ff3,"Fecha Fin:",5);           e_ff=mke(ff3,"AAAA-MM-DD  HH:MM",5)
mkl(ff3,"N° Asistentes Est.:",6);  e_asi=mke(ff3,"Ej: 250",6)
mkl(ff3,"Estado Actual:",7);       e_est=mkc(ff3,["— Seleccionar —","Cotización","Confirmado","En curso","Finalizado","Cancelado"],7)

def ev_save():
    v = (gv(e_num), gv(e_tit), e_tip.get(), gv(e_cli), gv(e_fi), gv(e_ff), gv(e_asi) or None, e_est.get())
    if not v[0] or not v[1]: messagebox.showwarning("Guardar","N° y Título son obligatorios."); return
    try:
        call_sp("sp_insertar_evento", v)
        messagebox.showinfo("Guardar","Evento guardado ✔")
    except mysql.connector.IntegrityError: messagebox.showerror("Error","N° de evento ya existe.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def ev_upd():
    num = gv(e_num)
    if not num: messagebox.showwarning("Actualizar","Ingresa el N° de evento."); return
    try:
        call_sp("sp_actualizar_evento", (num, gv(e_tit), e_tip.get(), gv(e_cli), gv(e_fi), gv(e_ff), gv(e_asi) or None, e_est.get()))
        messagebox.showinfo("Actualizar","Evento actualizado ✔")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def ev_del():
    num = gv(e_num)
    if not num: messagebox.showwarning("Eliminar","Ingresa el N° de evento."); return
    if not messagebox.askyesno("Eliminar", f"¿Eliminar evento {num}?"): return
    try:
        call_sp("sp_eliminar_evento", (num,))
        messagebox.showinfo("Eliminar","Evento eliminado ✔"); ev_clr()
    except Exception as ex: messagebox.showerror("Error", str(ex))

def ev_clr():
    for e in [e_num,e_tit,e_cli,e_fi,e_ff,e_asi]: cv(e)
    e_tip.set(e_tip["values"][0]); e_est.set(e_est["values"][0])

mkbtns(tab3, ev_save, ev_upd, ev_del, ev_clr)

# ═══════════════════════════════════════════════════════════════════
#  TAB 4 – PERSONAL
# ═══════════════════════════════════════════════════════════════════
tk.Label(tab4, text="FORMULARIO DE PERSONAL", font=FT, fg="red").pack(pady=(14,4))

def sp(t):
    if not t: return
    try:
        rows = call_sp_fetch("sp_buscar_personal", (t,))
        if rows:
            r = rows[0]
            sv(p_cod, r[0]); sv(p_nom, r[1]); sv(p_ape, r[2])
            p_esp.set(r[3] if r[3] in p_esp["values"] else p_esp["values"][0])
            sv(p_tar, r[4]); sv(p_evt, r[5]); sv(p_hor, r[6])
            p_dis.set(r[7] if r[7] in p_dis["values"] else p_dis["values"][0])
        else:
            messagebox.showinfo("Buscar","No se encontró ningún empleado.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

mksearch(tab4, "red", sp)
ff4 = tk.Frame(tab4); ff4.pack(pady=6, anchor="w", padx=50)
mkl(ff4,"Código Empleado:",0);  p_cod=mke(ff4,"Ej: EP-001",0)
mkl(ff4,"Nombres:",1);          p_nom=mke(ff4,"Nombres del empleado",1)
mkl(ff4,"Apellidos:",2);        p_ape=mke(ff4,"Apellidos del empleado",2)
mkl(ff4,"Especialidad:",3);     p_esp=mkc(ff4,["— Seleccionar —","Coordinador","Técnico audiovisual","Camarero","Seguridad","Decorador","Chef"],3)
mkl(ff4,"Tarifa Aplicable:",4); p_tar=mke(ff4,"Ej: $45.000/hora",4)
mkl(ff4,"Evento Asignado:",5);  p_evt=mke(ff4,"N° o nombre del evento",5)
mkl(ff4,"Horario Asignado:",6); p_hor=mke(ff4,"Ej: 08:00 – 18:00",6)
mkl(ff4,"Disponibilidad:",7);   p_dis=mkc(ff4,["— Seleccionar —","Disponible","Asignado","De vacaciones","Baja médica"],7)

def p_save():
    v = (gv(p_cod), gv(p_nom), gv(p_ape), p_esp.get(), gv(p_tar), gv(p_evt), gv(p_hor), p_dis.get())
    if not v[0] or not v[1]: messagebox.showwarning("Guardar","Código y Nombres son obligatorios."); return
    try:
        call_sp("sp_insertar_personal", v)
        messagebox.showinfo("Guardar","Empleado guardado ✔")
    except mysql.connector.IntegrityError: messagebox.showerror("Error","Código ya existe.")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def p_upd():
    cod = gv(p_cod)
    if not cod: messagebox.showwarning("Actualizar","Ingresa el código."); return
    try:
        call_sp("sp_actualizar_personal", (cod, gv(p_nom), gv(p_ape), p_esp.get(), gv(p_tar), gv(p_evt), gv(p_hor), p_dis.get()))
        messagebox.showinfo("Actualizar","Empleado actualizado ✔")
    except Exception as ex: messagebox.showerror("Error", str(ex))

def p_del():
    cod = gv(p_cod)
    if not cod: messagebox.showwarning("Eliminar","Ingresa el código."); return
    if not messagebox.askyesno("Eliminar", f"¿Eliminar empleado {cod}?"): return
    try:
        call_sp("sp_eliminar_personal", (cod,))
        messagebox.showinfo("Eliminar","Empleado eliminado ✔"); p_clr()
    except Exception as ex: messagebox.showerror("Error", str(ex))

def p_clr():
    for e in [p_cod,p_nom,p_ape,p_tar,p_evt,p_hor]: cv(e)
    p_esp.set(p_esp["values"][0]); p_dis.set(p_dis["values"][0])

mkbtns(tab4, p_save, p_upd, p_del, p_clr)

# ═══════════════════════════════════════════════════════════════════
#  ARRANQUE
# ═══════════════════════════════════════════════════════════════════
try:
    get_conn()
except Exception as err:
    messagebox.showerror("Error de conexión",
        f"No se pudo conectar a MySQL.\n\n{err}\n\n"
        "Verifica que WAMP esté corriendo.")

root.mainloop()