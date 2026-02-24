import streamlit as st
from pandas_toolkit.io import ReaderFactory
from pandas_toolkit.io.exporter import FileExporter
import pandas as pd
from pathlib import Path
import tempfile
import os
import logging
from datetime import datetime
import traceback

# Configurar logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Crear logger
logger = logging.getLogger('StreamlitApp')
logger.setLevel(logging.INFO)

# Crear handler para archivo
log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Formato del log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Agregar handler al logger
if not logger.handlers:
    logger.addHandler(file_handler)

st.set_page_config(page_title="Lector de Archivos", page_icon="📊", layout="wide")

st.title("📊 Lector de Archivos HTML, CSV y TXT")
st.write("Sube un archivo HTML (con tablas), CSV o TXT y convertilo a Excel o CSV")

# Inicializar session_state para cachear las tablas
if 'tables' not in st.session_state:
    st.session_state.tables = None
    st.session_state.file_id = None

# Upload del archivo
uploaded_file = st.file_uploader("Selecciona un archivo HTML, CSV o TXT", type=['html','csv','txt'])

if uploaded_file is not None:
    # Crear un identificador único del archivo (nombre + tamaño)
    current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    
    # Solo procesar el archivo si es nuevo o diferente
    if st.session_state.file_id != current_file_id:
        # Procesar el archivo automáticamente
        try:
            logger.info(f"Iniciando carga de archivo: {uploaded_file.name} (Tamaño: {uploaded_file.size} bytes)")
            with st.spinner("🔄 Extrayendo tablas..."):
                # Guardar el archivo subido temporalmente
                # Determine file extension based on uploaded file
                file_ext = Path(uploaded_file.name).suffix
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                logger.info(f"Archivo temporal creado: {tmp_path}")
                
                # Factory para leer tablas
                factory = ReaderFactory()                
                tables = factory.create_reader(tmp_path).read_all(tmp_path)                
                
                logger.info(f"Se extrajeron {len(tables)} tabla(s) exitosamente")
                
                # Limpiar archivo temporal
                os.unlink(tmp_path)
                
                # Guardar en session_state
                st.session_state.tables = tables
                st.session_state.file_id = current_file_id
        except Exception as e:
            error_msg = f"Error al procesar el archivo: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback completo:\n{traceback.format_exc()}")
            st.error(f"❌ {error_msg}")
            st.session_state.tables = None
            st.session_state.file_id = None
    
    # Mostrar información del archivo una sola vez
    if st.session_state.tables is not None:
        st.success(f"✅ Archivo cargado: **{uploaded_file.name}**")
        st.success(f"🎉 Se encontraron **{len(st.session_state.tables)}** tabla(s)")
    
    # Usar las tablas del session_state
    if st.session_state.tables is not None:
        tables = st.session_state.tables
        
        # Sección de Vista Previa y Estadísticas
        st.divider()
        st.header("📋 Vista Previa y Estadísticas")
        
        # Almacenar selección de tablas y tablas modificadas
        selected_tables = []
        modified_tables = []  # Guardar versiones modificadas de las tablas
        
        for i, df in enumerate(tables):
            # Crear una copia del dataframe para modificaciones
            df_modified = df.copy()
            with st.expander(f"📊 Tabla {i+1}", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"Vista Previa (primeras 10 filas)")
                    st.dataframe(df.head(10), width='stretch')
                
                with col2:
                    st.subheader("📈 Estadísticas")
                    st.metric("Filas", df.shape[0])
                    st.metric("Columnas", df.shape[1])
                    
                    # Valores nulos
                    null_count = df.isnull().sum().sum()
                    st.metric("Valores Nulos", null_count)
                    
                    # Valores duplicados
                    dup_count = df.duplicated().sum()
                    st.metric("Filas Duplicadas", dup_count)
                    
                    st.write("**Tipos de datos:**")
                    type_counts = df.dtypes.value_counts()
                    for dtype, count in type_counts.items():
                        st.write(f"• {dtype}: {count}")
                
                # Sección de Edición de Columnas
                st.divider()
                st.subheader("✏️ Editar Columnas")
                
                # Opción para eliminar columnas
                st.write("**🗑️ Eliminar Columnas**")
                cols_to_remove = st.multiselect(
                    "Selecciona las columnas que deseas eliminar:",
                    options=list(df_modified.columns),
                    key=f"remove_cols_{i}",
                    help="Las columnas seleccionadas se eliminarán antes de exportar"
                )
                
                if cols_to_remove:
                    df_modified = df_modified.drop(columns=cols_to_remove)
                    st.info(f"✅ Se eliminarán {len(cols_to_remove)} columna(s)")
                
                # Opción para renombrar columnas
                st.write("**✏️ Renombrar Columnas**")
                rename_expander = st.expander("Cambiar nombres de columnas")
                with rename_expander:
                    rename_dict = {}
                    remaining_cols = [col for col in df.columns if col not in cols_to_remove]
                    
                    if remaining_cols:
                        st.write("Ingresa los nuevos nombres (deja en blanco para mantener el original):")
                        col_rename_left, col_rename_right = st.columns(2)
                        
                        for idx, col in enumerate(remaining_cols):
                            with col_rename_left if idx % 2 == 0 else col_rename_right:
                                new_name = st.text_input(
                                    f"**{col}**",
                                    value="",
                                    key=f"rename_{i}_{col}",
                                    placeholder=f"Nuevo nombre para '{col}'"
                                )
                                if new_name and new_name != col:
                                    rename_dict[col] = new_name
                        
                        if rename_dict:
                            df_modified = df_modified.rename(columns=rename_dict)
                            st.success(f"✅ Se renombrarán {len(rename_dict)} columna(s)")
                    else:
                        st.warning("No hay columnas disponibles para renombrar (todas fueron eliminadas)")
                
                # Vista previa de cambios
                if cols_to_remove or rename_dict:
                    st.write("**👀 Vista Previa con Cambios:**")
                    st.dataframe(df_modified.head(5), width='stretch')
                
                # Guardar la tabla modificada
                modified_tables.append(df_modified)
                
                # Checkbox para seleccionar esta tabla
                is_selected = st.checkbox(
                    f"✅ Incluir Tabla {i+1} en exportación",
                    value=True,
                    key=f"select_table_{i}"
                )
                selected_tables.append(is_selected)
        
        # Sección de Exportación
        st.divider()
        st.header("💾 Exportación")
        
        # Contar tablas seleccionadas
        num_selected = sum(selected_tables)
        
        if num_selected == 0:
            st.warning("⚠️ No has seleccionado ninguna tabla para exportar")
        else:
            st.info(f"📊 Has seleccionado **{num_selected}** de {len(tables)} tabla(s)")
            
            col1, col2 = st.columns(2)
            with col1:
                export_to_csv = st.checkbox("📄 Exportar a CSV (un archivo por tabla)", value=False)
            with col2:
                include_index = st.checkbox("Incluir índice en exportación", value=False)
            
            # Extraer el nombre del archivo sin extensión
            nombre_archivo = Path(uploaded_file.name).stem
            
            # Botón de exportar
            button_label = "🚀 Exportar a CSV" if export_to_csv else "🚀 Exportar a Excel"
            if st.button(button_label, type="primary", width='stretch'):
                try:
                    logger.info(f"Iniciando exportación - Formato: {'CSV' if export_to_csv else 'Excel'}, Tablas seleccionadas: {sum(selected_tables)}")
                    with st.spinner("📦 Generando archivo(s)..."):
                        # Filtrar solo las tablas seleccionadas (usar tablas modificadas)
                        selected_dfs = [modified_tables[i] for i in range(len(modified_tables)) if selected_tables[i]]
                        
                        # Crear carpeta output si no existe
                        output_dir = Path('output')
                        output_dir.mkdir(exist_ok=True)
                        
                        # Exportar según formato seleccionado
                        if export_to_csv:
                            # Exportar cada tabla seleccionada a un CSV separado
                            csv_files = []
                            tabla_counter = 1
                            for i, df in enumerate(modified_tables):
                                if selected_tables[i]:
                                    csv_path = output_dir / f'{nombre_archivo}_tabla_{tabla_counter}.csv'
                                    df.to_csv(csv_path, index=include_index, encoding='utf-8-sig')
                                    csv_files.append(csv_path)
                                    logger.info(f"CSV exportado: {csv_path.name} ({df.shape[0]} filas, {df.shape[1]} columnas)")
                                    tabla_counter += 1
                            
                            logger.info(f"Exportación CSV completada: {len(csv_files)} archivo(s)")
                            st.success(f"✅ Exportadas **{len(csv_files)}** tabla(s) a CSV exitosamente!")
                            st.info(f"📁 Guardados en carpeta: output/")
                            
                            # Mostrar archivos generados
                            st.write("**Archivos disponibles para descarga:**")
                            for csv_file in csv_files:
                                with open(csv_file, 'rb') as f:
                                    st.download_button(
                                        label=f"⬇️ Descargar {csv_file.name}",
                                        data=f.read(),
                                        file_name=csv_file.name,
                                        mime='text/csv',
                                        key=f"download_{csv_file.name}"
                                    )
                        else:
                            # Intentar exportar a Excel
                            try:
                                #MODIFICADOOOO
                                output_path = output_dir / f'{nombre_archivo}.xlsx'
                                exporter = FileExporter(output_dir=output_dir)
                                exporter.export_tables(modified_tables, filename=f'{nombre_archivo}.xlsx')

                                # with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                                #     sheet_counter = 1
                                #     for i, df in enumerate(modified_tables):
                                #         if selected_tables[i]:
                                #             df.to_excel(writer, sheet_name=f'Tabla{sheet_counter}', index=include_index)
                                #             logger.info(f"Hoja Excel creada: Tabla{sheet_counter} ({df.shape[0]} filas, {df.shape[1]} columnas)")
                                #             sheet_counter += 1


                                
                                logger.info(f"Exportación Excel completada: {output_path.name}")
                                st.success(f"✅ Archivo exportado a Excel exitosamente!")
                                st.info(f"📁 Guardado en: {output_path}")
                                
                                # Botón de descarga
                                with open(output_path, 'rb') as f:
                                    st.download_button(
                                        label="⬇️ Descargar Excel",
                                        data=f.read(),
                                        file_name=f'{nombre_archivo}.xlsx',
                                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                    )
                            except Exception as excel_error:
                                logger.error(f"Error en exportación Excel: {str(excel_error)}")
                                logger.error(f"Traceback Excel:\n{traceback.format_exc()}")
                                st.warning(f"⚠️ No se pudo exportar a Excel: {str(excel_error)}")
                                st.info("🔄 Intentando exportar a CSV como fallback...")
                                
                                # Fallback a CSV
                                csv_files = []
                                tabla_counter = 1
                                for i, df in enumerate(modified_tables):
                                    if selected_tables[i]:
                                        csv_path = output_dir / f'{nombre_archivo}_tabla_{tabla_counter}.csv'
                                        df.to_csv(csv_path, index=include_index, encoding='utf-8-sig')
                                        csv_files.append(csv_path)
                                        logger.info(f"CSV fallback exportado: {csv_path.name}")
                                        tabla_counter += 1
                                
                                logger.info(f"Fallback CSV completado: {len(csv_files)} archivo(s)")
                                st.success(f"✅ Exportadas **{len(csv_files)}** tabla(s) a CSV exitosamente!")
                                st.info(f"📁 Guardados en carpeta: output/")
                                
                                # Mostrar archivos generados
                                st.write("**Archivos disponibles para descarga:**")
                                for csv_file in csv_files:
                                    with open(csv_file, 'rb') as f:
                                        st.download_button(
                                            label=f"⬇️ Descargar {csv_file.name}",
                                            data=f.read(),
                                            file_name=csv_file.name,
                                            mime='text/csv',
                                            key=f"download_fallback_{csv_file.name}"
                                        )
                        
                except Exception as e:
                    error_msg = f"Error al exportar: {str(e)}"
                    logger.error(error_msg)
                    logger.error(f"Traceback exportación:\n{traceback.format_exc()}")
                    st.error(f"❌ {error_msg}")

else:
    # Limpiar session_state si no hay archivo
    st.session_state.tables = None
    st.session_state.file_id = None
    
    st.info("👆 Por favor, sube un archivo HTML para comenzar")    
    # Sección de ayuda y características
    st.divider()
    st.header("✨ Características")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Vista Previa")
        st.write("• Visualiza tus tablas antes de exportar")
        st.write("• Primeras 10 filas de cada tabla")
        st.write("• Interfaz interactiva y responsive")
    
    with col2:
        st.subheader("📈 Estadísticas")
        st.write("• Cantidad de filas y columnas")
        st.write("• Detección de valores nulos")
        st.write("• Identificación de duplicados")
        st.write("• Tipos de datos por columna")
    
    with col3:
        st.subheader("💾 Exportación Flexible")
        st.write("• Selecciona tablas específicas")
        st.write("• Elimina columnas innecesarias")
        st.write("• Renombra columnas fácilmente")
        st.write("• Exporta a Excel o CSV")
        st.write("• Opción de incluir índice")
        st.write("• Descarga directa desde el navegador")

# Sidebar con información adicional
with st.sidebar:
    st.header("ℹ️ Información")
    st.write("**Versión:** 2.0")
    st.write("**Última actualización:** Feb 2026")
    
    st.divider()
    
    st.subheader("📖 Instrucciones")
    st.write("""
    1. Sube un archivo HTML con tablas
    2. Revisa la vista previa y estadísticas
    3. Edita columnas (eliminar/renombrar)
    4. Selecciona las tablas a exportar
    5. Elige el formato (Excel/CSV)
    6. Haz clic en Exportar
    7. Descarga tus archivos
    """)
    
    st.divider()
    
    st.subheader("🎯 Formatos Soportados")
    st.write("• **Entrada:** HTML")
    st.write("• **Salida:** Excel (.xlsx), CSV (.csv)")
    
    st.divider()
    
    st.subheader("💡 Consejos")
    st.info("Puedes eliminar columnas innecesarias y renombrar las que necesites antes de exportar para tener un archivo final más limpio y profesional.")
    
    st.divider()
    
    st.subheader("📋 Logs de Actividad")
    if st.button("Ver logs de hoy", key="view_logs"):
        log_file = log_dir / f'app_{datetime.now().strftime("%Y%m%d")}.log'
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                logs_content = f.read()
                st.text_area("Logs:", logs_content, height=300)
        else:
            st.info("No hay logs disponibles para hoy")
    
    st.caption(f"📁 Logs guardados en: logs/")