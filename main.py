from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Datos de incidencias
INCIDENCIAS = [
    {"id": 1, "titulo": "Router principal caído", "descripcion": "Router principal sin conexión en sala de servidores", "categoria": "red", "gravedad": 5, "resuelta": False},
    {"id": 2, "titulo": "Disco duro defectuoso", "descripcion": "Servidor DB con disco duro fallando, sectores dañados", "categoria": "hardware", "gravedad": 4, "resuelta": True},
    {"id": 3, "titulo": "Error en base de datos", "descripcion": "Base de datos no responde a consultas", "categoria": "software", "gravedad": 5, "resuelta": False},
    {"id": 4, "titulo": "Cable de red dañado", "descripcion": "Cable ethernet dañado en oficina 3", "categoria": "red", "gravedad": 2, "resuelta": True},
    {"id": 5, "titulo": "Teclado no funciona", "descripcion": "Teclado de PC-15 no responde", "categoria": "hardware", "gravedad": 1, "resuelta": True},
    {"id": 6, "titulo": "Aplicación CRM lenta", "descripcion": "CRM muy lento, timeouts frecuentes", "categoria": "software", "gravedad": 3, "resuelta": False},
    {"id": 7, "titulo": "Switch sin energía", "descripcion": "Switch principal piso 2 sin alimentación", "categoria": "red", "gravedad": 4, "resuelta": False},
    {"id": 8, "titulo": "RAM defectuosa", "descripcion": "Servidor con módulo de memoria fallando", "categoria": "hardware", "gravedad": 5, "resuelta": True},
    {"id": 9, "titulo": "Firewall bloqueando tráfico", "descripcion": "Reglas de firewall mal configuradas", "categoria": "red", "gravedad": 3, "resuelta": True},
    {"id": 10, "titulo": "Licencia de software vencida", "descripcion": "Licencia de antivirus corporativo vencida", "categoria": "software", "gravedad": 4, "resuelta": False},
]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "contenido": "<p>Bienvenido al sistema de gestión de incidencias.</p><p>Ve a <a href='/informe'>/informe</a> para ver el informe completo.</p>",
        },
    )


@app.get("/informe", response_class=HTMLResponse)
async def informe(
    request: Request,
    categoria: Optional[str] = Query(None, description="Filtrar por categoría (red/hardware/software)"),
    min_gravedad: int = Query(1, ge=1, le=5, description="Gravedad mínima (1-5)"),
):
    # Filtrar incidencias
    incidencias_filtradas = []
    for incidencia in INCIDENCIAS:
        # Filtro por categoría
        if categoria is not None and incidencia["categoria"] != categoria:
            continue
        # Filtro por gravedad mínima
        if incidencia["gravedad"] < min_gravedad:
            continue
        incidencias_filtradas.append(incidencia)

    # Calcular resumen
    total_incidencias = len(incidencias_filtradas)
    resueltas = sum(1 for inc in incidencias_filtradas if inc["resuelta"])
    porcentaje_resueltas = (resueltas / total_incidencias * 100) if total_incidencias > 0 else 0

    resumen = {
        "total": total_incidencias,
        "resueltas": resueltas,
        "pendientes": total_incidencias - resueltas,
        "porcentaje_resueltas": round(porcentaje_resueltas, 2),
    }

    # Datos para gráfico de barras (incidencias por categoría)
    categorias = ["red", "hardware", "software"]
    valores_categorias = [
        sum(1 for inc in incidencias_filtradas if inc["categoria"] == cat)
        for cat in categorias
    ]

    # Datos para gráfico de pastel (resueltas vs pendientes)
    labels_estado = ["Resueltas", "Pendientes"]
    valores_estado = [resumen["resueltas"], resumen["pendientes"]]

    return templates.TemplateResponse(
        "informe.html",
        {
            "request": request,
            "incidencias": incidencias_filtradas,
            "resumen": resumen,
            "labels_categorias": categorias,
            "valores_categorias": valores_categorias,
            "labels_estado": labels_estado,
            "valores_estado": valores_estado,
            "categoria": categoria,
            "min_gravedad": min_gravedad,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
