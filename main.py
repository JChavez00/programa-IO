import tkinter as tk
from tkinter import ttk, messagebox

def calcular_probabilidades():
    try:
        # 1. Leer los datos de entrada desde las cajas de texto
        prob_demanda = {
            0: float(entry_dem_0.get()),
            1: float(entry_dem_1.get()),
            2: float(entry_dem_2.get()),
            3: float(entry_dem_3.get())
        }
        
        prob_demora = {
            1: float(entry_demora_1.get()),
            2: float(entry_demora_2.get()),
            3: float(entry_demora_3.get())
        }
        
        # Opcional: Validar que las probabilidades sumen 1 (o cerca de 1 por decimales)
        suma_demanda = sum(prob_demanda.values())
        suma_demora = sum(prob_demora.values())
        if round(suma_demanda, 2) != 1.00 or round(suma_demora, 2) != 1.00:
            messagebox.showwarning("Advertencia", "Las probabilidades deberían sumar 1.00\nRevisa tus datos.")
            
    except ValueError:
        messagebox.showerror("Error de formato", "Por favor, ingresa solo números válidos (usa punto para decimales).")
        return

    # 2. Diccionario para almacenar la probabilidad total
    prob_total = {i: 0.0 for i in range(10)}

    # 3. Cálculos combinatorios
    # Demora de 1 día
    for d1, p_d1 in prob_demanda.items():
        prob_total[d1] += p_d1 * prob_demora[1]

    # Demora de 2 días
    for d1, p_d1 in prob_demanda.items():
        for d2, p_d2 in prob_demanda.items():
            prob_total[d1 + d2] += p_d1 * p_d2 * prob_demora[2]

    # Demora de 3 días
    for d1, p_d1 in prob_demanda.items():
        for d2, p_d2 in prob_demanda.items():
            for d3, p_d3 in prob_demanda.items():
                prob_total[d1 + d2 + d3] += p_d1 * p_d2 * p_d3 * prob_demora[3]

    # 4. Calcular probabilidad acumulada (de 9 a 0)
    prob_acumulada = {}
    acumulado = 0.0
    for i in range(9, -1, -1):
        acumulado += prob_total[i]
        prob_acumulada[i] = acumulado

    # 5. Limpiar la tabla
    for row in tabla.get_children():
        tabla.delete(row)

    # 6. Insertar los datos calculados en la tabla
    for i in range(9, -1, -1):
        prob_formateada = f"{prob_total[i]:.4f}"
        acum_formateada = f"{prob_acumulada[i]:.4f}"
        tabla.insert("", "end", values=(i, prob_formateada, acum_formateada))


# --- CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (GUI) ---
root = tk.Tk()
root.title("Calculadora de Inventario Estocástico")
root.geometry("550x650")
root.configure(padx=20, pady=20)

titulo_label = tk.Label(root, text="Modelo de Revisión Continua", font=("Arial", 14, "bold"))
titulo_label.pack(pady=(0, 15))

# --- SECCIÓN DE ENTRADA DE DATOS ---
frame_entradas = tk.Frame(root)
frame_entradas.pack(fill=tk.X, pady=10)

# Panel izquierdo: Probabilidades de Demanda
frame_demanda = tk.LabelFrame(frame_entradas, text="Probabilidades de Demanda (Día)", font=("Arial", 10, "bold"), padx=10, pady=10)
frame_demanda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

tk.Label(frame_demanda, text="0 Unidades:").grid(row=0, column=0, sticky="e", pady=2)
entry_dem_0 = tk.Entry(frame_demanda, width=8)
entry_dem_0.insert(0, "0.40") # Valor por defecto
entry_dem_0.grid(row=0, column=1, pady=2)

tk.Label(frame_demanda, text="1 Unidad:").grid(row=1, column=0, sticky="e", pady=2)
entry_dem_1 = tk.Entry(frame_demanda, width=8)
entry_dem_1.insert(0, "0.30")
entry_dem_1.grid(row=1, column=1, pady=2)

tk.Label(frame_demanda, text="2 Unidades:").grid(row=2, column=0, sticky="e", pady=2)
entry_dem_2 = tk.Entry(frame_demanda, width=8)
entry_dem_2.insert(0, "0.20")
entry_dem_2.grid(row=2, column=1, pady=2)

tk.Label(frame_demanda, text="3 Unidades:").grid(row=3, column=0, sticky="e", pady=2)
entry_dem_3 = tk.Entry(frame_demanda, width=8)
entry_dem_3.insert(0, "0.10")
entry_dem_3.grid(row=3, column=1, pady=2)

# Panel derecho: Probabilidades de Demora
frame_demora = tk.LabelFrame(frame_entradas, text="Probabilidades de Demora", font=("Arial", 10, "bold"), padx=10, pady=10)
frame_demora.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(frame_demora, text="1 Día:").grid(row=0, column=0, sticky="e", pady=2)
entry_demora_1 = tk.Entry(frame_demora, width=8)
entry_demora_1.insert(0, "0.25")
entry_demora_1.grid(row=0, column=1, pady=2)

tk.Label(frame_demora, text="2 Días:").grid(row=1, column=0, sticky="e", pady=2)
entry_demora_2 = tk.Entry(frame_demora, width=8)
entry_demora_2.insert(0, "0.50")
entry_demora_2.grid(row=1, column=1, pady=2)

tk.Label(frame_demora, text="3 Días:").grid(row=2, column=0, sticky="e", pady=2)
entry_demora_3 = tk.Entry(frame_demora, width=8)
entry_demora_3.insert(0, "0.25")
entry_demora_3.grid(row=2, column=1, pady=2)

# Botón para ejecutar el cálculo
boton_calcular = tk.Button(root, text="Actualizar y Calcular", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", command=calcular_probabilidades)
boton_calcular.pack(pady=15)

# --- SECCIÓN DE RESULTADOS ---
frame_tabla = tk.LabelFrame(root, text="Tabla Acumulada de Resultados", font=("Arial", 10, "bold"), padx=10, pady=10)
frame_tabla.pack(fill=tk.BOTH, expand=True)

columnas = ("demanda", "probabilidad", "acumulada")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

tabla.heading("demanda", text="Demanda Total")
tabla.heading("probabilidad", text="Probabilidad")
tabla.heading("acumulada", text="Prob. Acumulada")

tabla.column("demanda", anchor=tk.CENTER, width=120)
tabla.column("probabilidad", anchor=tk.CENTER, width=120)
tabla.column("acumulada", anchor=tk.CENTER, width=120)

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Iniciar el programa
root.mainloop()