# Memoria Técnica - Informe Web de Incidencias

## 1. Estructura del Informe

### 1.1 Arquitectura de la Aplicación

La aplicación sigue el patrón **MVC** (Modelo-Vista-Controlador) adaptado a FastAPI:

- **Modelo**: Datos de incidencias almacenados en la lista `INCIDENCIAS` en `main.py`
- **Vista**: Plantillas Jinja2 (`base.html` y `informe.html`)
- **Controlador**: Rutas FastAPI que procesan peticiones y renderizan plantillas

### 1.2 Componentes Principales

#### Backend (`main.py`)
- **Ruta `/`**: Página de bienvenida
- **Ruta `/informe`**: Informe principal con filtros
- **Datos**: 10 incidencias con estructura:
  ```python
  {
    "id": int,
    "titulo": str,
    "descripcion": str,
    "categoria": "red" | "hardware" | "software",
    "gravedad": int (1-5),
    "resuelta": bool
  }
  ```

#### Frontend (Templates)
- **`base.html`**: Plantilla base con estilos CSS modernos
- **`informe.html`**: Extiende `base.html`, contiene:
  - Formulario de filtros
  - Resumen estadístico
  - Tabla de incidencias
  - Dos gráficos Chart.js

---

## 2. Filtros Implementados

### 2.1 Filtro por Categoría

**Parámetro**: `categoria` (opcional)

**Valores posibles**:
- `red`: Incidencias de red (routers, switches, cables)
- `hardware`: Incidencias de hardware (discos, RAM, teclados)
- `software`: Incidencias de software (aplicaciones, bases de datos)
- `null` (vacío): Muestra todas las categorías

**Implementación**:
```python
if categoria is not None and incidencia["categoria"] != categoria:
    continue
```

### 2.2 Filtro por Gravedad Mínima

**Parámetro**: `min_gravedad` (obligatorio, default=1)

**Valores posibles**: 1 a 5

**Comportamiento**: Muestra solo incidencias con `gravedad >= min_gravedad`

**Implementación**:
```python
if incidencia["gravedad"] < min_gravedad:
    continue
```

### 2.3 Combinación de Filtros

Los filtros se aplican de forma **acumulativa** (AND lógico):
- Ejemplo: `categoria=red&min_gravedad=4` → Solo incidencias de red con gravedad >= 4

---

## 3. Cálculos de Totales

### 3.1 Resumen Estadístico

El sistema calcula automáticamente:

1. **Total de incidencias filtradas**:
   ```python
   total_incidencias = len(incidencias_filtradas)
   ```

2. **Incidencias resueltas**:
   ```python
   resueltas = sum(1 for inc in incidencias_filtradas if inc["resuelta"])
   ```

3. **Incidencias pendientes**:
   ```python
   pendientes = total_incidencias - resueltas
   ```

4. **Porcentaje de resolución**:
   ```python
   porcentaje_resueltas = (resueltas / total_incidencias * 100) if total_incidencias > 0 else 0
   ```

### 3.2 Datos para Gráficos

#### Gráfico 1: Incidencias por Categoría
```python
categorias = ["red", "hardware", "software"]
valores_categorias = [
    sum(1 for inc in incidencias_filtradas if inc["categoria"] == cat)
    for cat in categorias
]
```

#### Gráfico 2: Estado de Resolución
```python
labels_estado = ["Resueltas", "Pendientes"]
valores_estado = [resumen["resueltas"], resumen["pendientes"]]
```

---

## 4. Modificación Realizada en la Plantilla ✨

### 4.1 Descripción del Cambio

**Modificación obligatoria**: Se agregó un **segundo gráfico** (pie chart) que muestra el estado de resolución de las incidencias.

### 4.2 Justificación

El enunciado requería modificar la plantilla agregando:
- Una nueva sección/columna **O**
- Un segundo gráfico

**Elección**: Segundo gráfico (pie chart) porque:
1. Complementa la información del gráfico de barras
2. Proporciona una visualización clara del porcentaje de resolución
3. Mejora la experiencia del usuario con información visual adicional
4. Es más útil que una columna adicional en la tabla

### 4.3 Implementación Técnica

**Ubicación**: `templates/informe.html`, líneas 107-170

**Código HTML**:
```html
<h2>🥧 Gráfico 2: Estado de Resolución (Resueltas vs Pendientes)</h2>
<div style="background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
  <canvas id="graficoEstado" width="400" height="400"></canvas>
</div>
```

**Código JavaScript (Chart.js)**:
```javascript
const ctxEstado = document.getElementById("graficoEstado").getContext("2d");
new Chart(ctxEstado, {
  type: "pie",
  data: {
    labels: ["Resueltas", "Pendientes"],
    datasets: [{
      data: valoresEstado,
      backgroundColor: [
        "rgba(16, 185, 129, 0.8)",  // Verde para resueltas
        "rgba(239, 68, 68, 0.8)",    // Rojo para pendientes
      ],
    }],
  },
  options: {
    responsive: true,
    plugins: {
      tooltip: {
        callbacks: {
          label: function(context) {
            // Muestra valor y porcentaje
            let value = context.parsed;
            let total = context.dataset.data.reduce((a, b) => a + b, 0);
            let percentage = ((value / total) * 100).toFixed(1);
            return context.label + ': ' + value + ' (' + percentage + '%)';
          }
        }
      }
    }
  }
});
```

### 4.4 Características del Gráfico

- **Tipo**: Pie chart (gráfico de pastel)
- **Datos**: Número de incidencias resueltas vs pendientes
- **Colores**: Verde para resueltas, rojo para pendientes
- **Interactividad**: Tooltip muestra valor absoluto y porcentaje
- **Responsive**: Se adapta al tamaño de la pantalla

### 4.5 Beneficios

1. **Visual**: Permite ver de un vistazo el estado general del sistema
2. **Complementario**: Junto con el gráfico de barras, ofrece una visión completa
3. **Informativo**: El porcentaje en el tooltip ayuda a tomar decisiones
4. **Profesional**: Mejora la presentación del informe

---

## 5. Tecnologías y Librerías

### 5.1 Backend
- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Jinja2**: Motor de plantillas

### 5.2 Frontend
- **Chart.js 4.x**: Librería de gráficos interactivos
- **CSS3**: Estilos modernos con gradientes y animaciones
- **HTML5**: Estructura semántica

### 5.3 Características de Diseño
- Gradientes de color (#667eea → #764ba2)
- Sombras y bordes redondeados
- Efectos hover en tablas y botones
- Diseño responsive
- Iconos emoji para mejor UX

---

## 6. Flujo de Datos

```
Usuario → Navegador
    ↓
Solicitud HTTP GET /informe?categoria=red&min_gravedad=4
    ↓
FastAPI (main.py)
    ↓
Filtrado de INCIDENCIAS
    ↓
Cálculo de estadísticas
    ↓
Preparación de datos para gráficos
    ↓
Renderizado de plantilla Jinja2
    ↓
HTML + JavaScript (Chart.js)
    ↓
Navegador muestra informe con gráficos
```

---

## 7. Posibles Mejoras Futuras

1. **Persistencia**: Usar base de datos (SQLite, PostgreSQL)
2. **CRUD**: Permitir crear, editar y eliminar incidencias
3. **Autenticación**: Sistema de usuarios y roles
4. **Exportación**: Generar PDF o Excel del informe
5. **Notificaciones**: Alertas para incidencias críticas
6. **Dashboard**: Página principal con métricas generales
7. **Historial**: Registro de cambios en incidencias
8. **API REST**: Endpoints JSON para integración con otros sistemas

---

## 8. Conclusiones

El proyecto cumple con todos los requisitos del enunciado:

✅ Ruta `/informe` con generación de HTML  
✅ Filtros por categoría y gravedad mínima  
✅ Resumen con estadísticas (total, resueltas, %)  
✅ Tabla con incidencias filtradas  
✅ Gráfico Chart.js (incidencias por categoría)  
✅ Plantillas Jinja2 (base.html + informe.html)  
✅ **Modificación obligatoria**: Segundo gráfico (pie chart)  

El sistema es funcional, visualmente atractivo y fácil de usar, cumpliendo con los objetivos de la práctica de Desarrollo de Interfaces.
