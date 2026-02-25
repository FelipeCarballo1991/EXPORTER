# 📊 Conversor de Archivos a Excel/CSV

Aplicación web desarrollada con Streamlit para convertir múltiples formatos de archivos a Excel o CSV con opciones avanzadas de edición y transformación de datos.

## ✨ Características

### 📤 Carga de Archivos
- Soporta múltiples formatos: **HTML, CSV, TXT, XLSX, JSON, TSV**
- Límite de carga: **hasta 1GB**
- Caché inteligente para evitar procesamiento repetido

### 📊 Análisis y Vista Previa
- **Vista previa interactiva** de las primeras 10 filas
- **Estadísticas detalladas**:
  - Número de filas y columnas (con formato de miles)
  - Uso de memoria del dataset
  - Valores nulos con porcentajes
  - Filas duplicadas con porcentajes
  - Tipos de datos por columna
  - Detección automática de columnas anidadas

### 🔓 Manejo de Datos Anidados (JSON)
- **Detección automática** de estructuras anidadas (diccionarios y listas)
- **3 opciones de transformación**:
  1. Mantener original
  2. Convertir a JSON string
  3. Desanidar columnas (flatten)
- Soporte para **listas de diccionarios** `[{'key': 'value'}]`
- Desanidado inteligente que crea columnas separadas

### ✂️ Edición de Datos
- **Eliminar columnas** innecesarias
- **Renombrar columnas** fácilmente
- **Selección de tablas** específicas para exportar

### 💾 Exportación
- Formatos: **Excel (.xlsx)** o **CSV**
- Opción de incluir/excluir índice
- Exportación múltiple (un CSV por tabla)
- Descarga directa desde el navegador
- Fallback automático a CSV si Excel falla

### 📋 Sistema de Logs
- Registro completo de actividades y errores
- Logs diarios en carpeta `logs/`
- Visor de logs integrado en la aplicación

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

## 📖 Guía de Uso

### Flujo Básico

1. **Subir archivo**: Selecciona un archivo desde tu equipo
2. **Vista previa**: Revisa las estadísticas y primeras filas de cada tabla
3. **Desanidar (opcional)**: Si el archivo JSON tiene datos anidados, elige cómo procesarlos
4. **Editar**: Elimina o renombra columnas según necesites
5. **Seleccionar**: Marca las tablas que deseas exportar
6. **Exportar**: Elige formato (Excel/CSV) y descarga

### Manejo de Archivos JSON con Datos Anidados

Cuando cargues un archivo JSON con estructuras anidadas, la aplicación te ofrecerá 3 opciones:

#### Opción 1: Mantener Original
- Deja los datos como están
- ⚠️ Puede causar problemas al exportar

#### Opción 2: Convertir a JSON String
- Convierte diccionarios y listas a texto
- Ejemplo: `{'name': 'Juan'}` → `"{'name': 'Juan'}"`
- ✅ Exporta sin problemas, pero pierde estructura

#### Opción 3: Desanidar Columnas (Flatten)
- **Diccionarios simples**: Crea columnas separadas
  ```json
  // Antes
  {"user": {"name": "Juan", "age": 25}}
  
  // Después
  user.name | user.age
  Juan      | 25
  ```

- **Listas de diccionarios**: Extrae el primer elemento y lo desanida
  ```json
  // Antes
  {"tags": [{"name": "tag1", "value": "x"}]}
  
  // Después
  tags.name | tags.value
  tag1      | x
  ```

### Visor de Logs

Accede al sidebar → "📋 Logs de Actividad" → "Ver logs de hoy" para revisar:
- Operaciones realizadas
- Errores capturados con stack trace completo
- Información de archivos procesados

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

## � Formatos Soportados

### Entrada
| Formato | Extensión | Características |
|---------|-----------|-----------------|
| HTML    | `.html`   | Extrae todas las tablas del documento |
| CSV     | `.csv`    | Separado por comas |
| TXT     | `.txt`    | Detecta delimitador automáticamente |
| Excel   | `.xlsx`   | Lee todas las hojas como tablas separadas |
| JSON    | `.json`   | Soporta estructuras anidadas y arrays |
| TSV     | `.tsv`    | Separado por tabuladores |

### Salida
- **Excel** (`.xlsx`): Múltiples hojas en un solo archivo
- **CSV** (`.csv`): Un archivo por tabla con encoding UTF-8

## 📝 Logs

Los logs se guardan automáticamente en la carpeta `logs/` con formato:
- `app_YYYYMMDD.log` (un archivo por día)
- Incluye información de:
  - Carga de archivos (nombre, tamaño, tablas extraídas)
  - Operaciones de desanidado
  - Exportaciones realizadas
  - Errores con stack trace completo

## 🔧 Tecnologías

- **Streamlit**: Framework de aplicación web
- **Pandas**: Procesamiento y análisis de datos
- **OpenPyXL**: Exportación a Excel
- **Pandas-Toolkit**: Lectura de múltiples formatos
- **Python Logging**: Sistema de registro de eventos

## ⚡ Características Técnicas

- **Caché de sesión**: Los archivos se procesan una sola vez por sesión
- **Manejo robusto de errores**: Try-catch en operaciones críticas
- **Logging detallado**: Registro de todas las operaciones y errores
- **Detección inteligente**: Identifica automáticamente estructuras de datos
- **Fallback automático**: Si Excel falla, exporta a CSV automáticamente

## 🐛 Troubleshooting

### Error al exportar a Excel
- Revisa si hay columnas con datos anidados
- Usa la opción "Desanidar columnas" o "Convertir a JSON string"
- Como último recurso, exporta a CSV

### Archivo JSON no se carga correctamente
- Verifica que el JSON sea válido
- Asegúrate de que sea un array de objetos o un objeto con estructura tabular

### La aplicación se congela
- Archivos muy grandes pueden tardar en procesarse
- Revisa el uso de memoria del sistema
- Considera dividir el archivo en partes más pequeñas

## 📄 Licencia

