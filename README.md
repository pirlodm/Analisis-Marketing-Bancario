# 🏦 Optimización de Marketing Bancario (Data Analytics)

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Data-Pandas-green?style=flat&logo=pandas)
![Seaborn](https://img.shields.io/badge/Viz-Seaborn-orange?style=flat&logo=python)
![Status](https://img.shields.io/badge/Status-Finalizado-success)

## 📖 Contexto del Proyecto
Este proyecto analiza la eficiencia de las campañas de telemarketing de una entidad bancaria portuguesa. A través de un dataset procesado de **+20,000 interacciones reales**, se busca entender por qué la tasa de conversión es tan baja y proponer una estrategia basada en datos para mejorar el ROI (Retorno de Inversión).

El análisis abarca desde la limpieza de datos (`ETL`) hasta la visualización avanzada y la generación de informes ejecutivos.

## 📂 Estructura del Repositorio
El proyecto sigue una estructura modular profesional:

* **`data/`**: Contiene los datasets procesados y limpios.
* **`notebooks/`**: Análisis secuencial paso a paso:
    * `01-05`: Exploración (EDA), limpieza y transformación de datos.
    * `06_analisis_descriptivo.ipynb`: Estadísticas clave.
    * `07_visualizacion_datos.ipynb`: **Visualización avanzada** con librería propia.
    * `08_informe_final.ipynb`: **Informe Ejecutivo** con insights y recomendaciones de negocio.
* **`src/`**: Código fuente reutilizable y modular.
    * `sp_eda.py`: Funciones para el Análisis Exploratorio inicial (conteo de nulos, info general, duplicados).
    * `sp_lim.py`: Funciones de limpieza, estandarización y tratamiento de datos.
    * `sp_vis.py`: Librería personalizada de gráficos con etiquetas porcentuales y diseño corporativo.

## 📊 Hallazgos Clave (Insights)
Tras analizar más de 20 variables, estos son los descubrimientos más críticos:

1.  **📉 El Desafío del 4.6%:** La tasa de conversión real es extremadamente baja (4.6%), lo que indica un desperdicio masivo de recursos en llamadas fallidas (95.4%).
2.  **🎓 La Paradoja del Perfil:** Aunque el banco centra sus esfuerzos en perfiles *Blue-collar* y *Administrativos*, los segmentos más rentables son **Estudiantes** y **Jubilados**, que duplican la tasa de éxito.
3.  **💸 Independencia Económica:** Se demostró estadísticamente que el nivel de ingresos del cliente **NO influye** en su decisión de compra.
4.  **🤖 Estacionalidad Plana:** El banco opera en "piloto automático", realizando el mismo volumen de llamadas (~1600/mes) sin aprovechar los picos de conversión natural.

## 🚀 Recomendaciones Estratégicas
Basado en los datos, se propone al negocio:
1.  **Pivotar el Target:** Redirigir presupuesto hacia los nichos de Estudiantes y Seniors.
2.  **Implementar IA:** Desarrollar un modelo de Machine Learning para filtrar el 95% de "Noes" antes de llamar.
3.  **Romper la Estacionalidad:** Concentrar esfuerzos en inicio de curso y pagas extra, abandonando la estrategia plana.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3
* **Librerías de Análisis:** Pandas, Numpy
* **Visualización:** Matplotlib, Seaborn
* **Entorno:** Jupyter Notebook, VS Code, Git

---
### ✒️ Autor
**[David morales mendez]** *Analista de Datos / Data Scientist en formación*