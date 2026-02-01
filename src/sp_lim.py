# -------------------------------------------------------------------------
# MÓDULO DE LIMPIEZA DE DATOS (sp_lim.py)
# -------------------------------------------------------------------------
# 
# Descripción: Funciones reutilizables para limpieza y estandarización de DataFrames.
# -------------------------------------------------------------------------

import pandas as pd

# -------------------------------------------------------------------------
# 1. ESTANDARIZACIÓN GENERAL (TEXTO Y TÍTULOS)
# -------------------------------------------------------------------------

def limpiar_titulos(df):
    """
    Estandariza los títulos de las columnas:
    - Todo a minúsculas.
    - Reemplaza puntos (.) y espacios ( ) por guiones bajos (_).
    """
    df.columns = df.columns.str.lower().str.replace('.', '_').str.replace(' ', '_')
    print("✅ Títulos de columnas estandarizados.")


def limpiar_texto(df, columnas_a_ignorar=[]):
    """
    Estandariza columnas de texto:
    - Pone todo en minúsculas.
    - Cambia espacios y puntos por guiones bajos.
    - Cambia la 'ñ' por 'n' (para evitar problemas de codificación).
    
    Parámetros:
    - columnas_a_ignorar: Lista de columnas que NO queremos tocar (ej: IDs).
    """
    # Seleccionamos solo las columnas de tipo texto (object)
    cols_texto = df.select_dtypes(include='object').columns
    
    # Filtramos las que queremos ignorar
    cols_a_limpiar = [col for col in cols_texto if col not in columnas_a_ignorar]
    
    print(f"🧹 Limpiando contenido de {len(cols_a_limpiar)} columnas...")
    
    for col in cols_a_limpiar:
        if col in df.columns:
            # 1. A minúsculas
            df[col] = df[col].str.lower()
            # 2. Espacios -> guiones bajos
            df[col] = df[col].str.replace(' ', '_')
            # 3. Puntos -> guiones bajos
            df[col] = df[col].str.replace('.', '_', regex=False)
            # 4. Ñ -> n (Regla de oro)
            df[col] = df[col].str.replace('ñ', 'n')
            
    print("✅ Textos estandarizados (sin ñ).")

# -------------------------------------------------------------------------
# 2. GESTIÓN DE COLUMNAS Y VALORES
# -------------------------------------------------------------------------

def cambiar_nombres(df, nombres_nuevos):
    """
    Renombra columnas específicas.
    Uso: cambiar_nombres(df, {'id_': 'ID', 'age': 'edad'})
    """
    df.rename(columns=nombres_nuevos, inplace=True)
    print(f"✅ Se han renombrado las columnas: {list(nombres_nuevos.keys())}")


def reemplazar_valor(df, columna, valor_antiguo, valor_nuevo):
    """
    Busca un valor específico en una columna y lo cambia por otro.
    Ideal para cambiar 'unknown' por 'desconocido'.
    """
    if columna in df.columns:
        # Contamos cuántos hay antes de cambiarlo para informar
        cantidad = df[columna].value_counts().get(valor_antiguo, 0)
        
        # Hacemos el cambio
        df[columna] = df[columna].replace(valor_antiguo, valor_nuevo)
        
        print(f"🔄 En columna '{columna}': se han cambiado {cantidad} veces '{valor_antiguo}' por '{valor_nuevo}'.")
    else:
        print(f"⚠️ La columna '{columna}' no existe, no se pudo reemplazar.")


def eliminar_columnas(df, columnas_a_borrar):
    """
    Elimina las columnas indicadas.
    Uso: eliminar_columnas(df, ['unnamed:_0', 'columna_basura'])
    """
    # errors='ignore' evita que el código falle si la columna ya no existe
    df.drop(columns=columnas_a_borrar, inplace=True, errors='ignore')
    
    print(f"🗑️ Columnas eliminadas: {columnas_a_borrar}")


def eliminar_duplicados(df):
    """
    Busca filas totalmente repetidas y las borra, dejando solo una.
    """
    num_duplicados = df.duplicated().sum()
    if num_duplicados > 0:
        df.drop_duplicates(inplace=True)
        print(f"🗑️ Se han eliminado {num_duplicados} filas duplicadas.")
    else:
        print("✅ No se encontraron duplicados.")

# -------------------------------------------------------------------------
# 3. CORRECCIONES DE FORMATO (FECHAS Y NÚMEROS)
# -------------------------------------------------------------------------

def arreglar_fecha(df, columna):
    """
    Convierte fechas de texto español (ej: '1-mayo-2016') a formato fecha real.
    """
    # Diccionario de traducción
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    if columna in df.columns:
        # Reemplazamos el texto del mes por su número
        for mes_nombre, mes_numero in meses.items():
            df[columna] = df[columna].str.replace(mes_nombre, mes_numero)

        # Convertimos a formato fecha datetime
        try:
            df[columna] = pd.to_datetime(df[columna], format='%d-%m-%Y')
            print(f"📅 Columna '{columna}' convertida a fecha correctamente.")
        except Exception as e:
            print(f"❌ Error convirtiendo fecha en '{columna}': {e}")


def limpiar_numeros(df, lista_columnas):
    """
    Convierte números que vienen como texto con comas ('93,5') 
    a números reales con puntos (93.5).
    """
    print(f"🔢 Arreglando formato numérico en: {lista_columnas}")
    
    for col in lista_columnas:
        if col in df.columns:
            # 1. Cambiamos la coma por punto
            # (Usamos astype(str) por seguridad)
            df[col] = df[col].astype(str).str.replace(',', '.')
            
            # 2. Convertimos a numérico (float)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    print("✅ Números convertidos.")