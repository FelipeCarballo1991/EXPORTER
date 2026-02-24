# 📊 Conversor de Archivos HTML/CSV/TXT a Excel

Aplicación web desarrollada con Streamlit para convertir archivos HTML (con tablas), CSV y TXT a formatos Excel o CSV con opciones avanzadas de edición.

## ✨ Características

- 📤 **Carga de archivos**: Soporta HTML, CSV y TXT (hasta 1GB)
- 👀 **Vista previa**: Visualiza tus tablas antes de exportar
- 📈 **Estadísticas**: Filas, columnas, valores nulos y duplicados
- ✂️ **Edición de columnas**: Elimina y renombra columnas fácilmente
- 📊 **Selección de tablas**: Elige qué tablas exportar
- 💾 **Múltiples formatos**: Exporta a Excel (.xlsx) o CSV
- 📋 **Sistema de logs**: Registro completo de actividades y errores
- 🚀 **Alto rendimiento**: Caché inteligente para evitar procesamiento repetido

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd EXPORTER
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Instala pandas-toolkit desde el repositorio:
```bash
pip install git+https://github.com/FelipeCarballo1991/EDA-toolkit.git
```

## 🚀 Uso

Ejecuta la aplicación:
```bash
streamlit run streamlit_app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📂 Estructura del Proyecto

```
EXPORTER/
├── .streamlit/
│   └── config.toml          # Configuración de Streamlit
├── input/                   # Archivos de entrada (ignorado en git)
├── output/                  # Archivos exportados (ignorado en git)
├── logs/                    # Logs de la aplicación (ignorado en git)
├── streamlit_app.py         # Aplicación principal
├── .gitignore              # Archivos ignorados por git
└── README.md               # Este archivo
```

## 📋 Configuración

El archivo `.streamlit/config.toml` permite configurar:
- Tamaño máximo de carga (default: 1000 MB)
- Opciones del navegador

## 📝 Logs

Los logs se guardan automáticamente en la carpeta `logs/` con formato:
- `app_YYYYMMDD.log` (un archivo por día)
- Incluye información de carga, exportación y errores

## 🔧 Tecnologías

- **Streamlit**: Framework de aplicación web
- **Pandas**: Procesamiento de datos
- **OpenPyXL**: Exportación a Excel
- **Pandas-Toolkit**: Lectura de múltiples formatos


