# Análisis del Proyecto: Data Tracking Plan Dashboard

Este documento presenta una revisión completa del estado actual del proyecto, identificando puntos fuertes, áreas de mejora y proponiendo un plan de desarrollo para futuras iteraciones.

## 1. Visión General del Proyecto
El proyecto es un **Dashboard basado en Flask** diseñado para visualizar y auditar la implementación de planes de seguimiento (tracking plans) de múltiples fuentes: **Amplitude** (CSV), **Insider** (JSON) y **Google Tag Manager** (JSON). Su objetivo principal es centralizar la información dispersa en exportaciones estáticas para facilitar el análisis de eventos, propiedades y etiquetas.

### Arquitectura Actual
- **Backend**: Python con Flask.
- **Procesamiento de Datos**: Pandas para CSVs, `json` nativo para archivos JSON.
- **Frontend**: Templates Jinja2 con Bootstrap 5 y Chart.js/Plotly para visualizaciones.
- **Estructura**: Monolito simple con separación lógica de parsers (extractores de datos).

---

## 2. Análisis de Código y Buenas Prácticas

### ✅ Puntos Fuertes
1.  **Separación de Responsabilidades**: La lógica de extracción de datos está encapsulada en clases dentro de `parsers/` (`AmplitudeParser`, `InsiderParser`, `GTMParser`), manteniendo `app.py` relativamente limpio de lógica de negocio compleja.
2.  **Tipado Estático**: Uso de Type Hints (`List`, `Dict`) en los parsers, lo cual mejora la legibilidad y ayuda al mantenimiento.
3.  **Uso de Pandas**: Correcta elección para manipular el CSV de Amplitude, facilitando operaciones de filtrado y conteo.
4.  **Configuración Centralizada**: Uso de `config.py` y `pathlib` para manejar rutas de archivos de manera robusta (independiente del sistema operativo).

### ⚠️ Áreas de Mejora y Deuda Técnica

#### A. Estructura y Modularidad
-   **Lógica Duplicada**: Existen scripts sueltos en la raíz (`process_data.py`, `process_events_properties.py`) que duplican la lógica de lectura de archivos presente en los parsers. **Recomendación**: Refactorizar estos scripts para que importen y usen las clases de `parsers/`.
-   **Manejo de Parsers en `app.py`**: La inicialización de parsers usa bloques `try-except` repetitivos. Si se añade una nueva fuente, el código crece verticalmente. Además, `parsers` es una variable global, lo cual no es ideal para aplicaciones escalables (aunque aceptable para este uso de solo lectura).
-   **Ausencia de Blueprints**: Todas las rutas están definidas en `app.py`. Para un crecimiento ordenado, se debería dividir la aplicación en Blueprints (e.g., un blueprint para la API, otro para las vistas HTML).

#### B. Calidad de Código y Testing
-   **Falta de Tests Automatizados**: No existe una suite de pruebas (unitarias o de integración). Si cambia el formato de un CSV o JSON de entrada, la aplicación podría fallar silenciosamente o romper la UI.
-   **Validación de Datos**: Los parsers asumen que los archivos de entrada tienen columnas específicas (e.g., 'Object Type'). Se debería usar una validación más estricta (como **Pydantic** o validación de esquema de Pandas) al cargar los datos para dar mensajes de error más descriptivos si el formato cambia.

#### C. Frontend
-   **Recursos Estáticos**: `charts.js` parece tener lógica de visualización específica mezclada. Sería ideal modularizar el JS si las gráficas se vuelven complejas.
-   **Hardcoding en Templates**: Algunos templates podrían beneficiarse de componentes reutilizables (macros de Jinja2) para tablas y tarjetas de métricas repetitivas.

---

## 3. Seguridad y Rendimiento

-   **Secret Key**: `config.py` tiene una clave por defecto insegura. Aunque es una app local, es buena práctica forzar la carga desde variables de entorno o generar una aleatoria al inicio si no existe.
-   **Carga de Datos**: Los datos se cargan en memoria al inicio (`initialize_parsers`). Si los archivos de exportación crecen mucho (cientos de MBs), esto podría ralentizar el inicio o consumir mucha RAM.
    *   *Mejora*: Implementar carga perezosa (lazy loading) o cacheo inteligente.
-   **Entorno**: Falta un archivo de definición de dependencias más estricto (como `poetry.lock` o `Pipfile.lock`) para asegurar reproducibilidad exacta del entorno.

---

## 4. Posibles Nuevas Integraciones

1.  **Conexión API Directa**:
    *   En lugar de depender de exportaciones manuales (CSV/JSON), conectar directamente a las APIs de **Amplitude** y **GTM** para obtener el esquema en tiempo real.
2.  **Validación contra Esquema Maestro**:
    *   Integrar una definición de "Plan de Tracking Maestro" (puede ser un Google Sheet o un JSON schema) y comparar automáticamente los datos de las plataformas contra este maestro para detectar discrepancias (e.g., "El evento X existe en Amplitude pero no está definido en el Plan").
3.  **Notificaciones (Slack/Email)**:
    *   Alertar cuando se detecten nuevos eventos no documentados o propiedades con tipos de datos incorrectos.
4.  **Autenticación**:
    *   Si se despliega en un servidor compartido, añadir login simple (Flask-Login) para proteger el acceso al dashboard.

---

## 5. Development Plan (Hoja de Ruta)

Para llevar el proyecto al siguiente nivel sin romper la funcionalidad actual, sugiero el siguiente plan:

### Fase 1: Robustez y Limpieza (Inmediato)
1.  **Refactorización de Scripts**: Eliminar lógica duplicada en `process_*.py` haciendo que usen los `parsers` existentes.
2.  **Standardización**: Añadir `black` y `flake8` para asegurar estilo de código consistente.
3.  **Testing Básico**: Crear tests unitarios simples para cada Parser (`tests/test_amplitude_parser.py`, etc.) asegurando que leen correctamente datos de muestra.

### Fase 2: Mejoras de Arquitectura (Corto Plazo)
1.  **Implementar Blueprints**: Mover rutas a `routes/web.py` y `routes/api.py`.
2.  **Validación de Esquema**: Implementar una capa de validación que verifique que los archivos CSV/JSON cargados cumplen con la estructura esperada antes de intentar procesarlos.
3.  **UI Interaciva**: Añadir DataTables.js en el frontend para permitir búsqueda y ordenamiento en las tablas de eventos sin recargar la página.

### Fase 3: Funcionalidades Avanzadas (Mediano Plazo)
1.  **Comparador de Versiones**: Permitir cargar dos versiones del archivo de GTM o Amplitude y mostrar un "Diff" visual de cambios.
2.  **Exportación de Reportes**: Generar un PDF o Excel con el resumen del estado del tracking plan (útil para compartir con stakeholders).
3.  **Integración de APIs**: Crear conectores para descargar los datos automáticamente.

