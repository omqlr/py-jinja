from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

TAREAS = [
    {"id": 1, "titulo": "Disenar interfaz", "estado": "pendiente", "prioridad": 3, "horas": 5},
    {"id": 2, "titulo": "Implementar backend", "estado": "en_curso", "prioridad": 5, "horas": 12},
    {"id": 3, "titulo": "Pruebas unitarias", "estado": "pendiente", "prioridad": 2, "horas": 4},
    {"id": 4, "titulo": "Documentar API", "estado": "completada", "prioridad": 4, "horas": 3},
    {"id": 5, "titulo": "Despliegue", "estado": "completada", "prioridad": 5, "horas": 2},
]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "contenido": "<p>Ve a <a href='/informe'>/informe</a> para ver el informe.</p>",
        },
    )


@app.get("/informe", response_class=HTMLResponse)
async def informe(
    request: Request,   
    estado: Optional[str] = Query(None, description="Filtrar por estado"),  #query params
    min_prioridad: int = Query(0, ge=0, le=5, description="Prioridad minima"),
):
    tareas_filtradas = []
    for tarea in TAREAS:
        if estado is not None and tarea["estado"] != estado:
            continue
        if tarea["prioridad"] < min_prioridad:
            continue
        tareas_filtradas.append(tarea)

    total_tareas = len(tareas_filtradas)
    completadas = sum(1 for tarea in tareas_filtradas if tarea["estado"] == "completada")
    porcentaje_completadas = (completadas / total_tareas * 100) if total_tareas > 0 else 0

    resumen = {
        "total": total_tareas,
        "completadas": completadas,
        "porcentaje_completadas": round(porcentaje_completadas, 2),
    }

    estados_posibles = ["pendiente", "en_curso", "completada"]
    labels = estados_posibles
    values = [sum(1 for tarea in tareas_filtradas if tarea["estado"] == e) for e in estados_posibles]

    return templates.TemplateResponse(
        "informe.html",
        {
            "request": request,
            "tareas": tareas_filtradas,
            "resumen": resumen,
            "labels": labels,
            "values": values,
            "estado": estado,
            "min_prioridad": min_prioridad,
        },
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
