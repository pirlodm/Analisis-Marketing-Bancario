# -------------------------------------------------------------------------
# MÓDULO DE EXPLORACIÓN DE DATOS (sp_eda.py)
# -------------------------------------------------------------------------
# Descripción: He creado este módulo para no tener que repetir siempre
#              los mismos pasos al empezar a analizar un DataFrame.
#              Con una sola función, me da una visión general de todo.
# -------------------------------------------------------------------------

import pandas as pd
from IPython.display import display  # Lo importo para que las tablas se vean bonitas en el notebook.

def eda_preliminar(df):
    """
    Función que he programado para hacer una auditoría completa de un DataFrame.
    Me muestra todo lo que necesito saber al principio:
    1. Una muestra aleatoria.
    2. Dimensiones (filas y columnas).
    3. Información técnica (tipos de datos).
    4. Porcentaje de valores nulos.
    5. Conteo de duplicados.
    6. Estadísticas de columnas numéricas.
    7. Análisis de valores frecuentes en columnas de texto.
    """
    
    # ---------------------------------------------------------------------
    # 1. MUESTRA ALEATORIA
    # ---------------------------------------------------------------------
    print("--- 1. MUESTRA ALEATORIA ---")
    # Si hay menos de 5 filas, mostramos todas. Si hay más, mostramos 5.
    n = 5 if len(df) > 5 else len(df)
    display(df.sample(n))

    # ---------------------------------------------------------------------
    # 2. DIMENSIONES
    # ---------------------------------------------------------------------
    print("\n--- 2. DIMENSIONES ---")
    print(f'Filas: {df.shape[0]} | Columnas: {df.shape[1]}')

    # ---------------------------------------------------------------------
    # 3. TIPOS DE DATOS (INFO)
    # ---------------------------------------------------------------------
    print("\n--- 3. INFO GENERAL ---")
    df.info()

    # ---------------------------------------------------------------------
    # 4. VALORES NULOS
    # ---------------------------------------------------------------------
    print("\n--- 4. NULOS ---")
    # Calculo el porcentaje de nulos. Uso .mean() porque al tratar True/False como 1/0,
    # la media me da directamente la proporción, que es más útil que una suma.
    nulos_pct = df.isnull().mean() * 100
    
    if nulos_pct.sum() > 0:
        # Mostramos solo las columnas que tienen nulos, ordenadas de mayor a menor
        display(nulos_pct[nulos_pct > 0].sort_values(ascending=False).to_frame('% Nulos'))
    else:
        print("✅ ¡Perfecto! No hay valores nulos.")

    # ---------------------------------------------------------------------
    # 5. DUPLICADOS
    # ---------------------------------------------------------------------
    print("\n--- 5. DUPLICADOS ---")
    num_duplicados = df.duplicated().sum()
    
    if num_duplicados > 0:
        print(f"⚠️ Alerta: Se han encontrado {num_duplicados} filas totalmente duplicadas.")
    else:
        print("✅ No hay filas duplicadas.")

    # ---------------------------------------------------------------------
    # 6. ESTADÍSTICAS NUMÉRICAS
    # ---------------------------------------------------------------------
    print("\n--- 6. ESTADÍSTICAS NUMÉRICAS ---")
    # Uso select_dtypes para aplicar el describe() solo a las columnas que son
    # numéricas y evitar errores con las de texto.
    cols_num = df.select_dtypes(include=['number']).columns
    
    if len(cols_num) > 0:
        display(df.describe().T)
    else:
        print("No hay columnas numéricas para analizar.")

    # ---------------------------------------------------------------------
    # 7. COLUMNAS DE TEXTO (CATEGÓRICAS)
    # ---------------------------------------------------------------------
    print("\n--- 7. COLUMNAS DE TEXTO (Top 10 valores) ---")
    # Hago lo mismo que con las numéricas, pero para las de tipo 'object' (texto),
    # que son las que puedo analizar por categorías.
    cols_texto = df.select_dtypes(include='object').columns
    
    if len(cols_texto) > 0:
        for col in cols_texto:
            # Calculamos cuántos valores únicos hay
            num_unicos = df[col].nunique()
            
            # Título explicativo
            print(f"\n-> Columna: {col.upper()} (Total únicos: {num_unicos})")
            
            # Para que la salida sea más clara, creo una tabla con los valores más frecuentes.
            # 1. Cuento los valores y me quedo con los 10 primeros.
            top_valores = df[col].value_counts().head(10).reset_index()
            # 2. Renombro las columnas para que se entienda qué es cada cosa.
            top_valores.columns = ['Valor', 'Frecuencia']
            
            # 3. Uso display() para que Jupyter lo muestre como una tabla HTML.
            display(top_valores)
            
            # Nota informativa si hay muchos valores ocultos
            if num_unicos > 10:
                print(f"   (Se muestran solo los 10 primeros de {num_unicos})")
            
    else:
        print("No hay columnas de texto.")