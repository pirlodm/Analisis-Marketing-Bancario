# -------------------------------------------------------------------------
# MÓDULO DE VISUALIZACIÓN (sp_vis.py)
# -------------------------------------------------------------------------
# Descripción: Librería de gráficos profesionales.
#              Soporte para barras horizontales en categorías largas.
# Autor: Gemini (Tu Asistente de IA)
# -------------------------------------------------------------------------

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- CONFIGURACIÓN ---
COLORES_PRO = ["#e74c3c", "#3498db"] 

def configurar_estilo():
    sns.set_context("talk")
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)
    print("🎨 Estilo visual configurado correctamente.")

# --- HELPER 1: Etiquetas para Barras Verticales (Columnas) ---
def agregar_etiquetas(ax, total):
    for p in ax.patches:
        height = p.get_height()
        if np.isnan(height) or height == 0: continue
        percentage = f'{100 * height / total:.1f}%'
        x = p.get_x() + p.get_width() / 2.
        y = height + (total * 0.01) 
        ax.text(x, y, percentage, ha="center", size=10, color='black', weight='bold')

# --- HELPER 2: Etiquetas para Barras Horizontales (Filas) ---
def agregar_etiquetas_horizontal(ax, total):
    """
    Pone el porcentaje a la derecha de la barra.
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
    plt.figure(figsize=(7, 7))
    conteo = df[col_target].value_counts()
    labels = [f"No ({conteo[0]})", f"Sí ({conteo[1]})"] 
    plt.pie(conteo, labels=labels, autopct='%1.1f%%', colors=COLORES_PRO, 
            startangle=90, pctdistance=0.85, explode=(0.05, 0.05))
    centro_blanco = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centro_blanco)
    plt.title(f"Distribución de {col_target.upper()}", fontsize=16, weight='bold')
    plt.show()

def plot_ingresos_vs_target(df, col_x='y', col_y='income'):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=col_x, y=col_y, data=df, palette=COLORES_PRO, width=0.5, linewidth=1.5)
    sns.despine(trim=True)
    plt.title(f"Distribución de {col_y} según decisión", fontsize=16)
    plt.xlabel("Respuesta", weight='bold')
    plt.ylabel(f"{col_y} (Euros)", weight='bold')
    plt.show()

def plot_heatmap_estrategico(df, target_col='y', cols_extra=[]):
    plt.figure(figsize=(10, 8))
    df_corr = df.copy()
    if df_corr[target_col].dtype == 'object':
        df_corr['TARGET_VENTA'] = df_corr[target_col].map({'yes': 1, 'no': 0})
    else:
        df_corr['TARGET_VENTA'] = df_corr[target_col]
    cols_base = ['TARGET_VENTA', 'income', 'age', 'euribor3m', 'campaign', 'pdays']
    cols_totales = list(set(cols_base + cols_extra))
    cols_finales = df_corr.columns.intersection(cols_totales)
    matriz_corr = df_corr[cols_finales].corr()
    mask = np.triu(np.ones_like(matriz_corr, dtype=bool))
    sns.heatmap(matriz_corr, mask=mask, cmap="RdBu_r", center=0, 
                vmax=1, vmin=-1, annot=True, fmt=".2f", linewidths=1, cbar_kws={"shrink": .8})
    plt.title("Factores influyentes en la VENTA", fontsize=16, weight='bold')
    plt.yticks(rotation=0)
    plt.show()

# --- GRÁFICOS PERFIL DE CLIENTE ---

def plot_edad_distribucion(df, col_x='age', hue='y'):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=col_x, hue=hue, multiple="stack", palette=COLORES_PRO, bins=20, kde=True)
    plt.title(f"Distribución de {col_x.upper()} por Respuesta", fontsize=16)
    plt.xlabel("Edad", weight='bold')
    plt.ylabel("Cantidad de Clientes", weight='bold')
    plt.show()

def plot_trabajo_barras(df, col_cat='job', hue='y'):
    """Gráfico HORIZONTAL para profesiones."""
    plt.figure(figsize=(12, 8))
    orden = df[col_cat].value_counts().index
    
    ax = sns.countplot(data=df, y=col_cat, hue=hue, palette=COLORES_PRO, order=orden)
    
    plt.xlim(0, plt.xlim()[1] * 1.15) # Aire a la derecha
    agregar_etiquetas_horizontal(ax, len(df))
    
    plt.title(f"Respuesta de la Campaña por {col_cat.upper()}", fontsize=16)
    plt.xlabel("Cantidad de Clientes", weight='bold')
    plt.ylabel("Tipo de Trabajo", weight='bold')
    plt.legend(title='¿Compró?', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

def plot_educacion_barras(df, col_cat='education', hue='y'):
    """Gráfico HORIZONTAL para educación (NUEVO CAMBIO)."""
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
    """Este se queda VERTICAL porque los meses son cortos (mar, apr...)."""
    plt.figure(figsize=(10, 6))
    orden_meses = ['mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    orden_final = [m for m in orden_meses if m in df[col_cat].unique()]
    
    ax = sns.countplot(data=df, x=col_cat, hue=hue, palette=COLORES_PRO, order=orden_final)
    
    plt.ylim(0, plt.ylim()[1] * 1.15) # Aire arriba
    agregar_etiquetas(ax, len(df))
    
    plt.title("Evolución de Ventas por Mes", fontsize=16)
    plt.xlabel("Mes de la Campaña", weight='bold')
    plt.ylabel("Clientes Contactados", weight='bold')
    plt.legend(title='¿Compró?', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()