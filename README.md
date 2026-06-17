# Proyecto Churn MLOps

## Descripción

Este proyecto implementa una solución de Machine Learning Operations (ML-Ops) para la predicción de abandono de clientes (Churn Prediction).

La solución incluye el entrenamiento de un modelo de Machine Learning, su despliegue mediante una API desarrollada con FastAPI, ejecución dentro de contenedores Docker y una capa básica de observabilidad para monitoreo operativo.

## Objetivo

Desarrollar una API predictiva capaz de identificar clientes con riesgo de abandono, incorporando prácticas fundamentales de ML-Ops como:

* Despliegue de modelos.
* Validación de datos.
* Monitoreo operativo.
* Registro de eventos (logging).
* Detección de anomalías.
* Gestión básica de métricas.
* Contenerización mediante Docker.

---

## Problema de negocio

La pérdida de clientes representa un desafío para las organizaciones debido al impacto económico asociado a la reducción de ingresos y fidelización.

Este proyecto busca identificar clientes con probabilidad de abandono utilizando variables relacionadas con el comportamiento del cliente.

---

## Arquitectura de la solución

```text
Cliente
   │
   ▼
FastAPI
   │
   ├── Validación de datos
   ├── Detección de anomalías
   ├── Monitoreo de métricas
   ├── Logging
   │
   ▼
Modelo Machine Learning (.joblib)
   │
   ▼
Predicción de Churn
```

---

## Estructura del proyecto

```text
proyecto_churn_mlops
├── api
│   └── main.py
├── data
├── docs
├── logs
├── models
├── notebooks
├── src
├── tests
├── Dockerfile
├── requirements.txt
├── .dockerignore
└── README.md
```

---

## Funcionalidades implementadas

### Predicción de churn

La API recibe información del cliente y devuelve:

* Probabilidad de abandono.
* Clasificación de riesgo.
* Alertas por valores fuera del rango histórico.
* Información del modelo utilizado.

### Monitoreo básico

Se implementaron mecanismos de observabilidad:

* Registro de eventos en consola y archivo.
* Medición de latencia.
* Conteo de solicitudes.
* Conteo de errores de validación.
* Conteo de errores internos.
* Métricas acumuladas.
* Detección de posibles señales de drift.

### Logging

Los eventos son almacenados en:

```text
logs/monitor_api.log
```

---

## Endpoints disponibles

| Endpoint | Método | Descripción                   |
| -------- | ------ | ----------------------------- |
| /        | GET    | Información general de la API |
| /health  | GET    | Estado de salud del servicio  |
| /metrics | GET    | Métricas acumuladas           |
| /predict | POST   | Predicción de churn           |
| /docs    | GET    | Documentación Swagger         |

---

## Ejecución local

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la API:

```bash
uvicorn api.main:app --reload
```

Acceder a Swagger:

```text
http://localhost:8000/docs
```

---

## Ejecución con Docker

Construcción de la imagen:

```bash
docker build -t churn-api .
```

Ejecución del contenedor:

```bash
docker run -p 8000:8000 churn-api
```

Verificar funcionamiento:

```text
http://localhost:8000/health
```

---

## Monitoreo y observabilidad

Las métricas disponibles permiten realizar seguimiento de:

* Solicitudes procesadas.
* Errores HTTP.
* Latencia promedio.
* Latencia máxima.
* Predicciones válidas.
* Solicitudes con anomalías.
* Distribución de respuestas.

Estas métricas pueden consultarse mediante:

```text
GET /metrics
```

---

## Riesgo de Drift

La solución incorpora una verificación de valores fuera de los rangos históricos utilizados durante el entrenamiento.

Cuando una observación presenta características atípicas, la API genera alertas que permiten identificar posibles señales tempranas de Data Drift.

---

## Tecnologías utilizadas

* Python
* FastAPI
* Scikit-Learn
* Joblib
* Docker
* Uvicorn
* Pydantic

---

## Autor

Maria Yamile Calderón Cárdenas

Maestría en Ciencia de Datos e Inteligencia Artificial
