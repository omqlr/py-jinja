# 🔧 Informe Web de Incidencias

Sistema de gestión y visualización de incidencias técnicas desarrollado con **FastAPI** y **Jinja2**.

## 📋 Descripción

Aplicación web que permite visualizar y filtrar incidencias de sistemas (red, hardware, software) con gráficos interactivos y estadísticas en tiempo real.

## ✨ Características

- 📊 **Filtros dinámicos**: Por categoría (red/hardware/software) y gravedad (1-5)
- 📈 **Estadísticas en tiempo real**: Total, resueltas, pendientes y porcentajes
- 📉 **Gráficos interactivos con Chart.js**:
  - Gráfico de barras: Incidencias por categoría
  - Gráfico de pastel: Estado de resolución (resueltas vs pendientes)
- 🎨 **Diseño moderno**: Interfaz responsive con gradientes y animaciones
- 🔍 **Tabla detallada**: Información completa de cada incidencia

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip

### Pasos

1. **Clonar o descargar el repositorio**

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python main.py
   ```

4. **Abrir en el navegador**:
   ```
   http://127.0.0.1:8000
   ```

## 📂 Estructura del Proyecto

```
Py-jinja/
├── main.py                 # Backend FastAPI con rutas y lógica
├── requirements.txt        # Dependencias del proyecto
├── templates/
│   ├── base.html          # Plantilla base con estilos
│   └── informe.html       # Plantilla del informe con gráficos
├── README.md              # Este archivo
└── MEMORIA.md             # Documentación técnica
```

## 🎯 Uso

### Página principal
Accede a `http://127.0.0.1:8000/` para ver la página de bienvenida.

### Informe de incidencias
Accede a `http://127.0.0.1:8000/informe` para ver el informe completo.

### Filtros disponibles

**Por categoría**:
- 🌐 Red
- 💻 Hardware
- ⚙️ Software
- (Todas)

**Por gravedad mínima**:
- Valores de 1 a 5
- Muestra solo incidencias con gravedad >= valor seleccionado

### Ejemplos de URLs con filtros

```
# Solo incidencias de red
http://127.0.0.1:8000/informe?categoria=red

# Solo incidencias con gravedad >= 4
http://127.0.0.1:8000/informe?min_gravedad=4

# Incidencias de hardware con gravedad >= 3
http://127.0.0.1:8000/informe?categoria=hardware&min_gravedad=3
```

## 📊 Gráficos

### Gráfico 1: Incidencias por Categoría
- **Tipo**: Gráfico de barras
- **Muestra**: Número de incidencias en cada categoría (red, hardware, software)
- **Interactivo**: Hover para ver valores exactos

### Gráfico 2: Estado de Resolución ✨
- **Tipo**: Gráfico de pastel (pie chart)
- **Muestra**: Porcentaje de incidencias resueltas vs pendientes
- **Modificación obligatoria**: Este segundo gráfico fue agregado como requisito del ejercicio

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI
- **Servidor**: Uvicorn
- **Templates**: Jinja2
- **Gráficos**: Chart.js
- **Estilos**: CSS3 con gradientes y animaciones

## 📝 Datos de Ejemplo

La aplicación incluye 10 incidencias de ejemplo con diferentes categorías y niveles de gravedad:
- 4 incidencias de red
- 3 incidencias de hardware
- 3 incidencias de software

## 👨‍💻 Autor

Desarrollado como práctica de Desarrollo de Interfaces (RA5)

## 📄 Licencia

Proyecto educativo - Libre uso para aprendizaje
