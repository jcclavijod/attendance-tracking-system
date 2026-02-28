# Attendance Tracking system

## 📌 Resumen del Proyecto

En el contexto universitario, uno de los desafíos frecuentes es **monitorear y analizar la asistencia de los estudiantes** para poder identificar patrones de participación, detectar estudiantes que requieren seguimiento y generar reportes precisos para administración o docentes. La información de asistencia puede provenir de múltiples fuentes, como sistemas de control de acceso o registros manuales, y suele llegar en formato de texto o archivos simples, lo que requiere **procesamiento confiable y estandarizado**.

Este proyecto implementa un sistema de registro y análisis de asistencia de estudiantes universitarios, pensado para ser **escalable y extensible**, diseñado para procesar un archivo de entrada con un formato predefinido. Cada línea del archivo representa un evento y puede ser de dos tipos:

1. **Registro de estudiante**  
   Formato: `Student <Nombre>`  
   Ejemplo:  
```bash
        Student Marco
        Student David
        Student Fran
```
2. **Registro de presencia**  
    Formato: `Presence <Nombre> <Día> <HoraInicio> <HoraFin> <Sala>`  
    Donde:
- Día: número del 1 al 7 representando el día de la semana.
- HoraInicio y HoraFin: formato `HH:MM` en 24 horas.
- Sala: código de la sala donde se registró la presencia.  
    Ejemplo:
```bash
        Presence Marco 1 09:02 10:17 R100
        Presence Marco 3 10:58 12:05 R205
        Presence David 5 14:02 15:46 F505
```

**Reglas de negocio importantes**:
- Se descartan presencias menores a 5 minutos automáticamente.
- No se permiten presencias fuera del rango horario válido (inicio < fin).
- Estudiantes no registrados que tengan presencias generan un warning y su evento se ignora.
- Se calcula la duración total de asistencia y los días distintos de asistencia por estudiante.

### Ejemplo de salida esperada

El sistema genera un reporte con la siguiente información:
- Nombre del estudiante.
- Total de minutos de asistencia (sumando todas las presencias válidas).
- Cantidad de días distintos que asistió.

    Ejemplo de salida:
```bash
        Marco: 142 minutes in 2 days
        David: 104 minutes in 1 day
        Fran: 0 minutes
```
---

## 🏗 Arquitectura y Decisiones de Diseño

La solución implementada se basa en una **arquitectura modular y en capas**, inspirada en principios de Clean Architecture y Domain-Driven Design (DDD), que permite separar responsabilidades claramente, facilitar la escalabilidad del sistema y garantizar la mantenibilidad del código.  

El flujo general de la aplicación es el siguiente:  
1. Se recibe el input desde un archivo o entrada estándar.  
2. Se parsean las líneas a eventos estructurados (`Student` y `Presence`).  
3. Se registran los estudiantes y sus presencias en el servicio de aplicación (`AttendanceService`).  
4. Se generan reportes finales ordenados por minutos de asistencia y días de asistencia distintos, listando incluso a estudiantes sin presencia.  

Esta separación asegura que cambios en la entrada, nuevas reglas de negocio o ampliaciones de reportes no afecten el resto del sistema.


### Estructura de Carpetas y Capas
```bash
attendance/
├── application/
│   ├── attendance_application.py
│   ├── attendance_service.py
│   └── attendance_report_generator.py
├── domain/
│   ├── student.py
│   └── presence_record.py
├── infrastructure/
│   ├── input_parser.py
│   └── logging_config.py
├── settings.py
└── __init__.py

tests/
├── test_input_parser.py
├── test_attendance_service.py
└── test_attendance_report_generator.py

cli.py
requirements.txt
readme.md
```
### 1️⃣ Capa de Dominio (Domain Layer)

**Propósito:** Contiene la lógica de negocio central, independiente de cómo se recibe o presenta la información.  

**Clases principales:**
- `Student`  
  - Representa un estudiante universitario.  
  - Gestiona las presencias válidas, calcula minutos totales y días distintos de asistencia.
- `PresenceRecord`  
  - Value Object inmutable que representa una presencia en un día y sala específica.  
  - Calcula la duración de la asistencia en minutos.  

**Responsabilidades clave:**
- Centralizar las reglas de negocio (p. ej., ignorar presencias menores a 5 minutos).  
- Garantizar consistencia y validación de datos de asistencia.  
- Mantener independencia de cualquier formato de entrada o salida.  

**Beneficio:**  
El dominio queda aislado, lo que permite cambiar input/output sin afectar la lógica principal, facilitando futuras ampliaciones y mantenibilidad.

---

### 2️⃣ Capa de Aplicación (Application Layer)

**Propósito:** Coordina la lógica de negocio y el flujo de la aplicación. Esta capa no tiene conocimiento de formatos de entrada ni de salida.  

**Clases principales:**
- `AttendanceService`  
  - Gestiona la creación de estudiantes y el registro de presencias.  
  - Valida existencia de estudiantes y delega reglas de negocio al dominio.  
- `AttendanceReportGenerator`  
  - Genera reportes finales formateados y ordenados según minutos de asistencia.  
- `AttendanceApplication`  
  - Orquesta el flujo completo: recibe eventos parseados, registra datos y genera el reporte.  

**Responsabilidades clave:**
- Interpretar los eventos parseados por la capa de infraestructura.  
- Delegar la lógica de validación y cálculo al dominio.  
- Garantizar que el flujo completo de registro y reporte funcione sin interrupciones.  

**Beneficio:**  
Permite que la lógica de negocio permanezca centralizada en el dominio y facilita la escalabilidad del sistema (por ejemplo, agregar nuevos tipos de reportes o integrar bases de datos externas).

---

### 3️⃣ Capa de Infraestructura (Infrastructure Layer)

**Propósito:** Gestiona la interacción con el mundo externo: parsing de input y logging.  

**Clases principales:**
- `InputParser`  
  - Convierte líneas de texto en eventos estructurados (`StudentEvent` y `PresenceEvent`).  
  - Aísla el formato del input del resto del sistema.  
- `logging_config`  
  - Configuración centralizada de logs para todo el sistema.  
  - Registra errores, advertencias e información de auditoría.  

**Responsabilidades clave:**
- Validar estructura mínima del input (cantidad de campos, tipo de datos).  
- Reportar errores y advertencias sin detener la ejecución del sistema.  
- Mantener independencia del dominio y de la aplicación.  

**Beneficio:**  
El sistema **no falla ante input inválido**, y cualquier cambio en el formato de entrada solo afecta esta capa. Esto permite escalar fácilmente a otros formatos (CSV, JSON) sin tocar la lógica de negocio.

---

## 🎯 Decisiones Clave y Escalabilidad

Aunque este problema podría resolverse con una sola función, se tomó la decisión intencional de estructurar la solución para garantizar:

- **Separación de responsabilidades (Separation of Concerns):**  
  Cada capa (Dominio, Aplicación e Infraestructura) tiene funciones claras y limitadas. Esto significa que cambios en el input o la presentación no afectan las reglas de negocio, y nuevas reglas de negocio no requieren modificar la capa de presentación ni parsing.

- **Encapsulación de reglas de negocio:**  
  Las validaciones y cálculos relacionados con asistencia están centralizados en el dominio (`Student` y `PresenceRecord`). Esto evita duplicación de lógica, asegura consistencia y facilita la implementación de nuevas reglas.

- **Manejo de errores:**  
  La solución fue diseñada para manejar entradas incorrectas o inesperadas de forma segura:
  - Presencia de estudiante no registrado → `WARNING`, evento ignorado.  
  - Línea de input incompleta o mal formateada → `ERROR` indicando línea y posición.  
  - Error inesperado al registrar presencia → `ERROR`, evento omitido y el procesamiento continúa.  
  Esto garantiza que el sistema no se detenga por errores de input y permite auditoría de los eventos procesados.

- **Testabilidad:**  
  Se implementaron tests unitarios que cubren los componentes principales que encapsulan la lógica del sistema:
  - `InputParser`: parsing de eventos válidos e inválidos.  
  - `AttendanceService`: registro de estudiantes y presencias, incluyendo reglas de negocio. 
  - `AttendanceReportGenerator`: generación de reportes y ordenamiento de resultados. 

  Aunque no hay tests separados para cada capa, la estructura modular permite **verificar el comportamiento central de manera aislada**, asegurando que refactorizaciones futuras sean predecibles y seguras.

- **Escalabilidad y extensibilidad:**  
  - Nuevos tipos de entrada (CSV, JSON) solo afectan la capa de infraestructura.  
  - Nuevos reportes o formatos solo afectan `AttendanceReportGenerator`.  
  - La integración con sistemas externos, dashboards o bases de datos se puede agregar como adaptadores independientes.  
  - Reglas de negocio adicionales se implementan en el dominio sin tocar la aplicación ni la infraestructura.

---

## ⚙️ Instalación y Ejecución

Para ejecutar el proyecto requiere **Python 3.14 o superior**, ademas se recomienda usar un entorno virtual y luego instalar las dependencias. Todos los comandos se ejecutan desde la terminal dentro del directorio raíz del proyecto.

1. **Crear un entorno virtual (recomendado):**

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la aplicación:

Usando archivo de entrada:
```bash
python cli.py input.txt
```

Usando entrada estándar:
```bash
cat input.txt | python cli.py
```

---

## 🧪 Running Tests
```bash
pytest -v
```
Los tests cubren los componentes centrales:

Parsing de eventos (InputParser)

Registro y validación de estudiantes y presencias (AttendanceService)

Generación de reportes y ordenamiento (AttendanceReportGenerator)

---

## 🔧 Requirements

- Python 3.14+
- pytest (for running tests)

Install dependencies:

pip install -r requirements.txt

---

## 🧠 Final Notes

El enfoque de esta solución no está en la complejidad algorítmica, sino en la claridad del modelado y la mantenibilidad.  

La lógica de negocio está aislada, es fácil de probar y está diseñada intencionalmente para reflejar un código listo para producción.