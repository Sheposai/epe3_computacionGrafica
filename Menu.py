import sqlite3
import csv
import random
from datetime import datetime, timedelta

# Crear la base de datos 
def crear_base_de_datos():
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        producto TEXT,
        categoria TEXT,
        precio REAL,
        cantidad INTEGER,
        total REAL)
    ''')
    conn.commit()
    conn.close()

# Productos predefinidos
productos = [
    {'nombre': 'Televisor', 'categoria': 'Electrónica', 'precio': 199990},
    {'nombre': 'Celular', 'categoria': 'Electrónica', 'precio': 149000},
    {'nombre': 'Laptop', 'categoria': 'Electrónica', 'precio': 500000},
    {'nombre': 'Camiseta', 'categoria': 'Ropa', 'precio': 10000},
    {'nombre': 'Jeans', 'categoria': 'Ropa', 'precio': 25000},
    {'nombre': 'Vestido', 'categoria': 'Ropa', 'precio': 30000},
    {'nombre': 'Silla', 'categoria': 'Hogar', 'precio': 20000},
    {'nombre': 'Mesa', 'categoria': 'Hogar', 'precio': 50000},
    {'nombre': 'Lámpara', 'categoria': 'Hogar', 'precio': 15000},
    {'nombre': 'Muñeca', 'categoria': 'Juguetes', 'precio': 8000},
    {'nombre': 'Pelota', 'categoria': 'Juguetes', 'precio': 6000},
    {'nombre': 'Rompecabezas', 'categoria': 'Juguetes', 'precio': 12000},
    {'nombre': 'Libro de aventuras', 'categoria': 'Libros', 'precio': 10000},
    {'nombre': 'Libro de cocina', 'categoria': 'Libros', 'precio': 15000},
    {'nombre': 'Libro de ciencia ficción', 'categoria': 'Libros', 'precio': 20000},
]


# ingresar un nuevo registro de venta
def agregar_venta():
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    
    fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        print("Fecha no válida. Inténtelo de nuevo.")
        return
    
    print("Seleccione el producto:")
    for idx, producto in enumerate(productos):
        print(f"{idx + 1}. {producto['nombre']} ({producto['categoria']}) - ${producto['precio']}")
    
    try:
        producto_opcion = int(input("Ingrese el número del producto: "))
        if producto_opcion < 1 or producto_opcion > len(productos):
            print("Opción no válida. Inténtelo de nuevo.")
            return
    except ValueError:
        print("Opción no válida. Inténtelo de nuevo.")
        return
    
    producto_seleccionado = productos[producto_opcion - 1]
    nombre_producto = producto_seleccionado['nombre']
    categoria = producto_seleccionado['categoria']
    precio = producto_seleccionado['precio']
    
    try:
        cantidad = int(input("Ingrese la cantidad vendida: "))
    except ValueError:
        print("Cantidad no válida. Inténtelo de nuevo.")
        return
    
    total = precio * cantidad
    
    cursor.execute('''
    INSERT INTO ventas (fecha, producto, categoria, precio, cantidad, total)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (fecha, nombre_producto, categoria, precio, cantidad, total))
    
    conn.commit()
    conn.close()
    print("Venta registrada con éxito.")

# exportar los datos a un archivo CSV
def exportar_a_csv():
    conn = sqlite3.connect('ventas.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ventas")
    rows = cursor.fetchall()
    
    with open('ventas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])  # Escribir los encabezados
        writer.writerows(rows)
    
    conn.close()
    print("Datos exportados a ventas.csv con éxito.")

# preguntar si se desea continuar
def desea_continuar():
    while True:
        continuar = input("¿Desea continuar? (s/n): ").lower()
        if continuar in ['s', 'n']:
            return continuar == 's'
        else:
            print("Opción no válida. Por favor, ingrese 's' para sí o 'n' para no.")

# Menú principal
def menu():
  
    while True:
        print("\nMenú Principal")
        print("1. Ingresar una nueva venta")
        print("2. Exportar datos a CSV")
        print("3. Salir")
        
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Opción no válida. Inténtelo de nuevo.")
            continue
        
        if opcion == 1:
            agregar_venta()
        elif opcion == 2:
            exportar_a_csv()
        elif opcion == 3:
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")
        
        if not desea_continuar():
            print("Saliendo del programa.")
            break

# Ejecutar  menú
if __name__ == "__main__":
    menu()
