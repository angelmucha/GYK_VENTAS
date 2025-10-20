import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import sistema as sm
from datetime import date, datetime
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import pandas as pd
from tkinter import filedialog
import sys

import os


# Función para mostrar la interfaz de clientes en la misma ventana
def formulario_clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Agregar Nuevo Cliente")

    # Centrar la ventana

    centrar_ventana(ventana_clientes, 0.2, 0.25)
    ventana_clientes.resizable(False, False)
    # Etiquetas y campos para el formulario del cliente
    etiqueta_nombre = ttk.Label(ventana_clientes, text="Nombre:")
    etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5)
    campo_nombre = ttk.Entry(ventana_clientes)
    campo_nombre.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_dni = ttk.Label(ventana_clientes, text="DNI:")
    etiqueta_dni.grid(row=1, column=0, padx=10, pady=5)
    campo_dni = ttk.Entry(ventana_clientes)
    campo_dni.grid(row=1, column=1, padx=10, pady=5)

    etiqueta_telefono = ttk.Label(ventana_clientes, text="Teléfono:")
    etiqueta_telefono.grid(row=2, column=0, padx=10, pady=5)
    campo_telefono = ttk.Entry(ventana_clientes)
    campo_telefono.grid(row=2, column=1, padx=10, pady=5)


    etiqueta_direccion = ttk.Label(ventana_clientes, text="Dirección:")
    etiqueta_direccion.grid(row=3, column=0, padx=10, pady=5)
    campo_direccion = ttk.Entry(ventana_clientes)
    campo_direccion.grid(row=3, column=1, padx=10, pady=5)

    # Función para guardar el cliente
    def guardar_cliente():
        nombre = campo_nombre.get()
        direccion = campo_direccion.get()
        telefono = campo_telefono.get()
        dni = campo_dni.get()
        
        sm.agregar_cliente(nombre, direccion, telefono, dni)
        ventana_clientes.destroy()

    boton_guardar = ttk.Button(ventana_clientes, text="Guardar Cliente", command=guardar_cliente)
    boton_guardar.grid(row=4, columnspan=2, pady=10)


# Función para mostrar la interfaz de productos en la misma ventana
def formulario_productos():
    ventana_productos = tk.Toplevel()
    ventana_productos.title("Agregar Nuevo Producto")

    centrar_ventana(ventana_productos, 0.24, 0.277778)  # Ajustando altura para nuevo campo
    ventana_productos.resizable(False, False)

    etiqueta_nombre = ttk.Label(ventana_productos, text="Nombre del Producto:")
    etiqueta_nombre.grid(row=0, column=0, padx=10, pady=5)
    campo_nombre = ttk.Entry(ventana_productos)
    campo_nombre.grid(row=0, column=1, padx=10, pady=5)

    etiqueta_costo = ttk.Label(ventana_productos, text="Costo:")
    etiqueta_costo.grid(row=1, column=0, padx=10, pady=5)
    campo_costo = ttk.Entry(ventana_productos)
    campo_costo.grid(row=1, column=1, padx=10, pady=5)

    etiqueta_precio_inicial = ttk.Label(ventana_productos, text="Precio Inicial:")
    etiqueta_precio_inicial.grid(row=2, column=0, padx=10, pady=5)
    campo_precio_inicial = ttk.Entry(ventana_productos)
    campo_precio_inicial.grid(row=2, column=1, padx=10, pady=5)

    etiqueta_stock = ttk.Label(ventana_productos, text="Stock:")
    etiqueta_stock.grid(row=3, column=0, padx=10, pady=5)
    campo_stock = ttk.Entry(ventana_productos)
    campo_stock.grid(row=3, column=1, padx=10, pady=5)

    def guardar_producto():
        nombre = campo_nombre.get()
        stock = campo_stock.get()
        costo = campo_costo.get()
        precio_inicial = campo_precio_inicial.get()

        try:
            stock = int(stock)
            costo = float(costo)
            precio_inicial = float(precio_inicial) if precio_inicial else None
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un número entero y el costo/precio inicial números válidos")
            return
        
        sm.agregar_producto(nombre, stock, costo, precio_inicial)
        ventana_productos.destroy()

    boton_guardar = ttk.Button(ventana_productos, text="Guardar Producto", command=guardar_producto)
    boton_guardar.grid(row=4, columnspan=2, pady=10)

# Función para limpiar el contenido del frame
def limpiar_ventana():
    for widget in frame_contenido.winfo_children():
        widget.destroy()

def centrar_ventana(ventana, ancho_pct, alto_pct):
    """
    Ajusta el tamaño y centra la ventana en función de las proporciones de la pantalla.
    """
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ancho = int(ancho_pantalla * ancho_pct)
    alto = int(alto_pantalla * alto_pct)
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def mostrar_interfaz_clientes():
    limpiar_ventana()

    # Crear un Canvas dentro de frame_contenido
    canvas = tk.Canvas(frame_contenido, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Crear un scrollbar y enlazarlo al canvas
    scrollbar = ttk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un sub-frame dentro del canvas que contendrá el contenido desplazable
    sub_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=sub_frame, anchor="nw")

    # Configuración de auto-ajuste de la región de scroll
    sub_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Vincular el evento de la rueda del ratón al canvas para desplazarse desde cualquier área
    def on_mouse_wheel(event):
        scroll_pos = canvas.yview()
        if (event.delta > 0 and scroll_pos[0] <= 0) or (event.delta < 0 and scroll_pos[1] >= 1):
            return
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

     # Crear un frame para el filtro y los botones
    filtro_frame = ttk.Frame(sub_frame)
    filtro_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Campo de filtro
    etiqueta_filtro = ttk.Label(filtro_frame, text="Filtrar por ID o Nombre:", font=("Arial", 12))
    etiqueta_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    campo_filtro = ttk.Entry(filtro_frame)
    campo_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Función para filtrar los clientes
    def filtrar_tabla():
        texto_filtro = campo_filtro.get().lower()
        for item in tabla_clientes.get_children():
            tabla_clientes.delete(item)

        clientes_filtrados = [
            cliente for cliente in sm.obtener_todos_los_clientes()
            if texto_filtro in str(cliente.id_cliente).lower() or texto_filtro in cliente.nombre.lower()
        ]

        for cliente in clientes_filtrados:
            tabla_clientes.insert("", "end", values=(cliente.id_cliente, cliente.dni, cliente.nombre, cliente.direccion, cliente.telefono))

    # Botón para aplicar filtro
    boton_filtro = ttk.Button(filtro_frame, text="Aplicar Filtro", command=filtrar_tabla)
    boton_filtro.grid(row=0, column=2, padx=5, pady=5, sticky="w")
    # Botón para restablecer filtro
    def restablecer_filtro():
        campo_filtro.delete(0, tk.END)
        filtrar_tabla()

    boton_restablecer = ttk.Button(filtro_frame, text="Restablecer Filtro", command=restablecer_filtro)
    boton_restablecer.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # Configurar grid para que las columnas se expandan proporcionalmente
    filtro_frame.columnconfigure(1, weight=1)

    # Botón para ingresar un nuevo cliente
    boton_nuevo_cliente = ttk.Button(sub_frame, text="Ingresar Nuevo Cliente", command=formulario_clientes)
    boton_nuevo_cliente.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Etiqueta para la lista de clientes
    etiqueta_clientes = ttk.Label(sub_frame, text="Lista de Clientes:", font=("Arial", 12))
    etiqueta_clientes.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Crear un frame para la tabla
    frame_tabla = ttk.Frame(sub_frame)
    frame_tabla.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Crear la tabla para mostrar los clientes
    columnas = ("ID", "DNI", "Nombre", "Direccion", "Celular")
    tabla_clientes = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=30)
    tabla_clientes.heading("ID", text="ID Cliente")
    tabla_clientes.heading("DNI", text="DNI")
    tabla_clientes.heading("Nombre", text="Nombre")
    tabla_clientes.heading("Direccion", text="Direccion")
    tabla_clientes.heading("Celular", text="Celular")

    tabla_clientes.column("ID", width=100, anchor="center")
    tabla_clientes.column("DNI", width=200, anchor="center")
    tabla_clientes.column("Nombre", width=200+150, anchor="center")
    tabla_clientes.column("Direccion", width=200+150, anchor="center")
    tabla_clientes.column("Celular", width=150+150, anchor="center")

    scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_clientes.yview)
    tabla_clientes.configure(yscrollcommand=scrollbar_tabla.set)

    tabla_clientes.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.pack(side="right", fill="y")

    # Llenar la tabla con los clientes obtenidos
    filtrar_tabla()

    # Botón para modificar cliente
    def abrir_modificar_cliente():
        selected_item = tabla_clientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar un cliente para modificar.")
            return

        cliente_seleccionado = tabla_clientes.item(selected_item, 'values')
        id_cliente = cliente_seleccionado[0]
        ventana_modificar_cliente(id_cliente)

    boton_modificar = ttk.Button(sub_frame, text="Modificar Cliente", command=abrir_modificar_cliente)
    boton_modificar.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Botón para eliminar cliente
    def eliminar_cliente():
        selected_item = tabla_clientes.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar un cliente para eliminar.")
            return

        cliente_seleccionado = tabla_clientes.item(selected_item, 'values')
        id_cliente = cliente_seleccionado[0]
        confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar el cliente {cliente_seleccionado[2]}?")
        if confirmacion:
            sm.eliminar_cliente(id_cliente)
            filtrar_tabla()

    boton_eliminar = ttk.Button(sub_frame, text="Eliminar Cliente", command=eliminar_cliente)
    boton_eliminar.grid(row=4, column=0, padx=10, pady=10, sticky="w")



def ventana_modificar_cliente(id_cliente):
    # Obtener el cliente seleccionado
    cliente = sm.obtener_cliente_por_id(id_cliente)
    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado.")
        return

    # Crear una nueva ventana para modificar el cliente
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Cliente")
    centrar_ventana(ventana_modificar, 0.15625, 0.231481)
    ventana_modificar.resizable(False, False)

    # Etiquetas y campos de entrada para modificar el cliente
    ttk.Label(ventana_modificar, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    campo_nombre = ttk.Entry(ventana_modificar)
    campo_nombre.grid(row=0, column=1, padx=10, pady=5)
    campo_nombre.insert(0, cliente.nombre)

    ttk.Label(ventana_modificar, text="DNI:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    campo_dni = ttk.Entry(ventana_modificar)
    campo_dni.grid(row=1, column=1, padx=10, pady=5)
    campo_dni.insert(0, cliente.dni)

    ttk.Label(ventana_modificar, text="Dirección:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    campo_direccion = ttk.Entry(ventana_modificar)
    campo_direccion.grid(row=2, column=1, padx=10, pady=5)
    campo_direccion.insert(0, cliente.direccion)

    ttk.Label(ventana_modificar, text="Celular:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    campo_celular = ttk.Entry(ventana_modificar)
    campo_celular.grid(row=3, column=1, padx=10, pady=5)
    campo_celular.insert(0, cliente.telefono)

    # Función para guardar los cambios en el cliente
    def guardar_cambios():
        nombre = campo_nombre.get()
        direccion = campo_direccion.get()
        telefono = campo_celular.get()
        dni = campo_dni.get()

        # Llamar a la función de modificación en la base de datos
        sm.modificar_cliente(id_cliente, nombre, direccion, telefono, dni)

        # Actualizar la tabla en la interfaz principal
        mostrar_interfaz_clientes()
        ventana_modificar.destroy()

    boton_guardar = ttk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios)
    boton_guardar.grid(row=4, column=0, columnspan=2, pady=10)




def mostrar_interfaz_productos():
    limpiar_ventana()

    # Canvas con scroll general
    canvas = tk.Canvas(frame_contenido, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    sub_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=sub_frame, anchor="nw")
    sub_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def on_mouse_wheel(event):
        scroll_pos = canvas.yview()
        if (event.delta > 0 and scroll_pos[0] <= 0) or (event.delta < 0 and scroll_pos[1] >= 1):
            return
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Costo total
    frame_costo_total = ttk.Frame(sub_frame, padding=10, relief="ridge", borderwidth=2)
    frame_costo_total.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    etiqueta_costo_total = ttk.Label(frame_costo_total, text="Costo Total del Inventario:", font=("Arial", 14, "bold"))
    etiqueta_costo_total.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    costo_total = sm.obtener_costo_total_inventario()
    etiqueta_valor_costo = ttk.Label(frame_costo_total, text=f"S/. {costo_total:,.2f}", font=("Arial", 14, "bold"), foreground="red")
    etiqueta_valor_costo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Filtro por texto
    filtro_frames = ttk.Frame(sub_frame)
    filtro_frames.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    etiqueta_filtro = ttk.Label(filtro_frames, text="Filtrar por ID o Nombre:", font=("Arial", 12))
    etiqueta_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    campo_filtro = ttk.Entry(filtro_frames)
    campo_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Checkbox para filtrar por stock
    mostrar_solo_con_stock = tk.BooleanVar(value=True)
    check_stock = ttk.Checkbutton(filtro_frames, text="Solo con stock", variable=mostrar_solo_con_stock, command=lambda: [set_pagina(1), filtrar_tabla()])
    check_stock.grid(row=0, column=4, padx=5, pady=5, sticky="w")

    frame_acciones = ttk.Frame(sub_frame)
    frame_acciones.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    
    boton_agregar_producto = ttk.Button(frame_acciones, text="Agregar Producto", command=formulario_productos)
    boton_agregar_producto.pack(side="left", padx=5, pady=5)

    def abrir_modificar_producto():
        seleccion = tabla_productos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un producto para modificar.")
            return

        valores = tabla_productos.item(seleccion[0], "values")
        id_producto = int(valores[0])
        nombre_actual = valores[1]
        costo_actual = float(valores[2]) if valores[2] not in (None, "", "None") else 0.0
        precio_inicial_actual = float(valores[3]) if valores[3] not in (None, "", "None") else None
        stock_actual = int(valores[4]) if valores[4] not in (None, "", "None") else 0

        # Crear ventana de edición
        ventana_editar = tk.Toplevel()
        ventana_editar.title("Modificar Producto")
        centrar_ventana(ventana_editar, 0.2, 0.277778)
        ttk.Label(ventana_editar, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        entry_nombre = ttk.Entry(ventana_editar)
        entry_nombre.grid(row=0, column=1, padx=5, pady=5)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.config(state="readonly")

        ttk.Label(ventana_editar, text="Costo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        entry_costo = ttk.Entry(ventana_editar)
        entry_costo.grid(row=1, column=1, padx=5, pady=5)
        entry_costo.insert(0, str(costo_actual))
        entry_costo.config(state="readonly")

        ttk.Label(ventana_editar, text="Precio Inicial:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        entry_precio_inicial = ttk.Entry(ventana_editar)
        entry_precio_inicial.grid(row=2, column=1, padx=5, pady=5)
        if precio_inicial_actual is not None:
            entry_precio_inicial.insert(0, str(precio_inicial_actual))

        ttk.Label(ventana_editar, text="Stock:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entry_stock = ttk.Entry(ventana_editar)
        entry_stock.grid(row=3, column=1, padx=5, pady=5)
        entry_stock.insert(0, str(stock_actual))

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nuevo_costo = float(entry_costo.get())
            nuevo_precio_inicial = entry_precio_inicial.get()
            nuevo_precio_inicial = float(nuevo_precio_inicial) if nuevo_precio_inicial.strip() != "" else None
            nuevo_stock = int(entry_stock.get())

            # Llamada al backend para actualizar
            sm.modificar_producto(id_producto, nuevo_nombre, nuevo_stock, nuevo_costo, nuevo_precio_inicial)

            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            ventana_editar.destroy()
            filtrar_tabla()  # Recargar tabla

        ttk.Button(ventana_editar, text="Guardar", command=guardar_cambios).grid(row=4, column=0, columnspan=2, pady=10)


    boton_modificar_producto = ttk.Button(frame_acciones, text="Modificar Producto", command=abrir_modificar_producto)
    boton_modificar_producto.pack(side="left", padx=5, pady=5)
    

    # Tabla con scrollbar propio
    frame_tabla = ttk.Frame(sub_frame)
    frame_tabla.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    columnas = ("ID", "Nombre", "Costo", "Precio Inicial", "Stock", "Costo Total")
    tabla_productos = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=30)
    tabla_productos.heading("ID", text="ID Producto")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Costo", text="Costo")
    tabla_productos.heading("Precio Inicial", text="Precio Inicial")
    tabla_productos.heading("Stock", text="Stock")
    tabla_productos.heading("Costo Total", text="Costo Total")
    tabla_productos.column("ID", width=80)
    tabla_productos.column("Nombre", width=280, anchor="center")
    tabla_productos.column("Costo", width=120, anchor="center")
    tabla_productos.column("Precio Inicial", width=120, anchor="center")
    tabla_productos.column("Stock", width=120, anchor="center")
    tabla_productos.column("Costo Total", width=120, anchor="center")

    scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_productos.yview)
    tabla_productos.configure(yscrollcommand=scrollbar_tabla.set)

    tabla_productos.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.pack(side="right", fill="y")

    # Variables de paginación
    pagina_actual = tk.IntVar(value=1)
    tamanio_pagina = 250
    total_paginas = tk.IntVar(value=1)

    # Funciones de paginación
    def set_pagina(num):
        pagina_actual.set(num)

    def pagina_anterior():
        if pagina_actual.get() > 1:
            pagina_actual.set(pagina_actual.get() - 1)
            filtrar_tabla()

    def pagina_siguiente():
        if pagina_actual.get() < total_paginas.get():
            pagina_actual.set(pagina_actual.get() + 1)
            filtrar_tabla()

    # Función para llenar la tabla
    def filtrar_tabla():
        texto_filtro = campo_filtro.get().strip()
        solo_stock = mostrar_solo_con_stock.get()

        # Limpiar tabla
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)

        productos, total = sm.obtener_productos_paginados(
            filtro_texto=texto_filtro,
            solo_stock=solo_stock,
            pagina=pagina_actual.get(),
            tamanio_pagina=tamanio_pagina
        )

        for p in productos:
            costo_total = p.costo * p.stock
            tabla_productos.insert("", "end", values=(p.id_producto, p.nombre, p.costo, p.precio_inicial, p.stock, costo_total))

        # Actualizar paginación
        total_paginas.set(((total - 1) // tamanio_pagina) + 1)
        etiqueta_paginacion.config(text=f"Página {pagina_actual.get()} de {total_paginas.get()}")

        # Habilitar/deshabilitar botones
        btn_anterior.config(state="normal" if pagina_actual.get() > 1 else "disabled")
        btn_siguiente.config(state="normal" if pagina_actual.get() < total_paginas.get() else "disabled")

    # Botones de filtro
    boton_filtro = ttk.Button(filtro_frames, text="Aplicar Filtro", command=lambda: [set_pagina(1), filtrar_tabla()])
    boton_filtro.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    boton_restablecer = ttk.Button(filtro_frames, text="Restablecer Filtro", command=lambda: [campo_filtro.delete(0, tk.END), set_pagina(1), filtrar_tabla()])
    boton_restablecer.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    filtro_frames.columnconfigure(1, weight=1)

    # Controles de paginación (debajo de la tabla)
    frame_paginacion = ttk.Frame(sub_frame)
    frame_paginacion.grid(row=5, column=0, pady=10)

    btn_anterior = ttk.Button(frame_paginacion, text="Anterior", command=pagina_anterior)
    btn_anterior.pack(side="left", padx=5)

    etiqueta_paginacion = ttk.Label(frame_paginacion, text="Página 1 de 1")
    etiqueta_paginacion.pack(side="left", padx=10)

    btn_siguiente = ttk.Button(frame_paginacion, text="Siguiente", command=pagina_siguiente)
    btn_siguiente.pack(side="left", padx=5)

    # Llenar tabla al inicio
    filtrar_tabla()


def ventana_modificar_producto(id_producto):
    # Obtener el producto seleccionado
    producto = sm.obtener_producto_por_id(id_producto)
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado.")
        return

    # Crear una nueva ventana para modificar el producto
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Producto")
    centrar_ventana(ventana_modificar, 0.179167, 0.238889)

    def on_resize(event):
        # Obtener las dimensiones actuales de la ventana
        width = event.width
        height = event.height
        # Imprimir las dimensiones en la consola
        print(f"Ancho: {width}, Alto: {height}")
    #ventana_modificar.bind("<Configure>", on_resize)
    ventana_modificar.resizable(False, False)  # Fijar el tamaño de la ventana

    # Mostrar el nombre y costo como campos de solo lectura
    ttk.Label(ventana_modificar, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    etiqueta_nombre = ttk.Label(ventana_modificar, text=producto.nombre, relief="sunken", anchor="w")
    etiqueta_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    ttk.Label(ventana_modificar, text="Costo:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    etiqueta_costo = ttk.Label(ventana_modificar, text=f"{producto.costo:.2f}" if producto.costo is not None else "0.00", relief="sunken", anchor="w")
    etiqueta_costo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Campo para modificar el stock
    ttk.Label(ventana_modificar, text="Stock:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    campo_stock = ttk.Entry(ventana_modificar)
    campo_stock.grid(row=2, column=1, padx=10, pady=5)
    campo_stock.insert(0, producto.stock)

    # Función para guardar los cambios en el producto
    def guardar_cambios():
        try:
            stock = int(campo_stock.get())
            if stock < 0:
                raise ValueError("El stock no puede ser negativo.")
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un número entero no negativo.")
            return

        # Llamar a la función de modificación en la base de datos
        sm.modificar_producto(id_producto, producto.nombre, stock, producto.costo)

        # Actualizar la tabla en la interfaz principal
        mostrar_interfaz_productos()
        ventana_modificar.destroy()

    boton_guardar = ttk.Button(ventana_modificar, text="Guardar Cambios", command=guardar_cambios)
    boton_guardar.grid(row=4, column=0, columnspan=2, pady=10)

def ventana_ingresar_nota():
    ventana_nota = tk.Toplevel()
    ventana_nota.title("Ingresar Nota de Venta")
    centrar_ventana(ventana_nota, 0.78, 0.75)  # Ajustando altura para observaciones
    ventana_nota.resizable(False, False)

    productos_cantidades = []
    cliente_seleccionado = None

    # Título de la sección
    etiqueta_nota_venta = ttk.Label(ventana_nota, text="Crear Nota de Venta", font=("Arial", 16))
    etiqueta_nota_venta.grid(row=0, column=0, padx=10, pady=10)

    # Desplegable para seleccionar cliente
    etiqueta_cliente = ttk.Label(ventana_nota, text="Selecciona el Cliente:", font=("Arial", 12))
    etiqueta_cliente.grid(row=1, column=0, padx=10, pady=5, sticky="w")

    clientes = sm.obtener_todos_los_clientes()
    opciones_clientes = [f"{cliente.id_cliente} - {cliente.nombre}" for cliente in clientes]
    var_cliente = tk.StringVar()
    desplegable_cliente = ttk.Combobox(ventana_nota, textvariable=var_cliente, state="normal")
    desplegable_cliente.grid(row=1, column=1, padx=10, pady=5)
    desplegable_cliente['values'] = opciones_clientes

    def actualizar_opciones_cliente(*args):
        texto_ingresado = var_cliente.get().lower()
        # Filtrar opciones basadas en el texto ingresado
        opciones_filtradas = [opcion for opcion in opciones_clientes if texto_ingresado in opcion.lower()]
        desplegable_cliente['values'] = opciones_filtradas
        # Mantener el texto que ya está escrito sin interrumpir
        desplegable_cliente.event_generate('<Key>')

    # Asociar evento para actualizar opciones al escribir
    var_cliente.trace_add("write", actualizar_opciones_cliente)

    def confirmar_cliente():
        nonlocal cliente_seleccionado
        cliente_seleccionado = var_cliente.get().split(" - ")[0]
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Debes seleccionar un cliente.")
            return
        desplegable_cliente.config(state="disabled")
        boton_confirmar_cliente.config(state="disabled")
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)

    boton_confirmar_cliente = ttk.Button(ventana_nota, text="Confirmar Cliente", command=confirmar_cliente)
    boton_confirmar_cliente.grid(row=1, column=2, padx=10, pady=5)

    etiqueta_observaciones = ttk.Label(ventana_nota, text="Observaciones:", font=("Arial", 12))
    etiqueta_observaciones.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    
    campo_observaciones = tk.Text(ventana_nota, height=3, width=50)
    campo_observaciones.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
    
    # Tabla para productos agregados
    etiqueta_productos = ttk.Label(ventana_nota, text="Productos agregados:", font=("Arial", 12))
    etiqueta_productos.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    columnas_productos = ("ID", "Nombre", "Cantidad", "Precio Unitario", "Talla", "Color", "Subtotal")
    tabla_productos = ttk.Treeview(ventana_nota, columns=columnas_productos, show='headings', height=20)
    tabla_productos.heading("ID", text="ID Producto")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Cantidad", text="Cantidad")
    tabla_productos.heading("Precio Unitario", text="Precio Unitario")
    tabla_productos.heading("Talla", text="Talla")
    tabla_productos.heading("Color", text="Color")
    tabla_productos.heading("Subtotal", text="Subtotal")
    tabla_productos.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def agregar_producto():
        if cliente_seleccionado is None:
            messagebox.showerror("Error", "Primero debes seleccionar y confirmar un cliente.")
            return
        ventana_producto = tk.Toplevel()
        ventana_producto.title("Seleccionar Producto")
        centrar_ventana(ventana_producto, 0.23, 0.277778)

        etiqueta_producto = ttk.Label(ventana_producto, text="Producto:", font=("Arial", 12))
        etiqueta_producto.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        productos = sm.obtener_todos_los_productos()
        opciones_productos = [f"{producto.id_producto} - {producto.nombre}" for producto in productos]
        var_producto = tk.StringVar()
        desplegable_producto = ttk.Combobox(ventana_producto, textvariable=var_producto, state="normal")
        desplegable_producto.grid(row=0, column=1, padx=10, pady=5)
        desplegable_producto['values'] = opciones_productos

        def actualizar_opciones(*args):
            texto_ingresado = var_producto.get().lower()
            # Filtrar opciones basadas en el texto ingresado
            opciones_filtradas = [opcion for opcion in opciones_productos if texto_ingresado in opcion.lower()]
            desplegable_producto['values'] = opciones_filtradas
            # Mantener el texto que ya está escrito sin interrumpir
            desplegable_producto.event_generate('<Key>')        
        # Asociar evento para actualizar opciones al escribir
        var_producto.trace_add("write", actualizar_opciones)

        def actualizar_precio_inicial(*args):
            try:
                producto_seleccionado = var_producto.get().split(" - ")[0]
                if producto_seleccionado.isdigit():
                    producto = sm.obtener_producto_por_id(int(producto_seleccionado))
                    if producto and producto.precio_inicial:
                        campo_precio.delete(0, tk.END)
                        campo_precio.insert(0, str(producto.precio_inicial))
            except:
                pass

        var_producto.trace_add("write", actualizar_precio_inicial)

        etiqueta_cantidad = ttk.Label(ventana_producto, text="Cantidad:", font=("Arial", 12))
        etiqueta_cantidad.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entrada_cantidad = ttk.Entry(ventana_producto)
        entrada_cantidad.grid(row=1, column=1, padx=10, pady=5)

        campo_precio_label = ttk.Label(ventana_producto, text="Precio Unitario:", font=("Arial", 12))
        campo_precio_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        campo_precio = ttk.Entry(ventana_producto)
        campo_precio.grid(row=2, column=1, padx=10, pady=5)
        campo_precio.insert(0, "0")

        # Campo Talla
        campo_talla_label = ttk.Label(ventana_producto, text="Talla:", font=("Arial", 12))
        campo_talla_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        campo_talla = ttk.Entry(ventana_producto)
        campo_talla.grid(row=3, column=1, padx=10, pady=5)

        # Campo Color
        campo_color_label = ttk.Label(ventana_producto, text="Color:", font=("Arial", 12))
        campo_color_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        campo_color = ttk.Entry(ventana_producto)
        campo_color.grid(row=4, column=1, padx=10, pady=5)

        def confirmar_producto():
            producto_seleccionado = var_producto.get().split(" - ")[0]
            cantidad = entrada_cantidad.get()
            precio_unitario = float(campo_precio.get())
            talla = campo_talla.get()
            color = campo_color.get()
            if not cantidad.isdigit() or int(cantidad) <= 0:
                messagebox.showerror("Error", "Cantidad debe ser un número positivo.")
                return
            if int(cantidad) <= 0 or precio_unitario <= 0:
                raise ValueError("La cantidad y el precio deben ser mayores a cero.")
            producto = sm.obtener_producto_por_id(producto_seleccionado)
            if producto:
                subtotal = round(precio_unitario * int(cantidad),2)
                tabla_productos.insert("", "end", values=(producto.id_producto, producto.nombre, cantidad, precio_unitario, talla, color, subtotal))
                productos_cantidades.append((producto.id_producto, int(cantidad), precio_unitario, talla, color))
            ventana_producto.destroy()

        boton_confirmar_producto = ttk.Button(ventana_producto, text="OK", command=confirmar_producto)
        boton_confirmar_producto.grid(row=5, column=0, columnspan=2, pady=10)

    boton_agregar_producto = ttk.Button(ventana_nota, text="Agregar Producto", command=agregar_producto)
    boton_agregar_producto.grid(row=5, column=0, padx=10, pady=10)

    def cancelar_nota_venta():
        productos_cantidades.clear()
        cliente_seleccionado = None
        var_cliente.set("")
        campo_observaciones.delete(1.0, tk.END)
        desplegable_cliente.config(state="normal")
        boton_confirmar_cliente.config(state="normal")
        for item in tabla_productos.get_children():
            tabla_productos.delete(item)

    boton_cancelar = ttk.Button(ventana_nota, text="Cancelar Nota", command=cancelar_nota_venta)
    boton_cancelar.grid(row=6, column=0, padx=10, pady=10)

    def guardar_nota_venta():
        if cliente_seleccionado is None:
            messagebox.showerror("Error", "Debes confirmar un cliente antes de guardar.")
            return
        if not productos_cantidades:
            messagebox.showerror("Error", "Debes agregar al menos un producto.")
            return
        try:
            observaciones = campo_observaciones.get(1.0, tk.END).strip()
            observaciones = observaciones if observaciones else None
            
            id_nota, total = sm.crear_nota_venta(cliente_seleccionado, productos_cantidades, observaciones)
            
            messagebox.showinfo("Éxito", f"Nota creada. ID: {id_nota}, Total: {total:.2f}")
            cancelar_nota_venta()
            ventana_nota.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la nota: {e}")

    boton_guardar = ttk.Button(ventana_nota, text="Guardar Nota de Venta", command=guardar_nota_venta)
    boton_guardar.grid(row=6, column=1, padx=10, pady=10)


def mostrar_interfaz_nota_venta():
    limpiar_ventana()

    # Variables para paginación
    pagina_actual = tk.IntVar(value=1)
    tamanio_pagina = 150
    total_paginas = tk.IntVar(value=1)

    # Crear Canvas y Scroll
    canvas = tk.Canvas(frame_contenido, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    sub_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=sub_frame, anchor="nw")
    sub_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # Frame de filtros
    frame_filtros = ttk.Frame(sub_frame)
    frame_filtros.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Primera fila de filtros - Búsqueda por texto
    etiqueta_filtro = ttk.Label(frame_filtros, text="Filtrar por Cliente o ID:", font=("Arial", 12))
    etiqueta_filtro.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    campo_filtro = ttk.Entry(frame_filtros)
    campo_filtro.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    # Segunda fila de filtros - Estado
    etiqueta_estado = ttk.Label(frame_filtros, text="Filtrar por Estado:", font=("Arial", 12))
    etiqueta_estado.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    combo_estado = ttk.Combobox(frame_filtros, values=["Todos", "ABIERTO", "PREPARADO", "ENVIADO"], state="readonly")
    combo_estado.set("Todos")
    combo_estado.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # Configurar columnas para que se expandan
    frame_filtros.columnconfigure(1, weight=1)

    # Tabla
    frame_tabla = ttk.Frame(sub_frame)
    frame_tabla.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    columnas = ("ID Nota", "Cliente", "Fecha", "Estado", "Estado Pedido", "Total")
    tabla_notas = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=30)
    for col in columnas:
        tabla_notas.heading(col, text=col)
        tabla_notas.column(col, width=200, anchor="center")
    scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_notas.yview)
    tabla_notas.configure(yscrollcommand=scrollbar_tabla.set)
    tabla_notas.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.pack(side="right", fill="y")

    # Función para cargar datos
    def cargar_tabla():
        tabla_notas.delete(*tabla_notas.get_children())
        filtro_texto = campo_filtro.get().strip()
        filtro_estado = combo_estado.get() if combo_estado.get() != "Todos" else ""

        # sm.obtener_notas_paginadas ahora debe recibir ambos filtros
        notas, total_registros = sm.obtener_notas_paginadas(
            filtro_texto, pagina_actual.get(), tamanio_pagina, filtro_estado
        )

        for nota in notas:
            tabla_notas.insert("", "end", values=(
                nota.id_nota, nota.cliente.nombre, nota.fecha, nota.estado, nota.estado_pedido, nota.total
            ))

        # Calcular total de páginas
        total_paginas.set(((total_registros - 1) // tamanio_pagina) + 1 if total_registros > 0 else 1)
        etiqueta_paginacion.config(text=f"Página {pagina_actual.get()} de {total_paginas.get()}")

        # Habilitar/deshabilitar botones
        btn_anterior.config(state="normal" if pagina_actual.get() > 1 else "disabled")
        btn_siguiente.config(state="normal" if pagina_actual.get() < total_paginas.get() else "disabled")

    # Funciones de paginación
    def pagina_anterior():
        if pagina_actual.get() > 1:
            pagina_actual.set(pagina_actual.get() - 1)
            cargar_tabla()

    def pagina_siguiente():
        if pagina_actual.get() < total_paginas.get():
            pagina_actual.set(pagina_actual.get() + 1)
            cargar_tabla()

    # Botones de filtro
    boton_filtro = ttk.Button(frame_filtros, text="Aplicar Filtro", command=lambda: [pagina_actual.set(1), cargar_tabla()])
    boton_filtro.grid(row=0, column=2, rowspan=2, padx=5, sticky="ns")

    boton_restablecer = ttk.Button(frame_filtros, text="Restablecer", 
                                   command=lambda: [campo_filtro.delete(0, tk.END), combo_estado.set("Todos"), pagina_actual.set(1), cargar_tabla()])
    boton_restablecer.grid(row=0, column=3, rowspan=2, padx=5, sticky="ns")

    # Botones extra
    ttk.Button(sub_frame, text="Ingresar Nota de Venta", command=ventana_ingresar_nota).grid(row=1, column=0, padx=10, pady=10, sticky="w")

    def eliminar_nota():
        selected_item = tabla_notas.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar una nota de venta para eliminar.")
            return
        id_nota = tabla_notas.item(selected_item, 'values')[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar nota {id_nota}?"):
            sm.eliminar_nota_venta(id_nota)
            cargar_tabla()

    ttk.Button(sub_frame, text="Eliminar Nota", command=eliminar_nota).grid(row=4, column=0, padx=10, pady=10, sticky="w")

    def ver_detalles():
        selected_item = tabla_notas.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar una nota.")
            return
        id_nota = tabla_notas.item(selected_item, 'values')[0]
        ventana_detalles_nota(id_nota, "nota_de_venta")

    ttk.Button(sub_frame, text="Ver Detalles", command=ver_detalles).grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Controles de paginación al estilo productos
    frame_paginacion = ttk.Frame(sub_frame)
    frame_paginacion.grid(row=5, column=0, pady=10)

    btn_anterior = ttk.Button(frame_paginacion, text="Anterior", command=pagina_anterior)
    btn_anterior.pack(side="left", padx=5)

    etiqueta_paginacion = ttk.Label(frame_paginacion, text="Página 1 de 1")
    etiqueta_paginacion.pack(side="left", padx=10)

    btn_siguiente = ttk.Button(frame_paginacion, text="Siguiente", command=pagina_siguiente)
    btn_siguiente.pack(side="left", padx=5)

    # Cargar datos iniciales
    cargar_tabla()

def ventana_detalles_nota(id_nota, ventana):
    ventana_detalles = tk.Toplevel()
    ventana_detalles.title("Detalles de la Nota de Venta")
    #ventana_detalles.resizable(False, False)

    centrar_ventana(ventana_detalles, 0.82, 0.694444) #VOLVER A 0.82 para produccion para desarrollo 0.92


    def on_resize(event):
        # Obtener las dimensiones actuales de la ventana
        width = event.width
        height = event.height
        # Imprimir las dimensiones en la consola
        print(f"Ancho: {width}, Alto: {height}")
    #ventana_detalles.bind("<Configure>", on_resize)

    # Obtener la nota de venta y sus detalles
    nota = sm.obtener_nota_venta_por_id(id_nota)
    cliente = sm.obtener_cliente_por_id(nota.id_cliente)
    detalles = sm.obtener_detalles_nota_por_id_nota(id_nota)
    amortizaciones = sm.obtener_amortizaciones_por_id_nota(id_nota)

    # Información de la nota de venta y cliente
    # Información de la nota de venta y cliente
    etiqueta_info = ttk.Label(ventana_detalles, text=f"Nota de Venta ID: {id_nota}", font=("Arial", 14))
    etiqueta_info.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    etiqueta_cliente = ttk.Label(ventana_detalles, text=f"Cliente: {cliente.nombre}", font=("Arial", 12))
    etiqueta_cliente.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    etiqueta_fecha = ttk.Label(ventana_detalles, text=f"Fecha: {nota.fecha}", font=("Arial", 12))
    etiqueta_fecha.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    # Mostrar y actualizar el estado
    etiqueta_estado = ttk.Label(ventana_detalles, text=f"Estado: {nota.estado}", font=("Arial", 12))
    etiqueta_estado.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    # Frame para el estado de pedido
    frame_estado_pedido = ttk.Frame(ventana_detalles)
    frame_estado_pedido.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    ttk.Label(frame_estado_pedido, text="Estado del Pedido:", font=("Arial", 12)).pack(side="left", padx=(0, 10))

    var_estado_pedido = tk.StringVar(value=nota.estado_pedido if hasattr(nota, 'estado_pedido') and nota.estado_pedido else "ABIERTO")

    opciones_estado_pedido = ["ABIERTO", "PREPARADO", "ENVIADO"]
    combo_estado_pedido = ttk.Combobox(frame_estado_pedido, textvariable=var_estado_pedido, values=opciones_estado_pedido, state="readonly", width=12)
    combo_estado_pedido.pack(side="left", padx=(0, 10))

    def cambiar_estado_pedido():
        try:
            nuevo_estado = var_estado_pedido.get()
            sm.actualizar_estado_pedido(id_nota, nuevo_estado)
            messagebox.showinfo("Éxito", f"Estado del pedido actualizado a: {nuevo_estado}",parent=ventana_detalles)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el estado del pedido: {e}")

    boton_actualizar_estado = ttk.Button(frame_estado_pedido, text="Actualizar", command=cambiar_estado_pedido)
    boton_actualizar_estado.pack(side="left", padx=5)

    def modificar_nota():
        if nota.estado.lower() == "cancelado":
            messagebox.showerror("Error", "No puedes modificar una nota de venta que ya está cancelada.")
            return

        # Ventana de modificación mejorada
        ventana_modificar = tk.Toplevel(ventana_detalles)
        ventana_modificar.title("Modificar Nota de Venta")
        centrar_ventana(ventana_modificar, 0.75, 0.45)

        # Etiqueta para productos
        etiqueta_productos_modificar = ttk.Label(ventana_modificar, text="Productos de la Nota:", font=("Arial", 12))
        etiqueta_productos_modificar.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Definir columnas de la tabla
        columnas_modificar = ("ID", "Nombre", "Cantidad", "Precio Unitario", "Color", "Talla", "Subtotal")
        tabla_modificar = ttk.Treeview(ventana_modificar, columns=columnas_modificar, show='headings', height=8)

        for col in columnas_modificar:
            tabla_modificar.heading(col, text=col)
            if col == "ID":
                tabla_modificar.column(col, width=80, anchor="center")
            elif col == "Nombre":
                tabla_modificar.column(col, width=200, anchor="center")
            elif col in ["Cantidad", "Precio Unitario", "Subtotal"]:
                tabla_modificar.column(col, width=120, anchor="center")
            else:  # Color, Talla
                tabla_modificar.column(col, width=100, anchor="center")

        tabla_modificar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Rellenar la tabla con los detalles actuales
        for detalle in detalles:
            producto = sm.obtener_producto_por_id(detalle.id_producto)
            nombre_producto = producto.nombre if producto else "Desconocido"
            tabla_modificar.insert("", "end", values=(
                detalle.id_producto,
                nombre_producto,
                detalle.cantidad,
                detalle.precio_unitario,
                detalle.color,
                detalle.talla,
                detalle.subtotal
            ))

        def editar_producto_seleccionado():
            selected_item = tabla_modificar.selection()
            if not selected_item:
                messagebox.showerror("Error", "Debes seleccionar un producto para editar.")
                return

            # Obtener los datos del producto seleccionado
            producto_data = tabla_modificar.item(selected_item, 'values')
            
            # Crear ventana de edición
            ventana_editar = tk.Toplevel(ventana_modificar)
            ventana_editar.title("Editar Producto")
            centrar_ventana(ventana_editar, 0.3, 0.5)
            #ventana_editar.resizable(False, False)
            
            # Centrar la ventana
            ventana_editar.transient(ventana_modificar)
            ventana_editar.grab_set()

            # Campos de edición
            ttk.Label(ventana_editar, text="Producto:", font=("Arial", 12, "bold")).pack(pady=5)
            ttk.Label(ventana_editar, text=f"{producto_data[0]} - {producto_data[1]}", font=("Arial", 10)).pack(pady=5)

            ttk.Label(ventana_editar, text="Cantidad:", font=("Arial", 10)).pack(pady=(15, 5))
            var_cantidad = tk.StringVar(value=producto_data[2])
            entry_cantidad = ttk.Entry(ventana_editar, textvariable=var_cantidad, width=20)
            entry_cantidad.pack(pady=5)

            ttk.Label(ventana_editar, text="Precio Unitario:", font=("Arial", 10)).pack(pady=(10, 5))
            var_precio = tk.StringVar(value=producto_data[3])
            entry_precio = ttk.Entry(ventana_editar, textvariable=var_precio, width=20)
            entry_precio.pack(pady=5)

            ttk.Label(ventana_editar, text="Color:", font=("Arial", 10)).pack(pady=(10, 5))
            var_color = tk.StringVar(value=producto_data[4])
            entry_color = ttk.Entry(ventana_editar, textvariable=var_color, width=20)
            entry_color.pack(pady=5)

            ttk.Label(ventana_editar, text="Talla:", font=("Arial", 10)).pack(pady=(10, 5))
            var_talla = tk.StringVar(value=producto_data[5])
            entry_talla = ttk.Entry(ventana_editar, textvariable=var_talla, width=20)
            entry_talla.pack(pady=5)

            # Función para actualizar subtotal automáticamente
            def actualizar_subtotal(*args):
                try:
                    cantidad = float(var_cantidad.get() or 0)
                    precio = float(var_precio.get() or 0)
                    subtotal = round(cantidad * precio, 2)
                    label_subtotal.config(text=f"Subtotal: S/.{subtotal:.2f}")
                except:
                    label_subtotal.config(text="Subtotal: S/.0.00")

            # Vincular eventos para actualizar subtotal
            var_cantidad.trace_add("write", actualizar_subtotal)
            var_precio.trace_add("write", actualizar_subtotal)

            # Mostrar subtotal calculado
            label_subtotal = ttk.Label(ventana_editar, text="Subtotal: S/.0.00", font=("Arial", 10, "bold"))
            label_subtotal.pack(pady=15)
            actualizar_subtotal()  # Calcular subtotal inicial

            # Función para guardar cambios
            def guardar_cambios_producto():
                try:
                    nueva_cantidad = int(var_cantidad.get())
                    nuevo_precio = float(var_precio.get())
                    nuevo_color = var_color.get().strip()
                    nueva_talla = var_talla.get().strip()
                    nuevo_subtotal = round(nueva_cantidad * nuevo_precio, 2)

                    if nueva_cantidad <= 0:
                        raise ValueError("La cantidad debe ser mayor a 0")
                    if nuevo_precio < 0:
                        raise ValueError("El precio no puede ser negativo")

                    # Actualizar la fila en la tabla
                    tabla_modificar.item(selected_item, values=(
                        producto_data[0],  # ID (no cambia)
                        producto_data[1],  # Nombre (no cambia)
                        nueva_cantidad,
                        nuevo_precio,
                        nuevo_color,
                        nueva_talla,
                        nuevo_subtotal
                    ))

                    ventana_editar.destroy()
                    ventana_modificar.lift()  # Traer ventana de modificar al frente
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente.", parent=ventana_modificar)
                    

                except ValueError as e:
                    messagebox.showerror("Error", f"Datos inválidos: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

            # Botones
            frame_botones_editar = ttk.Frame(ventana_editar)
            frame_botones_editar.pack(pady=20)

            ttk.Button(frame_botones_editar, text="Guardar Cambios", command=guardar_cambios_producto).pack(side="left", padx=5)
            ttk.Button(frame_botones_editar, text="Cancelar", command=ventana_editar.destroy).pack(side="left", padx=5)

        # Función para agregar un nuevo producto
        def agregar_producto():
            agregar_producto_a_nota(tabla_modificar)
        
        frame_botones = ttk.Frame(ventana_modificar)
        frame_botones.grid(row=2, column=0, columnspan=3, pady=10, sticky="w")

        boton_agregar = ttk.Button(frame_botones, text="Agregar Producto", command=agregar_producto)
        boton_agregar.pack(side="left", padx=5)

        boton_editar = ttk.Button(frame_botones, text="Editar Producto", command=editar_producto_seleccionado)
        boton_editar.pack(side="left", padx=5)

        # Lista temporal para mantener los cambios hasta que se guarden
        productos_a_eliminar = []

        # Botón para eliminar un producto seleccionado
        def eliminar_producto():
            selected_item = tabla_modificar.selection()
            if not selected_item:
                messagebox.showerror("Error", "Debes seleccionar un producto para eliminar.")
                return

            confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este producto de la nota de venta?")
            if not confirmacion:
                return

            producto_seleccionado = tabla_modificar.item(selected_item, 'values')
            id_producto = producto_seleccionado[0]

            productos_a_eliminar.append(id_producto)
            tabla_modificar.delete(selected_item)

        boton_eliminar = ttk.Button(frame_botones, text="Eliminar Producto", command=eliminar_producto)
        boton_eliminar.pack(side="left", padx=5)

        # Botón para guardar cambios
        def guardar_cambios():
            try:
                # Obtener los detalles actuales de la tabla
                nuevos_detalles = []
                for item in tabla_modificar.get_children():
                    valores = tabla_modificar.item(item, 'values')
                    id_producto = valores[0]
                    cantidad = valores[2]
                    precio_unitario = valores[3]
                    color = valores[4]
                    talla = valores[5]
                    subtotal = valores[6]
                    nuevos_detalles.append((int(id_producto), int(cantidad), float(precio_unitario), color, talla, float(subtotal)))

                sm.actualizar_nota_venta_mejorada(id_nota, nuevos_detalles, productos_a_eliminar)

                ventana_modificar.destroy()
                ventana_detalles.destroy()
                messagebox.showinfo("Éxito", "Nota de venta modificada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la nota de venta: {e}")

        boton_guardar = ttk.Button(frame_botones, text="Guardar Cambios", command=guardar_cambios)
        boton_guardar.pack(side="left", padx=5)

    # Agregar botón de modificar nota a la ventana principal
    if ventana == "nota_de_venta":
        boton_modificar_nota = ttk.Button(ventana_detalles, text="Modificar Nota de Venta", command=modificar_nota)
        boton_modificar_nota.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    # Tabla para mostrar los productos de la nota de venta
    # Frame para la tabla de productos reservados y amortizaciones
    frame_izquierda = ttk.Frame(ventana_detalles)
    frame_izquierda.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")  # Columna izquierda para tablas

    # Frame para los detalles de pago
    frame_derecha = ttk.Frame(ventana_detalles)
    frame_derecha.grid(row=4, column=1, padx=20, pady=20, sticky="n")  # Columna derecha para detalles

    # Tabla de productos reservados
    etiqueta_productos = ttk.Label(frame_izquierda, text="Productos Reservados:", font=("Arial", 12))
    etiqueta_productos.grid(row=0, column=0, pady=10, sticky="w")

    columnas_productos = ("ID Producto", "Nombre", "Cantidad", "Precio Unitario", "Color", "Talla", "Subtotal")
    tabla_productos = ttk.Treeview(frame_izquierda, columns=columnas_productos, show='headings', height=8)

    # Definir encabezados y tamaños de las columnas
    tabla_productos.heading("ID Producto", text="ID Producto")
    tabla_productos.heading("Nombre", text="Nombre")
    tabla_productos.heading("Cantidad", text="Cantidad")
    tabla_productos.heading("Precio Unitario", text="Precio Unitario")
    tabla_productos.heading("Color", text="Color")
    tabla_productos.heading("Talla", text="Talla")
    tabla_productos.heading("Subtotal", text="Subtotal")

    # Ajustar el ancho y centrar contenido
    tabla_productos.column("ID Producto", width=100, anchor="center")  
    tabla_productos.column("Nombre", width=150+120, anchor="center")  
    tabla_productos.column("Cantidad", width=70+80, anchor="center")  
    tabla_productos.column("Precio Unitario", width=110+50, anchor="center")  
    tabla_productos.column("Color", width=80+200, anchor="center")  
    tabla_productos.column("Talla", width=80+80, anchor="center")  
    tabla_productos.column("Subtotal", width=100+80, anchor="center")  

    tabla_productos.grid(row=1, column=0, sticky="nsew")
    
    for detalle in detalles:
        producto = sm.obtener_producto_por_id(detalle.id_producto)
        nombre_producto = producto.nombre if producto else "Desconocido"
        tabla_productos.insert("", "end", values=(
            detalle.id_producto,
            nombre_producto,
            detalle.cantidad,
            detalle.precio_unitario,
            detalle.color,
            detalle.talla,
            detalle.subtotal
        ))

    # Tabla de amortizaciones
    etiqueta_amortizaciones = ttk.Label(frame_izquierda, text="Amortizaciones:", font=("Arial", 12))
    etiqueta_amortizaciones.grid(row=2, column=0, pady=10, sticky="w")

    columnas_amortizaciones = ("ID Amortización", "Monto", "Fecha")
    tabla_amortizaciones = ttk.Treeview(frame_izquierda, columns=columnas_amortizaciones, show='headings', height=5)

    # Definir encabezados y tamaños de las columnas
    tabla_amortizaciones.heading("ID Amortización", text="ID Amortización")
    tabla_amortizaciones.heading("Monto", text="Monto")
    tabla_amortizaciones.heading("Fecha", text="Fecha")

    # Ajustar el ancho y centrar contenido
    tabla_amortizaciones.column("ID Amortización", width=100, anchor="center")
    tabla_amortizaciones.column("Monto", width=100, anchor="center")
    tabla_amortizaciones.column("Fecha", width=120, anchor="center")

    tabla_amortizaciones.grid(row=3, column=0, sticky="nsew")

    for amortizacion in amortizaciones:
        tabla_amortizaciones.insert("", "end", values=(
            amortizacion.id_amortizacion,
            amortizacion.monto,
            amortizacion.fecha
        ))

     # Botón para añadir una nueva amortización
    def agregar_nueva_amortizacion():
        ventana_amortizacion = tk.Toplevel()
        ventana_amortizacion.title("Nueva Amortización")
        #ventana_amortizacion.geometry("300x150")
        centrar_ventana(ventana_amortizacion, 0.179167, 0.18)
        ventana_amortizacion.resizable(False, False)

        # Etiqueta y campo de entrada para el monto de amortización
        etiqueta_monto = ttk.Label(ventana_amortizacion, text="Ingrese el monto de la amortización:", font=("Arial", 12))
        etiqueta_monto.pack(pady=10)

        campo_monto = ttk.Entry(ventana_amortizacion)
        campo_monto.pack(pady=5)

        # Función para guardar la amortización
        def guardar_amortizacion():
            try:
                monto = float(campo_monto.get())
                if monto <= 0:
                    raise ValueError("El monto debe ser positivo.")

                # Agregar amortización en la base de datos
                sm.agregar_amortizacion(id_nota, monto)
                tabla_amortizaciones.insert("", "end", values=(len(tabla_amortizaciones.get_children()) + 1, monto, date.today()))
                
                # Cerrar la ventana de amortización
                ventana_amortizacion.destroy()
                messagebox.showinfo("Éxito", "Amortización agregada exitosamente.", parent=ventana_detalles)
        
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un monto válido.", parent=ventana_detalles)

        # Botón para confirmar la amortización
        boton_confirmar = ttk.Button(ventana_amortizacion, text="Guardar", command=guardar_amortizacion)
        boton_confirmar.pack(pady=10)

            # Botón para eliminar una amortización
    def eliminar_amortizacion():
        # Obtener la selección de la tabla
        selected_item = tabla_amortizaciones.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar una amortización para eliminar.")
            return

        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar esta amortización?")
        if not confirmacion:
            return

        # Obtener el ID de la amortización seleccionada
        amortizacion_seleccionada = tabla_amortizaciones.item(selected_item, 'values')
        id_amortizacion = amortizacion_seleccionada[0]

        try:
            # Llamar a la función para eliminar la amortización de la base de datos
            sm.eliminar_amortizacion(id_amortizacion)

            # Eliminar de la tabla en la interfaz
            tabla_amortizaciones.delete(selected_item)

            messagebox.showinfo("Éxito", "Amortización eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la amortización: {e}")

    


    # Botón para confirmar la venta
    def confirmar_venta():
        respuesta = messagebox.askyesno("Confirmar Venta", "¿Estás seguro de que deseas confirmar esta venta?")
        if respuesta:
            sm.agregar_venta(id_nota)  # Llamar a la función para agregar la venta
            etiqueta_estado.config(text="Estado: Cancelado")  # Actualizar el estado en la interfaz
    if ventana == "nota_de_venta":
        # Crear un frame para los botones de amortización y confirmar venta
        frame_botones = ttk.Frame(ventana_detalles)
        frame_botones.grid(row=9, column=0, columnspan=2, pady=10, padx=10, sticky="w")

        # Botón para agregar una nueva amortización
        boton_amortizacion = ttk.Button(frame_botones, text="Agregar Amortización", command=agregar_nueva_amortizacion)
        boton_amortizacion.grid(row=0, column=0, padx=5)

        # Botón para eliminar amortización
        boton_eliminar_amortizacion = ttk.Button(frame_botones, text="Eliminar Amortización", command=eliminar_amortizacion)
        boton_eliminar_amortizacion.grid(row=0, column=1, pady=10, sticky="w")

        # Botón para confirmar la venta
        boton_confirmar_venta = ttk.Button(frame_botones, text="Confirmar Venta", command=confirmar_venta)
        boton_confirmar_venta.grid(row=0, column=2, padx=5)

    # Frame para el total y el botón de impresión
    frame_imprimir = ttk.Frame(ventana_detalles)
    frame_imprimir.grid(row=10, column=0, columnspan=2, padx=20, pady=20)

    # Cálculos
    total_amortizacion = sm.total_menos_amortizacion(id_nota)  # Total restante por pagar
    total_pagado = nota.total - total_amortizacion  # Total ya amortizado
    estado_pago = "Saldada" if total_amortizacion <= 0 else "Pendiente"

    ttk.Label(frame_derecha, text="Detalles de Pago:", font=("Arial", 14, "bold")).grid(row=0, column=0, pady=10, sticky="w")
    ttk.Label(frame_derecha, text="Total:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
    ttk.Label(frame_derecha, text=f"{nota.total:.2f}", font=("Arial", 12, "bold")).grid(row=1, column=1, pady=5, sticky="w")
    ttk.Label(frame_derecha, text="Pagado:", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
    ttk.Label(frame_derecha, text=f"{total_pagado:.2f}", font=("Arial", 12)).grid(row=2, column=1, pady=5, sticky="w")
    ttk.Label(frame_derecha, text="Debe:", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky="w")
    ttk.Label(frame_derecha, text=f"{total_amortizacion:.2f}", font=("Arial", 12, "bold"),
            foreground="red" if total_amortizacion > 0 else "green").grid(row=3, column=1, pady=5, sticky="w")
    ttk.Label(frame_derecha, text="Estado de Pago:", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky="w")
    ttk.Label(frame_derecha, text=estado_pago, font=("Arial", 12, "bold"),
            foreground="green" if estado_pago == "Saldada" else "red").grid(row=4, column=1, pady=5, sticky="w")

    # Botón para imprimir la nota de venta
    boton_imprimir = ttk.Button(frame_derecha, text="Imprimir Nota de Venta", command=lambda: imprimir_nota_venta(nota, detalles, cliente))
    boton_imprimir.grid(row=5, column=0, columnspan=2, pady=20)

    # Apartado de observaciones dentro del frame de detalles de pago
    ttk.Label(frame_derecha, text="Observaciones:", font=("Arial", 12, "bold")).grid(row=6, column=0, pady=(20, 5), sticky="w")

    # Obtener observaciones actuales
    try:
        observaciones_actuales = sm.obtener_observaciones_nota(id_nota) or ""
    except:
        observaciones_actuales = ""

    # Área de texto para mostrar y editar observaciones
    texto_observaciones = tk.Text(frame_derecha, height=4, width=35, wrap=tk.WORD)
    texto_observaciones.insert("1.0", observaciones_actuales)
    texto_observaciones.grid(row=7, column=0, columnspan=2, pady=5, sticky="ew")

    # Función para guardar observaciones
    def guardar_observaciones():
        try:
            nuevas_observaciones = texto_observaciones.get("1.0", tk.END).strip()
            sm.actualizar_observaciones_nota(id_nota, nuevas_observaciones)
            messagebox.showinfo("Éxito", "Observaciones actualizadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron actualizar las observaciones: {e}")

    # Función para limpiar observaciones
    def limpiar_observaciones():
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas limpiar las observaciones?")
        if confirmacion:
            texto_observaciones.delete("1.0", tk.END)

    # Frame para botones de observaciones
    frame_botones_obs = ttk.Frame(frame_derecha)
    frame_botones_obs.grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

    # Botones para observaciones
    boton_guardar_obs = ttk.Button(frame_botones_obs, text="Guardar Observaciones", command=guardar_observaciones)
    boton_guardar_obs.pack(side="left", padx=5)

    boton_limpiar_obs = ttk.Button(frame_botones_obs, text="Limpiar", command=limpiar_observaciones)
    boton_limpiar_obs.pack(side="left", padx=5)



def agregar_producto_a_nota(tabla_modificar):
    ventana_producto = tk.Toplevel()
    ventana_producto.title("Agregar Producto a Nota")
    centrar_ventana(ventana_producto, 0.234375, 0.509259)

    ventana_producto.resizable(False, False)

    productos = sm.obtener_todos_los_productos()
    opciones_productos = [f"{producto.id_producto} - {producto.nombre}" for producto in productos]

    var_producto = tk.StringVar(ventana_producto)
    ttk.Label(ventana_producto, text="Selecciona el Producto:").pack(pady=10)
    # Crear Combobox con capacidad de escritura
    menu_producto = ttk.Combobox(ventana_producto, textvariable=var_producto, values=opciones_productos, state="normal")
    menu_producto.pack(pady=5)

    # Habilitar autocompletado
    def filtrar_opciones(event):
        texto_ingresado = menu_producto.get().lower()
        opciones_filtradas = [opcion for opcion in opciones_productos if texto_ingresado in opcion.lower()]
        menu_producto["values"] = opciones_filtradas
        if not opciones_filtradas:
            menu_producto.event_generate("<Down>")

    menu_producto.bind("<KeyRelease>", filtrar_opciones)

    ttk.Label(ventana_producto, text="Cantidad:").pack(pady=10)
    campo_cantidad = ttk.Entry(ventana_producto)
    campo_cantidad.pack(pady=5)

    ttk.Label(ventana_producto, text="Precio Unitario:").pack(pady=10)
    campo_precio = ttk.Entry(ventana_producto)
    campo_precio.pack(pady=5)
    campo_precio.insert(0, "0")  # Valor inicial

    ttk.Label(ventana_producto, text="Color:").pack(pady=10)
    campo_color = ttk.Entry(ventana_producto)
    campo_color.pack(pady=5)

    ttk.Label(ventana_producto, text="Talla:").pack(pady=10)
    campo_talla = ttk.Entry(ventana_producto)
    campo_talla.pack(pady=5)

    # Función para actualizar precio inicial automáticamente
    def actualizar_precio_inicial(*args):
        try:
            producto_seleccionado = var_producto.get().split(" - ")[0]
            if producto_seleccionado.isdigit():
                producto = sm.obtener_producto_por_id(int(producto_seleccionado))
                if producto and producto.precio_inicial:
                    campo_precio.delete(0, tk.END)
                    campo_precio.insert(0, str(producto.precio_inicial))
        except:
            pass

    # Asociar el evento para actualizar precio al cambiar producto
    var_producto.trace_add("write", actualizar_precio_inicial)

    def confirmar_agregar():
        try:
            producto_seleccionado = var_producto.get().split(" - ")[0]
            cantidad = int(campo_cantidad.get())
            precio_unitario = float(campo_precio.get())
            color = campo_color.get()
            talla = campo_talla.get()
            subtotal = round(cantidad * precio_unitario, 2)
            #print(f"El subtotal es: {subtotal}. Que es la multiplicación de {cantidad} * {precio_unitario}")

            producto = sm.obtener_producto_por_id(producto_seleccionado)
            tabla_modificar.insert("", "end", values=(
                producto.id_producto,
                producto.nombre,
                cantidad,
                precio_unitario,
                color,
                talla,
                subtotal
            ))
            ventana_producto.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    ttk.Button(ventana_producto, text="Agregar Producto", command=confirmar_agregar).pack(pady=20)

def mostrar_interfaz_ventas():
    limpiar_ventana()

    # Crear un Canvas dentro de frame_contenido
    canvas = tk.Canvas(frame_contenido, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Crear un scrollbar y enlazarlo al canvas
    scrollbar = ttk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un frame dentro del canvas que contendrá todo el contenido
    sub_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=sub_frame, anchor="nw")

    # Configuración de auto-ajuste de la región de scroll
    sub_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Vincular el evento de la rueda del ratón al canvas para desplazarse desde cualquier área
    def on_mouse_wheel(event):
        scroll_pos = canvas.yview()
        if (event.delta > 0 and scroll_pos[0] <= 0) or (event.delta < 0 and scroll_pos[1] >= 1):
            return
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Etiqueta para la interfaz de ventas
    etiqueta_ventas = ttk.Label(sub_frame, text="Gestión de Ventas", font=("Arial", 16))
    etiqueta_ventas.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Campo de filtro por columnas
    filtros = {}
    columnas = ("ID Venta", "Cliente", "Fecha", "Total")

    for i, col in enumerate(columnas[:-2]):  # Solo iterar por "ID Venta" y "Cliente"
        etiqueta_filtro = ttk.Label(sub_frame, text=f"Filtrar {col}:", font=("Arial", 12))
        etiqueta_filtro.grid(row=1, column=i, padx=5, pady=5)
        filtros[col] = ttk.Entry(sub_frame)
        filtros[col].grid(row=2, column=i, padx=5, pady=5)

    # Agregar filtros de Fecha Inicio y Fecha Fin con DateEntry
    etiqueta_fecha_inicio = ttk.Label(sub_frame, text="Fecha Inicio:", font=("Arial", 12))
    etiqueta_fecha_inicio.grid(row=1, column=2, padx=5, pady=5)
    filtros["Fecha Inicio"] = tb.DateEntry(sub_frame)
    filtros["Fecha Inicio"].grid(row=2, column=2, padx=5, pady=5)

    etiqueta_fecha_fin = ttk.Label(sub_frame, text="Fecha Fin:", font=("Arial", 12))
    etiqueta_fecha_fin.grid(row=1, column=3, padx=5, pady=5)
    filtros["Fecha Fin"] = tb.DateEntry(sub_frame)
    filtros["Fecha Fin"].grid(row=2, column=3, padx=5, pady=5)

    # Crear un frame para la tabla y su scrollbar
    frame_tabla = ttk.Frame(sub_frame)
    frame_tabla.grid(row=3, column=0, columnspan=len(columnas), padx=10, pady=10, sticky="nsew")

    # Crear el Treeview (tabla)
    tabla_ventas = ttk.Treeview(frame_tabla, columns=columnas, show='headings', height=30)
    for col in columnas:
        if col == "Cliente":
            tabla_ventas.heading(col, text=col)
            tabla_ventas.column(col, width=500, anchor="center")
        else:
            tabla_ventas.heading(col, text=col)
            tabla_ventas.column(col, width=220, anchor="center")

    # Scrollbar vertical para la tabla
    scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_ventas.yview)
    tabla_ventas.configure(yscrollcommand=scrollbar_tabla.set)

    # Posicionar el Treeview y su scrollbar en el frame
    tabla_ventas.pack(side="left", fill="both", expand=True)
    scrollbar_tabla.pack(side="right", fill="y")

    # Llenar la tabla con las notas de venta canceladas
    def cargar_ventas(filtros_activos=None):
        # Limpiar la tabla antes de cargar nuevos datos
        tabla_ventas.delete(*tabla_ventas.get_children())

        # Inicializar filtros si es None
        filtros_activos = filtros_activos or {}

        # Manejo de fechas con validación
        try:
            if "Fecha Inicio" in filtros_activos and filtros_activos["Fecha Inicio"]:
                filtros_activos["Fecha Inicio"] = datetime.strptime(filtros_activos["Fecha Inicio"], "%d/%m/%Y")
            if "Fecha Fin" in filtros_activos and filtros_activos["Fecha Fin"]:
                filtros_activos["Fecha Fin"] = datetime.strptime(filtros_activos["Fecha Fin"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese fechas en el formato correcto (DD/MM/YYYY).")
            return

        # Obtener las notas filtradas (incluyendo nombre del cliente en la consulta)
        ventas = sm.obtener_notas_filtradas(filtros_activos)

        # Insertar datos en la tabla
        for venta in ventas:
            tabla_ventas.insert("", "end", values=(venta.id_nota, venta.nombre_cliente, venta.fecha_venta, venta.total))


    cargar_ventas()

    # Función para aplicar filtros
    def aplicar_filtros():
        filtros_activos = {
            col: (filtros[col].entry.get() if col in ["Fecha Inicio", "Fecha Fin"] else filtros[col].get())
            for col in filtros
    }
        cargar_ventas(filtros_activos)

    # Botón para aplicar los filtros
    boton_filtrar = ttk.Button(sub_frame, text="Aplicar Filtros", command=aplicar_filtros)
    boton_filtrar.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Botón para restablecer los filtros
    def restablecer_filtros():
        for col, widget in filtros.items():
            if isinstance(widget, tb.DateEntry):
                widget.entry.delete(0, tk.END)  # Limpiar DateEntry
            elif isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)  # Limpiar Entry
        cargar_ventas()


    boton_restablecer = ttk.Button(sub_frame, text="Restablecer Filtros", command=restablecer_filtros)
    boton_restablecer.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Función para ver detalles de una venta
    def ver_detalles_venta():
        selected_item = tabla_ventas.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar una venta para ver los detalles.")
            return

        venta_seleccionada = tabla_ventas.item(selected_item, 'values')
        id_venta = venta_seleccionada[0]

        ventana_detalles_nota(id_venta, "ventas")  # Reutilizamos ventana_detalles_nota para visualización

    # Botón para ver los detalles de la venta seleccionada
    boton_ver_detalles = ttk.Button(sub_frame, text="Ver Detalles", command=ver_detalles_venta)
    boton_ver_detalles.grid(row=4, column=2, padx=10, pady=10, sticky="w")

def verificar_contraseña():
    contraseña_correcta = "0308"  # Cambia esta contraseña según lo necesites
    contraseña_ingresada = simpledialog.askstring("Acceso Restringido", "Ingrese la contraseña para acceder a las ganacias:", show='*')

    if contraseña_ingresada == contraseña_correcta:
        mostrar_interfaz_ganancia()
    elif contraseña_ingresada is not None:  # Evitar mensaje si el usuario cierra el diálogo
        messagebox.showerror("Acceso Denegado", "Contraseña incorrecta. Intente nuevamente.")


def mostrar_interfaz_ganancia():
    # Limpiar ventana
    limpiar_ventana()

    # Crear fecha de inicio y fin
    etiqueta_inicio = tb.Label(frame_contenido, text="Fecha Inicio:")
    etiqueta_inicio.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    campo_inicio = tb.DateEntry(frame_contenido)
    campo_inicio.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_fin = tb.Label(frame_contenido, text="Fecha Fin:")
    etiqueta_fin.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    campo_fin = tb.DateEntry(frame_contenido)
    campo_fin.grid(row=1, column=1, padx=10, pady=10)

    # Botón para generar el reporte
    def generar_reporte():
        fecha_inicio = campo_inicio.entry.get()
        fecha_fin = campo_fin.entry.get()

        try:
            # Validar formato de fecha
            fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese fechas en el formato correcto (YYYY-MM-DD).")
            return

        # Filtrar las ventas por fecha (en base de datos o usando ORM)
        ventas = sm.obtener_ventas_por_fecha(fecha_inicio, fecha_fin)
        if not ventas:
            messagebox.showinfo("Reporte", "No se encontraron ventas en el rango de fechas seleccionado.")
            return

        # Calcular las métricas
        ganancias = sm.calcular_ganancia(ventas)
        total_ventas = sm.calcular_total(ventas)
        total_costos = sm.calcular_costo_total(ventas)
        productos_vendidos = sm.obtener_productos_vendidos(ventas)

        # Calcular la cantidad total de prendas vendidas
        total_prendas_vendidas = sum(producto['cantidad'] for producto in productos_vendidos)

        # Crear un frame para las métricas
        frame_metricas = ttk.Frame(frame_contenido)
        frame_metricas.grid(row=3, column=2, padx=20, pady=10, sticky="n")

        # Etiqueta de Ganancia Total
        etiqueta_ganancia = ttk.Label(frame_metricas, text=f"Ganancia Total:\nS/.{ganancias:,.2f}", font=("Arial", 12, "bold"))
        etiqueta_ganancia.pack(pady=5, anchor="w")

        # Etiqueta de Total de Ventas
        etiqueta_total_ventas = ttk.Label(frame_metricas, text=f"Total Ventas:\nS/.{total_ventas:,.2f}", font=("Arial", 12, "bold"))
        etiqueta_total_ventas.pack(pady=5, anchor="w")

        # Etiqueta de Total de Costos
        etiqueta_total_costos = ttk.Label(frame_metricas, text=f"Total Costos:\nS/.{total_costos:,.2f}", font=("Arial", 12, "bold"))
        etiqueta_total_costos.pack(pady=5, anchor="w")

        # Etiqueta para Cantidad Total de Prendas Vendidas
        etiqueta_prendas_vendidas = ttk.Label(frame_metricas, text=f"Prendas Vendidas:\n{total_prendas_vendidas:,}", font=("Arial", 12, "bold"))
        etiqueta_prendas_vendidas.pack(pady=5, anchor="w")

        # Tabla con nuevas columnas: Costo del Producto y Utilidad
        columnas_productos = ("Nombre", "Cantidad", "Precio Unitario", "Costo", "Subtotal", "Utilidad")
        tabla_productos = ttk.Treeview(frame_contenido, columns=columnas_productos, show='headings', height=35)
        
        # Encabezados
        tabla_productos.heading("Nombre", text="Nombre")
        tabla_productos.heading("Cantidad", text="Cantidad")
        tabla_productos.heading("Precio Unitario", text="Precio Unitario")
        tabla_productos.heading("Costo", text="Costo del Producto")
        tabla_productos.heading("Subtotal", text="Subtotal")
        tabla_productos.heading("Utilidad", text="Utilidad")

        # Ajustar tamaño de columnas
        tabla_productos.column("Nombre", width=200+50, anchor="center")
        tabla_productos.column("Cantidad", width=100+50, anchor="center"), 
        tabla_productos.column("Precio Unitario", width=100+50, anchor="center")
        tabla_productos.column("Costo", width=100+50, anchor="center")
        tabla_productos.column("Subtotal", width=100+50, anchor="center")
        tabla_productos.column("Utilidad", width=100+50, anchor="center")

        tabla_productos.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Insertar datos en la tabla
        for producto in productos_vendidos:
            costo = producto['costo']
            precio_unitario = producto['precio_unitario']
            utilidad = (precio_unitario - costo) * producto['cantidad']
            
            tabla_productos.insert("", "end", values=(
                producto['producto'],  # Nombre del producto
                producto['cantidad'],  # Cantidad vendida
                f"S/.{precio_unitario:.2f}",  # Precio unitario
                f"S/.{costo:.2f}",  # Costo del producto
                f"S/.{producto['subtotal']:.2f}",  # Subtotal
                f"S/.{utilidad:.2f}",  # Utilidad
            ))

    boton_generar_reporte = ttk.Button(frame_contenido, text="Generar Reporte", command=generar_reporte)
    boton_generar_reporte.grid(row=1, column=2, padx=10, pady=10)



def imprimir_nota_venta(nota, detalles, cliente):
    """
    Genera un PDF para una nota de venta y abre el archivo para impresión.
    """
    # Ruta de la carpeta 'notas de venta'
    carpeta = "notas de venta"

    # Verificar si la carpeta existe, si no, crearla
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    pdf_nombre = os.path.join(carpeta, f"Nota_Venta_{nota.id_nota}.pdf")
    
    # Crear el PDF
    c = canvas.Canvas(pdf_nombre, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Encabezado
    c.drawString(100, 750, "Sexy Boom")
    c.drawString(100, 735, f"Nota de Venta ID: {nota.id_nota}")
    c.drawString(100, 720, f"Cliente: {cliente.nombre}")
    c.drawString(100, 705, f"Fecha: {nota.fecha}")
    c.drawString(100, 690, f"Estado: {nota.estado}")

    # **Calcular la posición inicial de la tabla**
    y = 600  # Justo debajo del estado, con un pequeño margen

    # Encabezados
    encabezados = ["ID Producto", "Nombre", "Precio Unitario", "Cantidad", "Color", "Talla", "Subtotal"]
    data = [encabezados]

    # Filas de detalles
    for detalle in detalles:
        producto = sm.obtener_producto_por_id(detalle.id_producto)
        
        # Convertir los colores en una lista y separarlos en líneas dentro de la celda
        colores = detalle.color if producto else "N/A"
        colores_multilinea = "\n".join(colores.split(", "))  # Agregar saltos de línea entre colores
        
        data.append([
            str(detalle.id_producto),
            producto.nombre if producto else "Desconocido",
            f"{detalle.precio_unitario:.2f}" if producto else "0.00",
            str(detalle.cantidad),
            colores_multilinea,  # Colores en varias líneas
            detalle.talla if producto else "N/A",
            f"{detalle.subtotal:.2f}"
        ])

    # Definir tabla con el nuevo ancho para la columna de colores (70 en lugar de 150)
    table = Table(data, colWidths=[70, 120, 80, 60, 70, 70, 80])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),  # Reducir fuente solo en los datos
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Ajustar posición de la tabla
    table.wrapOn(c, 50, y)
    table.drawOn(c, 50, y - len(data) * 18)  # Se usa 18 en vez de 20 para mejorar el ajuste

    # **Calcular nueva posición para el total**
    y -= len(data) * 18 + 30  # Ajusta la posición en función de la tabla
    c.drawString(400, y, "Total:")
    c.drawString(500, y, f"{nota.total:.2f}")

    # Guardar en carpeta y abrir el archivo
    c.save()
    os.startfile(pdf_nombre)


def mostrar_interfaz_reporte_mensual():
    limpiar_ventana()

    cont = ttk.Frame(frame_contenido, padding=10)
    cont.pack(fill="both", expand=True)

    # --- Controles de filtro ---
    filtros = ttk.LabelFrame(cont, text="Filtros", padding=10)
    filtros.pack(fill="x", pady=5)

    modo = tk.StringVar(value="mes")  # "mes" | "rango"
    ttk.Radiobutton(filtros, text="Por mes", variable=modo, value="mes").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Radiobutton(filtros, text="Por rango", variable=modo, value="rango").grid(row=0, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(filtros, text="Mes (1-12):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_mes = ttk.Combobox(filtros, values=[str(i) for i in range(1,13)], width=5, state="readonly")
    combo_mes.set("6")  # por defecto junio
    combo_mes.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(filtros, text="Año:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    spin_anio = ttk.Spinbox(filtros, from_=2000, to=2100, width=6)
    spin_anio.delete(0, tk.END)
    spin_anio.insert(0, "2025")  # por defecto 2025
    spin_anio.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    ttk.Label(filtros, text="Desde (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_desde = ttk.Entry(filtros, width=12)
    entry_desde.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(filtros, text="Hasta (YYYY-MM-DD):").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entry_hasta = ttk.Entry(filtros, width=12)
    entry_hasta.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # --- Botones acciones ---
    acciones = ttk.Frame(cont)
    acciones.pack(fill="x", pady=5)
    btn_generar = ttk.Button(acciones, text="Generar reporte")
    btn_generar.pack(side="left", padx=5)
    btn_exportar = ttk.Button(acciones, text="Exportar a Excel")
    btn_exportar.pack(side="left", padx=5)

    # --- Tabla ---
    columnas = ("ID Nota", "Producto", "Cliente", "Cantidad", "Precio Unitario", "Total por Nota", "Fecha Venta")
    frame_tabla = ttk.Frame(cont)
    frame_tabla.pack(fill="both", expand=True, pady=5)

    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=28)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=140, anchor="center")
    tabla.column("Producto", width=220)
    tabla.column("Cliente", width=200)

    sbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=sbar.set)
    tabla.pack(side="left", fill="both", expand=True)
    sbar.pack(side="right", fill="y")

    resultados_cache = []

    def parse_fecha(txt):
        txt = txt.strip()
        if not txt:
            return None
        return datetime.strptime(txt, "%Y-%m-%d").date()

    def cargar_datos():
        nonlocal resultados_cache
        # limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        if modo.get() == "rango":
            f_desde = parse_fecha(entry_desde.get())
            f_hasta = parse_fecha(entry_hasta.get())
            if not (f_desde and f_hasta):
                messagebox.showwarning("Atención", "Completa fechas 'Desde' y 'Hasta' en formato YYYY-MM-DD.")
                return
            resultados = sm.obtener_reporte(fecha_desde=f_desde, fecha_hasta=f_hasta)
        else:
            try:
                m = int(combo_mes.get())
                a = int(spin_anio.get())
            except ValueError:
                messagebox.showwarning("Atención", "Mes y año deben ser numéricos.")
                return
            resultados = sm.obtener_reporte(mes=m, anio=a)

        resultados_cache = resultados

        for r in resultados:
            fila = (
                r.id_nota_venta,
                r.producto,
                r.cliente,
                int(r.cantidad) if r.cantidad is not None else "",
                float(r.precio_unitario) if r.precio_unitario is not None else "",
                float(r.total_por_nota) if r.total_por_nota is not None else "",
                r.fecha_venta.strftime("%Y-%m-%d") if r.fecha_venta else ""
            )
            tabla.insert("", "end", values=fila)

        messagebox.showinfo("Reporte", f"Se listaron {len(resultados)} registros.")

    def exportar_excel():
        if not resultados_cache:
            messagebox.showwarning("Atención", "No hay datos para exportar. Genera el reporte primero.")
            return
        datos = [{
            "ID Nota": r.id_nota_venta,
            "Producto": r.producto,
            "Cliente": r.cliente,
            "Cantidad": int(r.cantidad) if r.cantidad is not None else None,
            "Precio Unitario": float(r.precio_unitario) if r.precio_unitario is not None else None,
            "Total por Nota": float(r.total_por_nota) if r.total_por_nota is not None else None,
            "Fecha Venta": r.fecha_venta.strftime("%Y-%m-%d") if r.fecha_venta else None
        } for r in resultados_cache]
        df = pd.DataFrame(datos)
        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="reporte_notas_venta.xlsx"
        )
        if ruta:
            df.to_excel(ruta, index=False)
            messagebox.showinfo("Éxito", f"Reporte exportado en:\n{ruta}")

    btn_generar.config(command=cargar_datos)
    btn_exportar.config(command=exportar_excel)

    # Generar por defecto (junio 2025)
    cargar_datos()

# ---------- Ventana principal ----------
def interfaz_principal(ventana_root):
    global frame_contenido
    ventana_root.deiconify()  # Mostrar la ventana principal si estaba oculta
    ventana_root.title("Sexy Boom v1.1")
    ventana_root.state("zoomed")
    ventana_root.resizable(True, True)

    ruta_icono = obtener_ruta_recurso("sexyboom.ico")
    ventana_root.iconbitmap(ruta_icono)

    frame_botones = ttk.Frame(ventana_root, padding=20)
    frame_botones.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

    botones = [
        ("Gestionar Clientes", mostrar_interfaz_clientes),
        ("Gestionar Productos", mostrar_interfaz_productos),
        ("Gestionar Nota de Venta", mostrar_interfaz_nota_venta),
        ("Ver Ventas", mostrar_interfaz_ventas),
        ("Ganancia", verificar_contraseña),
        ("Reporte Mensual", mostrar_interfaz_reporte_mensual),
        ("Salir", ventana_root.quit)
    ]

    for i, (texto, comando) in enumerate(botones):
        boton = ttk.Button(frame_botones, text=texto, width=30, padding=10, command=comando)
        boton.grid(row=i, column=0, pady=15, padx=10, sticky="ew")

    frame_contenido = ttk.Frame(ventana_root, padding=30)
    frame_contenido.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    ventana_root.columnconfigure(1, weight=1)
    ventana_root.rowconfigure(0, weight=1)

# ---------- Login ----------
def login(ventana_root):
    login_win = tk.Toplevel(ventana_root)
    login_win.title("Iniciar sesión")
    centrar_ventana(login_win, 0.15, 0.20)  # Centrar ventana de login
    login_win.grab_set()  # Bloquear interacción con la principal

    def cerrar_todo():
        ventana_root.destroy()  # Cierra toda la app

    # Si cierran la ventana con la X → cerrar app
    login_win.protocol("WM_DELETE_WINDOW", cerrar_todo)

    tk.Label(login_win, text="Usuario:").pack(pady=5)
    entry_user = tk.Entry(login_win)
    entry_user.pack()

    tk.Label(login_win, text="Contraseña:").pack(pady=5)
    entry_pass = tk.Entry(login_win, show="*")
    entry_pass.pack()

    def verificar():
        if entry_user.get() == "admin" and entry_pass.get() == "2308": 
            login_win.destroy()
            interfaz_principal(ventana_root)  # Mostrar interfaz principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    tk.Button(login_win, text="Entrar", command=verificar).pack(pady=15)




def obtener_ruta_recurso(rel_path):
    """ Devuelve la ruta correcta para acceder a archivos empaquetados con PyInstaller. """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Directorio temporal de PyInstaller
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

def obtener_factor_escala(ventana):
    """
    Obtiene el factor de escala DPI del sistema operativo.
    """
    return ventana.tk.call('tk', 'scaling')

def aplicar_escala_dpi(ventana, factor_escala):
    """
    Ajusta el tamaño de las fuentes y widgets basado en el factor de escala.
    """
    ventana.tk.call("tk", "scaling", factor_escala)
def ajustar_dimensiones(ventana, ancho_pct, alto_pct):
    """
    Ajusta las dimensiones de la ventana en función del porcentaje del tamaño de la pantalla.
    """
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ancho = int(ancho_pantalla * ancho_pct)
    alto = int(alto_pantalla * alto_pct)
    ventana.geometry(f"{ancho}x{alto}")


# ---------- Inicio ----------
if __name__ == "__main__":
    root = tb.Window(themename="minty")  # Solo una vez en toda la app
    root.withdraw()  # Ocultar al inicio
    login(root)
    root.mainloop()