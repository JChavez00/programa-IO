# main.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# Importamos las funciones matemáticas de nuestro otro archivo
from calculos import calcular_probabilidades, calcular_esperanza_y_costos

def ejecutar_programa():
    try:
        # --- 1. LEER DATOS DE LA PESTAÑA DE ENTRADA ---
        prob_demanda = {
            0: float(entry_dem_0.get()), 1: float(entry_dem_1.get()),
            2: float(entry_dem_2.get()), 3: float(entry_dem_3.get())
        }
        prob_demora = {
            1: float(entry_demora_1.get()), 2: float(entry_demora_2.get()), 3: float(entry_demora_3.get())
        }
        
        # Leer variables de costos
        q1 = float(entry_q1.get())
        q2 = float(entry_q2.get())
        q3 = float(entry_q3.get())
        beta = float(entry_beta.get())
        y = float(entry_y.get())
        delta_y = float(entry_delta_y.get())

        # --- 2. LLAMAR A LAS FUNCIONES MATEMÁTICAS ---
        # Calculamos probabilidades (Tabla 1)
        prob_total, prob_acumulada = calcular_probabilidades(prob_demanda, prob_demora)
        
        # Calculamos costos y E(D) (Tabla 2)
        resultados_costos = calcular_esperanza_y_costos(prob_total, q1, q2, q3, beta, y, delta_y)

        # --- 3. ACTUALIZAR LAS TABLAS EN LA INTERFAZ ---
        # Limpiar tablas
        for row in tabla_prob.get_children(): tabla_prob.delete(row)
        for row in tabla_costos.get_children(): tabla_costos.delete(row)

        # Llenar Tabla 1
        for i in range(9, -1, -1):
            tabla_prob.insert("", "end", values=(i, f"{prob_total[i]:.4f}", f"{prob_acumulada[i]:.4f}"))
            
        # Llenar Tabla 2 y guardar datos para el gráfico
        global lista_R, lista_Costos # Globales para usarlas en la función del gráfico
        lista_R = []
        lista_Costos = []
        
        for r in range(9, 0, -1):
            e_d = resultados_costos[r]["E(D)"]
            costo = resultados_costos[r]["Costo"]
            tabla_costos.insert("", "end", values=(r, f"{e_d:.4f}", f"${costo:.2f}"))
            
            # Guardamos para matplotlib (invertimos para que el eje X vaya de menor a mayor)
            lista_R.insert(0, r) 
            lista_Costos.insert(0, costo)

        # Cambiar a la pestaña de resultados automáticamente
        notebook.select(tab_resultados)
        boton_grafico.config(state="normal") # Habilitar botón de gráfico

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")

def mostrar_grafico():
    # Usamos matplotlib para dibujar la curva
    plt.figure(figsize=(7, 5))
    plt.plot(lista_R, lista_Costos, marker='o', linestyle='-', color='#E91E63', linewidth=2)
    
    # Encontrar el R óptimo (el mínimo costo)
    costo_minimo = min(lista_Costos)
    r_optimo = lista_R[lista_Costos.index(costo_minimo)]
    
    # Resaltar el punto óptimo
    plt.plot(r_optimo, costo_minimo, marker='o', markersize=10, color='blue', label=f'R Óptimo = {r_optimo}')
    
    plt.title('Costo Total vs Punto de Reorden (R)', fontsize=14)
    plt.xlabel('Punto de Reorden (R)', fontsize=12)
    plt.ylabel('Costo Total ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- CONFIGURACIÓN DE LA INTERFAZ ---
root = tk.Tk()
root.title("Modelo de Inventario Estocástico")
root.geometry("600x650")

# Sistema de Pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

tab_datos = ttk.Frame(notebook)
tab_resultados = ttk.Frame(notebook)

notebook.add(tab_datos, text='1. Ingreso de Datos')
notebook.add(tab_resultados, text='2. Tablas y Gráfica')

# ================= PESTAÑA 1: DATOS =================
frame_prob = tk.LabelFrame(tab_datos, text="Probabilidades")
frame_prob.pack(fill='x', padx=10, pady=5)

# (Simplificación visual del código para demanda y demora)
tk.Label(frame_prob, text="Demanda (0,1,2,3):").grid(row=0, column=0, pady=5, padx=5)
entry_dem_0 = tk.Entry(frame_prob, width=6); entry_dem_0.insert(0, "0.40"); entry_dem_0.grid(row=0, column=1)
entry_dem_1 = tk.Entry(frame_prob, width=6); entry_dem_1.insert(0, "0.30"); entry_dem_1.grid(row=0, column=2)
entry_dem_2 = tk.Entry(frame_prob, width=6); entry_dem_2.insert(0, "0.20"); entry_dem_2.grid(row=0, column=3)
entry_dem_3 = tk.Entry(frame_prob, width=6); entry_dem_3.insert(0, "0.10"); entry_dem_3.grid(row=0, column=4)

tk.Label(frame_prob, text="Demora (1,2,3 días):").grid(row=1, column=0, pady=5, padx=5)
entry_demora_1 = tk.Entry(frame_prob, width=6); entry_demora_1.insert(0, "0.25"); entry_demora_1.grid(row=1, column=1)
entry_demora_2 = tk.Entry(frame_prob, width=6); entry_demora_2.insert(0, "0.50"); entry_demora_2.grid(row=1, column=2)
entry_demora_3 = tk.Entry(frame_prob, width=6); entry_demora_3.insert(0, "0.25"); entry_demora_3.grid(row=1, column=3)

frame_costos = tk.LabelFrame(tab_datos, text="Parámetros de Costo y Operación")
frame_costos.pack(fill='x', padx=10, pady=10)

def crear_campo(frame, texto, fila, col, valor_defecto):
    tk.Label(frame, text=texto).grid(row=fila, column=col, sticky="e", padx=5, pady=5)
    entry = tk.Entry(frame, width=10)
    entry.insert(0, str(valor_defecto))
    entry.grid(row=fila, column=col+1, padx=5)
    return entry

entry_q1 = crear_campo(frame_costos, "Costo Almacenamiento (q1):", 0, 0, 100)
entry_q2 = crear_campo(frame_costos, "Costo Pedido (q2):", 1, 0, 20)
entry_q3 = crear_campo(frame_costos, "Costo Escasez (q3):", 2, 0, 40)
entry_beta = crear_campo(frame_costos, "Demanda Anual (Beta):", 0, 2, 365)
entry_y = crear_campo(frame_costos, "Tamaño de Lote (y):", 1, 2, 12.08)
entry_delta_y = crear_campo(frame_costos, "Demanda Prom. en Demora (Δy):", 2, 2, 2)

tk.Button(tab_datos, text="Procesar y Calcular Todo", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), command=ejecutar_programa).pack(pady=20)

# ================= PESTAÑA 2: RESULTADOS =================
tk.Label(tab_resultados, text="1. Distribución de Demanda", font=("Arial", 10, "bold")).pack(pady=5)
tabla_prob = ttk.Treeview(tab_resultados, columns=("D", "P", "PA"), show="headings", height=5)
tabla_prob.heading("D", text="Demanda"); tabla_prob.heading("P", text="Probabilidad"); tabla_prob.heading("PA", text="Acumulada")
tabla_prob.pack(fill='x', padx=10)

tk.Label(tab_resultados, text="2. Evaluación de Costos", font=("Arial", 10, "bold")).pack(pady=5)
tabla_costos = ttk.Treeview(tab_resultados, columns=("R", "ED", "CT"), show="headings", height=7)
tabla_costos.heading("R", text="Punto Reorden (R)"); tabla_costos.heading("ED", text="Esperanza E(D)"); tabla_costos.heading("CT", text="Costo Total")
tabla_costos.pack(fill='x', padx=10)

boton_grafico = tk.Button(tab_resultados, text="📊 Ver Gráfica de Costos", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), state="disabled", command=mostrar_grafico)
boton_grafico.pack(pady=20)

root.mainloop()