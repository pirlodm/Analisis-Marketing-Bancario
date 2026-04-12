# -------------------------------------------------------------------------
# MÓDULO DE VISUALIZACIÓN (sp_vis.py)
# -------------------------------------------------------------------------
# Descripción: Mi propia librería de gráficos. La he creado para que todos
#              los gráficos del proyecto tengan un estilo uniforme y para
#              no tener que repetir el código de poner etiquetas, etc.
# Autor: David Morales Méndez
# -------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURACIÓN ---
# He definido aquí los colores para usarlos en todos los gráficos y que sea fácil cambiarlos.
COLORES_PRO = ["#e74c3c", "#3498db"] 

def configurar_estilo():
    """Fija un estilo visual consistente para todos los gráficos del proyecto."""
    sns.set_context("talk")
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    print("🎨 Estilo visual configurado correctamente.")

# --- HELPER 1: Etiquetas para Barras Verticales (Columnas) ---
def agregar_etiquetas(ax, total):
    """
    Esta función la programé para poner los porcentajes encima de las barras verticales.
    Matplotlib no lo hace automáticamente, así que tuve que calcularlo.
    """
    for p in ax.patches:
        # 'p' es cada una de las barras del gráfico.
        height = p.get_height()
        # Si la barra no tiene altura, no hago nada.
        if np.isnan(height) or height == 0: continue
        # Calculo el porcentaje que representa la barra sobre el total.
        percentage = f'{100 * height / total:.1f}%'
        # Calculo las coordenadas X e Y donde quiero poner el texto.
        x = p.get_x() + p.get_width() / 2.
        y = height + (total * 0.01) 
        # Finalmente, dibujo el texto.
        ax.text(x, y, percentage, ha="center", size=10, color='black', weight='bold')

# --- HELPER 2: Etiquetas para Barras Horizontales (Filas) ---
def agregar_etiquetas_horizontal(ax, total):
    """
    Es la versión de la función anterior pero para barras horizontales.
    La lógica es la misma, pero cambiando 'height' por 'width' y ajustando
    las coordenadas X e Y.
    """
    for p in ax.patches:
        width = p.get_width() 
        if np.isnan(width) or width == 0: continue
        
        percentage = f'{100 * width / total:.1f}%'
        
        # X es el final de la barra + margen
        x = width + (total * 0.005) 
        y = p.get_y() + p.get_height() / 2.
        
        ax.text(x, y, percentage, va="center", size=10, color='black', weight='bold')

# --- GRÁFICOS RESULTADO Y ECONÓMICOS ---

def plot_target_donut(df, col_target='y'):
    """
    Gráfico de donut para ver la distribución de la variable objetivo.
    El truco para hacer el donut es dibujar un gráfico de pastel normal
    y luego superponer un círculo blanco en el centro.
    """
    plt.figure(figsize=(7, 7))
    conteo = df[col_target].value_counts()
    labels = [f"No ({conteo.iloc[0]})", f"Sí ({conteo.iloc[1]})"] 
    plt.pie(conteo, labels=labels, autopct='%1.1f%%', colors=COLORES_PRO, 
            startangle=90, pctdistance=0.85, explode=(0.05, 0.05))
    # Aquí está el truco: creo un círculo blanco.
    centro_blanco = plt.Circle((0,0), 0.70, fc='white') 
    ax = plt.gca()
    ax.add_artist(centro_blanco)
    plt.title(f"Distribución de {col_target.upper()}", fontsize=16, weight='bold')
    plt.show()

def plot_ingresos_vs_target(df, col_x='y', col_y='income'):
    plt.figure(figsize=(10, 6))
    # Uso un boxplot porque es perfecto para comparar la distribución de una
    # variable numérica (ingresos) entre dos categorías (sí/no).
    # Me permite ver medianas, cuartiles y outliers de un vistazo.
    sns.boxplot(x=col_x, y=col_y, hue=col_x, data=df, palette=COLORES_PRO, width=0.5, linewidth=1.5, legend=False)
    sns.despine(trim=True)
    plt.title(f"Distribución de {col_y} según decisión", fontsize=16)
    plt.xlabel("Respuesta", weight='bold')
    plt.ylabel(f"{col_y} (Euros)", weight='bold')
    plt.show()

def plot_heatmap_estrategico(df, target_col='y', cols_extra=[]):
    """
    Esta función la hice para ver qué variables numéricas están más
    relacionadas con la decisión de compra.
    """
    plt.figure(figsize=(10, 8))
    df_corr = df.copy()
    # La función de correlación solo funciona con números. Como mi objetivo es
    # 'yes'/'no', creo una columna temporal donde 'yes' es 1 y 'no' es 0.
    if df_corr[target_col].dtype == 'object':
        df_corr['TARGET_VENTA'] = df_corr[target_col].map({'yes': 1, 'no': 0})
    else:
        df_corr['TARGET_VENTA'] = df_corr[target_col]
    # Defino unas columnas base que siempre quiero analizar.
    cols_base = ['TARGET_VENTA', 'income', 'age', 'euribor3m', 'campaign', 'pdays']
    cols_totales = list(set(cols_base + cols_extra))
    cols_finales = df_corr.columns.intersection(cols_totales)
    matriz_corr = df_corr[cols_finales].corr(numeric_only=True)
    # La matriz de correlación es simétrica. Para que sea más fácil de leer,
    # creo una "máscara" para ocultar la mitad superior, que es redundante.
    mask = np.triu(np.ones_like(matriz_corr, dtype=bool))
    sns.heatmap(matriz_corr, mask=mask, cmap="RdBu_r", center=0, 
                vmax=1, vmin=-1, annot=True, fmt=".2f", linewidths=1, cbar_kws={"shrink": .8})
    plt.title("Factores influyentes en la VENTA", fontsize=16, weight='bold')
    plt.yticks(rotation=0)
    plt.show()

# --- GRÁFICOS PERFIL DE CLIENTE ---

def plot_edad_distribucion(df, col_x='age', hue='y'):
    plt.figure(figsize=(10, 6))
    # Un histograma apilado es ideal para ver cómo se distribuye la edad
    # y, dentro de cada rango de edad, qué proporción hay de 'sí' y 'no'.
    sns.histplot(data=df, x=col_x, hue=hue, multiple="stack", palette=COLORES_PRO, bins=20, kde=True)
    plt.title(f"Distribución de {col_x.upper()} por Respuesta", fontsize=16)
    plt.xlabel("Edad", weight='bold')
    plt.ylabel("Cantidad de Clientes", weight='bold')
    plt.show()

def plot_trabajo_barras(df, col_cat='job', hue='y'):
    """
    Para categorías con nombres largos como las profesiones, un gráfico de
    barras verticales es ilegible. Por eso decidí hacerlo horizontal,
    poniendo las categorías en el eje Y.
    """
    plt.figure(figsize=(12, 8))
    # Ordeno las barras de mayor a menor frecuencia para que el gráfico
    # sea más fácil de interpretar.
    orden = df[col_cat].value_counts().index
    
    ax = sns.countplot(data=df, y=col_cat, hue=hue, palette=COLORES_PRO, order=orden)
    # Dejo un poco de espacio extra a la derecha para que quepan las etiquetas.
    plt.xlim(0, plt.xlim()[1] * 1.15) # Aire a la derecha
    agregar_etiquetas_horizontal(ax, len(df))
    
    plt.title(f"Respuesta de la Campaña por {col_cat.upper()}", fontsize=16)
    plt.xlabel("Cantidad de Clientes", weight='bold')
    plt.ylabel("Tipo de Trabajo", weight='bold')
    plt.legend(title='¿Compró?', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_educacion_barras(df, col_cat='education', hue='y'):
    """
    Igual que con el trabajo, los niveles educativos tienen nombres largos.
    Por eso reutilizo la misma lógica de gráfico horizontal.
    """
    plt.figure(figsize=(12, 6))
    orden = df[col_cat].value_counts().index
    
    # Usamos 'y' para horizontal
    ax = sns.countplot(data=df, y=col_cat, hue=hue, palette=COLORES_PRO, order=orden)
    
    plt.xlim(0, plt.xlim()[1] * 1.15) # Aire a la derecha
    agregar_etiquetas_horizontal(ax, len(df))
    
    plt.title(f"Respuesta según Nivel Educativo ({col_cat})", fontsize=16)
    plt.xlabel("Cantidad de Clientes", weight='bold')
    plt.ylabel("Nivel de Estudios", weight='bold')
    plt.legend(title='¿Compró?', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

# --- GRÁFICO ESTACIONALIDAD ---

def plot_mes_barras(df, col_cat='month', hue='y'):
    """
    En este caso, como los nombres de los meses son cortos ('mar', 'apr'...),
    un gráfico de barras vertical funciona perfectamente y es más intuitivo
    para mostrar una evolución en el tiempo.
    """
    plt.figure(figsize=(10, 6))
    # Defino el orden correcto de los meses para que no se ordenen alfabéticamente.
    orden_meses = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    # Me aseguro de usar solo los meses que realmente están en mis datos.
    orden_final = [m for m in orden_meses if m in df[col_cat].unique()]
    
    ax = sns.countplot(data=df, x=col_cat, hue=hue, palette=COLORES_PRO, order=orden_final)
    # Dejo espacio arriba para las etiquetas.
    plt.ylim(0, plt.ylim()[1] * 1.15) # Aire arriba
    agregar_etiquetas(ax, len(df))
    
    plt.title("Evolución de Ventas por Mes", fontsize=16)
    plt.xlabel("Mes de la Campaña", weight='bold')
    plt.ylabel("Clientes Contactados", weight='bold')
    plt.legend(title='¿Compró?', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()