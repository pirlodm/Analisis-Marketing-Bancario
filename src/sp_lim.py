# -------------------------------------------------------------------------
# MÓDULO DE LIMPIEZA DE DATOS (sp_lim.py)
# -------------------------------------------------------------------------
# Descripción: He agrupado aquí todas las funciones que he ido creando para
#              limpiar y estandarizar los datos. Así no tengo que reescribirlas.
# -------------------------------------------------------------------------

import pandas as pd

# -------------------------------------------------------------------------
# 1. ESTANDARIZACIÓN GENERAL (TEXTO Y TÍTULOS)
# -------------------------------------------------------------------------

def limpiar_titulos(df):
    """
    Esta función la hice para estandarizar los nombres de las columnas.
    Así evito problemas con mayúsculas, espacios o puntos. Lo paso todo
    a minúsculas y uso guiones bajos, que es una buena práctica en Python
    (formato snake_case).
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('.', '_', regex=False)
    )
    print("✅ Nombres de columnas estandarizados.")
    return df


def limpiar_texto(df, columnas_a_ignorar=[]):
    """
    Esta función recorre todas las columnas de texto y las normaliza.
    La idea es que 'blue-collar' y 'Blue Collar' se traten como lo mismo.
    También quito la 'ñ' para evitar problemas de codificación (encoding)
    si luego exporto los datos.
    
    Parámetros:
    - columnas_a_ignorar: Le añadí este parámetro para poder saltarme
      columnas que no quiero modificar, como por ejemplo un ID.
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
            # 4. Guiones medios -> guiones bajos (NUEVO)
            df[col] = df[col].str.replace('-', '_', regex=False)
            # 5. Ñ -> n (Regla de oro)
            df[col] = df[col].str.replace('ñ', 'n')
            
    print("✅ Textos estandarizados (sin ñ, espacios, puntos ni guiones).")

# -------------------------------------------------------------------------
# 2. GESTIÓN DE COLUMNAS Y VALORES
# -------------------------------------------------------------------------

def cambiar_nombres(df, nombres_nuevos):
    """
    Una función simple para renombrar columnas. La hice para que el código
    principal quede más limpio y sea más legible.
    Ejemplo de uso: cambiar_nombres(df, {'id_': 'ID', 'age': 'edad'})
    """
    df.rename(columns=nombres_nuevos, inplace=True)
    print(f"✅ Se han renombrado las columnas: {list(nombres_nuevos.keys())}")


def reemplazar_valor(df, columna, valor_antiguo, valor_nuevo):
    """
    La uso para corregir valores específicos. Por ejemplo, para traducir
    'unknown' a 'desconocido' y que todo el dataset esté en el mismo idioma.
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
    Función para quitar columnas que no aportan información.
    Le puse 'errors='ignore'' para que el script no se rompa si
    intento borrar una columna que ya no existe.
    """
    # errors='ignore' evita que el código falle si la columna ya no existe
    df.drop(columns=columnas_a_borrar, inplace=True, errors='ignore')
    
    print(f"🗑️ Columnas eliminadas: {columnas_a_borrar}")


def eliminar_duplicados(df):
    """
    Busca filas que sean exactamente iguales y las elimina.
    Esto es clave para asegurar la calidad del dato.
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
    Me encontré con que las fechas venían como texto con el mes en español
    (ej: '1-mayo-2016'). Esta función traduce el mes a número y luego
    convierte toda la columna a un formato de fecha real (datetime).
    """
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    if columna in df.columns:
        # Itero sobre el diccionario para reemplazar el nombre del mes por su número.
        for mes_nombre, mes_numero in meses.items():
            df[columna] = df[columna].str.replace(mes_nombre, mes_numero)

        # Intento convertir la columna a fecha. Uso un try-except por si
        # algún valor está corrupto y no se puede convertir, para que el
        # programa me avise en lugar de fallar.
        try:
            df[columna] = pd.to_datetime(df[columna], format='%d-%m-%Y')
            print(f"📅 Columna '{columna}' convertida a fecha correctamente.")
        except Exception as e:
            print(f"❌ Error convirtiendo fecha en '{columna}': {e}")


def limpiar_numeros(df, lista_columnas):
    """
    Algunos números venían como texto y con coma decimal ('93,5').
    Esta función primero reemplaza la coma por un punto y luego convierte
    la columna a un tipo numérico para poder hacer cálculos con ella.
    """
    print(f"🔢 Arreglando formato numérico en: {lista_columnas}")
    
    for col in lista_columnas:
        if col in df.columns:
            # 1. Cambiamos la coma por punto
            # (Usamos astype(str) por seguridad)
            df[col] = df[col].astype(str).str.replace(',', '.')
            
            # 2. Convertimos a numérico. El 'errors='coerce'' es muy importante:
            # si encuentra un valor que no puede convertir (ej. una letra),
            # lo transforma en NaN (nulo) en lugar de dar un error.
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    print("✅ Números convertidos.")