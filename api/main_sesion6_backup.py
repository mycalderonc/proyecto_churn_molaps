"""
API de predicción de churn con FastAPI.

Servicio de inferencia para un modelo de Machine Learning
orientado a estimar el riesgo de abandono de clientes.
"""

from pathlib import Path
import logging

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# ==========================================================
# Configuración
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1.joblib"

VERSION_MODELO = "1.0.0"
NOMBRE_MODELO = "modelo_churn_v1"
AUTOR = "Maria Yamile Calderon Cardenas"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================================
# Carga del modelo
# ==========================================================

if not MODEL_PATH.exists():
    raise RuntimeError(
        f"No se encontró el modelo en: {MODEL_PATH}"
    )

modelo = joblib.load(MODEL_PATH)

logger.info("Modelo cargado correctamente")

# ==========================================================
# Esquemas de entrada y salida
# ==========================================================

class ClienteEntrada(BaseModel):
    antiguedad: int = Field(
        ...,
        ge=0,
        le=120,
        description="Antigüedad del cliente en meses"
    )

    cargo_mensual: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Monto facturado mensualmente"
    )

    reclamos: int = Field(
        ...,
        ge=0,
        le=50,
        description="Número de reclamos recientes"
    )


class PrediccionSalida(BaseModel):
    prediccion: str
    probabilidad: float
    version_modelo: str
    nombre_modelo: str
    autor: str


# ==========================================================
# Aplicación FastAPI
# ==========================================================

app = FastAPI(
    title="API de Predicción de Churn",
    description=(
        "Servicio de inferencia para estimar el riesgo "
        "de abandono de clientes."
    ),
    version=VERSION_MODELO,
)

# ==========================================================
# Endpoints
# ==========================================================

@app.get(
    "/",
    tags=["General"],
    summary="Estado general del servicio"
)
def inicio():

    return {
        "estado": "ok",
        "mensaje": "Servicio ML-Ops operativo",
        "modelo": NOMBRE_MODELO,
        "version": VERSION_MODELO,
        "autor": AUTOR
    }


@app.get(
    "/health",
    tags=["Monitoreo"],
    summary="Health Check"
)
def health():

    return {
        "estado": "healthy",
        "modelo": NOMBRE_MODELO,
        "version": VERSION_MODELO
    }


@app.post(
    "/predict",
    response_model=PrediccionSalida,
    tags=["Predicción"],
    summary="Predicción de riesgo de abandono"
)
def predict(datos: ClienteEntrada):

    try:

        caracteristicas = [[
            datos.antiguedad,
            datos.cargo_mensual,
            datos.reclamos
        ]]

        if not hasattr(modelo, "predict_proba"):
            raise ValueError(
                "El modelo cargado no soporta predict_proba"
            )

        probabilidad = float(
            modelo.predict_proba(caracteristicas)[0][1]
        )

        prediccion = (
            "alto_riesgo - Promociona"
            if probabilidad >= 0.50
            else "bajo_riesgo"
        )

        logger.info(
            f"Predicción realizada. "
            f"Probabilidad={probabilidad:.4f}"
        )

        return PrediccionSalida(
            prediccion=prediccion,
            probabilidad=round(probabilidad, 4),
            version_modelo=VERSION_MODELO,
            nombre_modelo=NOMBRE_MODELO,
            autor=AUTOR,
        )

    except Exception as exc:

        logger.error(
            f"Error durante la inferencia: {str(exc)}"
        )

        raise HTTPException(
            status_code=500,
            detail="Error interno durante la generación de la predicción."
        ) from exc

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "estado": "error",
            "mensaje": (
                "Los datos enviados no cumplen con el formato esperado. "
                "Verifique los campos antiguedad, cargo_mensual y reclamos."
            )
        }
    )