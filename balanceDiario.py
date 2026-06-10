"""
Balance Diario - Gestor de ingresos y gastos
=============================================
Aplicación de escritorio hecha con Python y Tkinter.
Guarda los datos en un archivo JSON local.

Autor: Tu nombre
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ─── Archivo donde se guardan los datos ───────────────────────────────────────
ARCHIVO_DATOS = "mis_finanzas.json"


# ─── Funciones para cargar y guardar datos ────────────────────────────────────

def cargar_datos():
    """Lee el archivo JSON y devuelve los datos. Si no existe, devuelve lista vacía."""
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_datos(datos):
    """Guarda la lista de transacciones en el archivo JSON."""
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


# ─── Clase principal de la aplicación ─────────────────────────────────────────

class AppFinanzas:
    def __init__(self, ventana_raiz):
        self.root = ventana_raiz
        self.root.title("💰 Balance Diario")
        self.root.geometry("820x620")
        self.root.configure(bg="#1C1C2E")
        self.root.resizable(True, True)

        # Cargamos los datos al iniciar
        self.transacciones = cargar_datos()

        self._construir_interfaz()
        self._actualizar_tabla()
        self._actualizar_resumen()

    # ── Construcción de la interfaz ───────────────────────────────────────────

    def _construir_interfaz(self):
        """Crea todos los widgets de la ventana."""

        # ── Paleta de colores ──
        self.color_fondo      = "#1C1C2E"
        self.color_panel      = "#2A2A40"
        self.color_acento     = "#7C3AED"   # violeta
        self.color_ingreso    = "#10B981"   # verde esmeralda
        self.color_gasto      = "#EF4444"   # rojo
        self.color_texto      = "#E2E8F0"
        self.color_subtexto   = "#94A3B8"
        self.color_entrada    = "#3B3B58"

        # ── Título ──
        frame_titulo = tk.Frame(self.root, bg=self.color_fondo, pady=14)
        frame_titulo.pack(fill="x", padx=20)

        tk.Label(
            frame_titulo, text="💰 Balance Diario",
            font=("Segoe UI", 20, "bold"),
            bg=self.color_fondo, fg=self.color_texto
        ).pack(side="left")

        tk.Label(
            frame_titulo, text="Control de ingresos y gastos",
            font=("Segoe UI", 10),
            bg=self.color_fondo, fg=self.color_subtexto
        ).pack(side="left", padx=12, pady=6)

        # ── Contenedor principal (izquierda + derecha) ──
        contenedor = tk.Frame(self.root, bg=self.color_fondo)
        contenedor.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self._construir_panel_formulario(contenedor)
        self._construir_panel_tabla(contenedor)

        # ── Barra de resumen abajo ──
        self._construir_barra_resumen()

    def _construir_panel_formulario(self, padre):
        """Panel izquierdo: formulario para añadir una transacción."""
        frame = tk.Frame(padre, bg=self.color_panel, bd=0, padx=20, pady=20)
        frame.pack(side="left", fill="y", padx=(0, 12), pady=0)

        tk.Label(
            frame, text="Nueva transacción",
            font=("Segoe UI", 13, "bold"),
            bg=self.color_panel, fg=self.color_texto
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        # ── Campo: Descripción ──
        self._etiqueta(frame, "Descripción", 1)
        self.entrada_descripcion = self._entrada(frame, 2, "Ej: Supermercado")

        # ── Campo: Importe ──
        self._etiqueta(frame, "Importe (€)", 3)
        self.entrada_importe = self._entrada(frame, 4, "Ej: 45.50")

        # ── Campo: Tipo ──
        self._etiqueta(frame, "Tipo", 5)
        self.tipo_var = tk.StringVar(value="Gasto")
        frame_tipo = tk.Frame(frame, bg=self.color_panel)
        frame_tipo.grid(row=6, column=0, columnspan=2, sticky="ew", pady=4)

        for texto, valor in [("📉 Gasto", "Gasto"), ("📈 Ingreso", "Ingreso")]:
            tk.Radiobutton(
                frame_tipo, text=texto, variable=self.tipo_var, value=valor,
                bg=self.color_panel, fg=self.color_texto,
                selectcolor=self.color_acento,
                activebackground=self.color_panel,
                font=("Segoe UI", 10), pady=4
            ).pack(side="left", padx=(0, 12))

        # ── Campo: Fecha ──
        self._etiqueta(frame, "Fecha (DD/MM/AAAA)", 7)
        self.entrada_fecha = self._entrada(frame, 8, "")
        self.entrada_fecha.insert(0, datetime.today().strftime("%d/%m/%Y"))

        # ── Botón añadir ──
        tk.Button(
            frame, text="＋ Añadir",
            font=("Segoe UI", 11, "bold"),
            bg=self.color_acento, fg="white",
            activebackground="#6D28D9",
            relief="flat", cursor="hand2",
            padx=10, pady=8,
            command=self._anadir_transaccion
        ).grid(row=9, column=0, columnspan=2, sticky="ew", pady=(16, 4))

        # ── Botón eliminar seleccionado ──
        tk.Button(
            frame, text="🗑 Eliminar seleccionado",
            font=("Segoe UI", 10),
            bg=self.color_entrada, fg=self.color_subtexto,
            activebackground="#4A4A6A",
            relief="flat", cursor="hand2",
            padx=10, pady=6,
            command=self._eliminar_transaccion
        ).grid(row=10, column=0, columnspan=2, sticky="ew", pady=4)

    def _construir_panel_tabla(self, padre):
        """Panel derecho: tabla con todas las transacciones y filtros."""
        frame = tk.Frame(padre, bg=self.color_panel, padx=14, pady=14)
        frame.pack(side="left", fill="both", expand=True)

        # ── Cabecera con filtro ──
        cabecera = tk.Frame(frame, bg=self.color_panel)
        cabecera.pack(fill="x", pady=(0, 10))

        tk.Label(
            cabecera, text="Movimientos",
            font=("Segoe UI", 13, "bold"),
            bg=self.color_panel, fg=self.color_texto
        ).pack(side="left")

        # Filtro por mes
        tk.Label(
            cabecera, text="Filtrar mes (MM/AAAA):",
            font=("Segoe UI", 9),
            bg=self.color_panel, fg=self.color_subtexto
        ).pack(side="left", padx=(20, 4))

        self.filtro_mes = tk.StringVar()
        entrada_filtro = tk.Entry(
            cabecera, textvariable=self.filtro_mes,
            font=("Segoe UI", 10), width=9,
            bg=self.color_entrada, fg=self.color_texto,
            insertbackground=self.color_texto, relief="flat",
            bd=4
        )
        entrada_filtro.pack(side="left")
        self.filtro_mes.trace_add("write", lambda *_: self._actualizar_tabla())

        tk.Button(
            cabecera, text="✕ Limpiar",
            font=("Segoe UI", 9),
            bg=self.color_entrada, fg=self.color_subtexto,
            relief="flat", cursor="hand2", padx=6,
            command=lambda: self.filtro_mes.set("")
        ).pack(side="left", padx=4)

        # ── Tabla (Treeview) ──
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Finanzas.Treeview",
            background=self.color_panel,
            foreground=self.color_texto,
            rowheight=28,
            fieldbackground=self.color_panel,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        estilo.configure(
            "Finanzas.Treeview.Heading",
            background=self.color_acento,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        estilo.map("Finanzas.Treeview", background=[("selected", "#4C1D95")])

        columnas = ("fecha", "descripcion", "tipo", "importe")
        self.tabla = ttk.Treeview(
            frame, columns=columnas, show="headings",
            style="Finanzas.Treeview", selectmode="browse"
        )

        # Cabeceras y anchos
        self.tabla.heading("fecha",       text="📅 Fecha")
        self.tabla.heading("descripcion", text="📝 Descripción")
        self.tabla.heading("tipo",        text="Tipo")
        self.tabla.heading("importe",     text="Importe")

        self.tabla.column("fecha",       width=100, anchor="center")
        self.tabla.column("descripcion", width=220, anchor="w")
        self.tabla.column("tipo",        width=90,  anchor="center")
        self.tabla.column("importe",     width=100, anchor="e")

        # Colores alternos para filas
        self.tabla.tag_configure("ingreso", foreground=self.color_ingreso)
        self.tabla.tag_configure("gasto",   foreground=self.color_gasto)

        # Barra de scroll
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _construir_barra_resumen(self):
        """Barra inferior con totales: ingresos, gastos y balance."""
        frame = tk.Frame(self.root, bg=self.color_panel, pady=14)
        frame.pack(fill="x", padx=20, pady=(0, 16))

        # Ingresos
        bloque_ing = tk.Frame(frame, bg=self.color_panel)
        bloque_ing.pack(side="left", expand=True)
        tk.Label(bloque_ing, text="INGRESOS TOTALES", font=("Segoe UI", 8),
                 bg=self.color_panel, fg=self.color_subtexto).pack()
        self.lbl_ingresos = tk.Label(bloque_ing, text="0,00 €",
                                     font=("Segoe UI", 16, "bold"),
                                     bg=self.color_panel, fg=self.color_ingreso)
        self.lbl_ingresos.pack()

        # Separador
        tk.Frame(frame, bg="#3B3B58", width=1).pack(side="left", fill="y", padx=20, pady=6)

        # Gastos
        bloque_gas = tk.Frame(frame, bg=self.color_panel)
        bloque_gas.pack(side="left", expand=True)
        tk.Label(bloque_gas, text="GASTOS TOTALES", font=("Segoe UI", 8),
                 bg=self.color_panel, fg=self.color_subtexto).pack()
        self.lbl_gastos = tk.Label(bloque_gas, text="0,00 €",
                                   font=("Segoe UI", 16, "bold"),
                                   bg=self.color_panel, fg=self.color_gasto)
        self.lbl_gastos.pack()

        # Separador
        tk.Frame(frame, bg="#3B3B58", width=1).pack(side="left", fill="y", padx=20, pady=6)

        # Balance
        bloque_bal = tk.Frame(frame, bg=self.color_panel)
        bloque_bal.pack(side="left", expand=True)
        tk.Label(bloque_bal, text="BALANCE", font=("Segoe UI", 8),
                 bg=self.color_panel, fg=self.color_subtexto).pack()
        self.lbl_balance = tk.Label(bloque_bal, text="0,00 €",
                                    font=("Segoe UI", 16, "bold"),
                                    bg=self.color_panel, fg=self.color_texto)
        self.lbl_balance.pack()

    # ── Funciones de ayuda para crear widgets ────────────────────────────────

    def _etiqueta(self, padre, texto, fila):
        tk.Label(
            padre, text=texto, font=("Segoe UI", 9),
            bg=self.color_panel, fg=self.color_subtexto
        ).grid(row=fila, column=0, columnspan=2, sticky="w", pady=(8, 2))

    def _entrada(self, padre, fila, placeholder):
        entrada = tk.Entry(
            padre, font=("Segoe UI", 11), width=22,
            bg=self.color_entrada, fg=self.color_texto,
            insertbackground=self.color_texto, relief="flat", bd=6
        )
        entrada.grid(row=fila, column=0, columnspan=2, sticky="ew", pady=2)
        if placeholder:
            entrada.insert(0, placeholder)
            entrada.config(fg=self.color_subtexto)
            entrada.bind("<FocusIn>",  lambda e: self._limpiar_placeholder(entrada, placeholder))
            entrada.bind("<FocusOut>", lambda e: self._restaurar_placeholder(entrada, placeholder))
        return entrada

    def _limpiar_placeholder(self, entrada, placeholder):
        if entrada.get() == placeholder:
            entrada.delete(0, "end")
            entrada.config(fg=self.color_texto)

    def _restaurar_placeholder(self, entrada, placeholder):
        if not entrada.get():
            entrada.insert(0, placeholder)
            entrada.config(fg=self.color_subtexto)

    # ── Lógica de negocio ─────────────────────────────────────────────────────

    def _anadir_transaccion(self):
        """Recoge los datos del formulario, valida y añade la transacción."""
        desc    = self.entrada_descripcion.get().strip()
        importe = self.entrada_importe.get().strip()
        tipo    = self.tipo_var.get()
        fecha   = self.entrada_fecha.get().strip()

        # Ignorar placeholders
        if desc in ("Ej: Supermercado", ""):
            messagebox.showwarning("Campo vacío", "Por favor escribe una descripción.")
            return
        if importe in ("Ej: 45.50", ""):
            messagebox.showwarning("Campo vacío", "Por favor escribe un importe.")
            return

        # Validar importe numérico
        importe_limpio = importe.replace(",", ".")
        try:
            valor = float(importe_limpio)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Importe inválido", "El importe debe ser un número positivo.\nEjemplo: 45.50")
            return

        # Validar fecha
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato DD/MM/AAAA.\nEjemplo: 15/06/2025")
            return

        # Crear y guardar la transacción
        nueva = {
            "fecha":       fecha,
            "descripcion": desc,
            "tipo":        tipo,
            "importe":     round(valor, 2)
        }
        self.transacciones.append(nueva)
        guardar_datos(self.transacciones)

        # Limpiar formulario
        self.entrada_descripcion.delete(0, "end")
        self.entrada_descripcion.insert(0, "Ej: Supermercado")
        self.entrada_descripcion.config(fg=self.color_subtexto)
        self.entrada_importe.delete(0, "end")
        self.entrada_importe.insert(0, "Ej: 45.50")
        self.entrada_importe.config(fg=self.color_subtexto)

        self._actualizar_tabla()
        self._actualizar_resumen()

    def _eliminar_transaccion(self):
        """Elimina la fila seleccionada en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Nada seleccionado", "Haz clic en una fila para seleccionarla primero.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar este movimiento?"):
            return

        # El iid de cada fila es su índice original en self.transacciones
        indice = int(self.tabla.item(seleccion[0])["values"][4])  # columna oculta con índice
        self.transacciones.pop(indice)
        guardar_datos(self.transacciones)

        self._actualizar_tabla()
        self._actualizar_resumen()

    def _actualizar_tabla(self, *_):
        """Recarga la tabla aplicando el filtro de mes si lo hay."""
        # Borrar filas actuales
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        filtro = self.filtro_mes.get().strip()

        for i, t in enumerate(self.transacciones):
            # Filtro por mes (MM/AAAA)
            if filtro and filtro not in t["fecha"][3:]:  # extrae MM/AAAA de DD/MM/AAAA
                continue

            signo   = "+" if t["tipo"] == "Ingreso" else "-"
            etiqueta = "ingreso" if t["tipo"] == "Ingreso" else "gasto"
            importe_fmt = f"{signo}{t['importe']:.2f} €"

            # Insertamos también el índice original como columna oculta
            self.tabla.insert(
                "", "end",
                values=(t["fecha"], t["descripcion"], t["tipo"], importe_fmt, i),
                tags=(etiqueta,)
            )

        # Ocultar la columna del índice
        self.tabla["displaycolumns"] = ("fecha", "descripcion", "tipo", "importe")

    def _actualizar_resumen(self):
        """Recalcula y muestra los totales en la barra inferior."""
        total_ing = sum(t["importe"] for t in self.transacciones if t["tipo"] == "Ingreso")
        total_gas = sum(t["importe"] for t in self.transacciones if t["tipo"] == "Gasto")
        balance   = total_ing - total_gas

        self.lbl_ingresos.config(text=f"{total_ing:,.2f} €".replace(",", "."))
        self.lbl_gastos.config(text=f"{total_gas:,.2f} €".replace(",", "."))

        color_balance = self.color_ingreso if balance >= 0 else self.color_gasto
        self.lbl_balance.config(
            text=f"{balance:+,.2f} €".replace(",", "."),
            fg=color_balance
        )


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = AppFinanzas(root)
    root.mainloop()
    