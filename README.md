# Plataforma de Data Analytics para Predicción de Demanda y Optimización de Inventarios

## 1. Visión General del Proyecto

Este proyecto implementa una **plataforma end-to-end de Data Engineering y Analytics** orientada a la **predicción de demanda en retail** y a la **optimización de inventarios**, utilizando buenas prácticas de la industria y herramientas open-source.

El objetivo es simular un entorno realista similar al que operan equipos de datos en empresas de retail, consumo masivo o logística, cubriendo desde la **ingesta de datos** hasta la **preparación para modelos de forecasting y visualización**.

---

## 2. Objetivo de Negocio

Predecir la demanda futura por **producto y tienda** a partir de datos históricos de ventas para:

* Reducir quiebres de stock
* Minimizar exceso de inventario
* Mejorar la planificación de compras
* Facilitar la toma de decisiones basada en datos

Los resultados del proyecto están pensados para ser consumidos mediante:

* APIs (FastAPI)
* Dashboards interactivos (Power BI)

---

## 3. Arquitectura General

La arquitectura sigue un enfoque modular y reproducible:

* **Datos simulados** versionados en Git (CSV)
* **Docker Compose** para orquestación local
* **PostgreSQL** como Data Warehouse
* **Apache Airflow** para orquestación de pipelines
* **Python** para simulación, ingesta y modelado

Todo el entorno se ejecuta **localmente**, sin dependencia de servicios cloud pagos.

---

## 4. Estructura del Proyecto

```text
plataforma-prediccion-demanda/
│
├── docker/
│   └── docker-compose.yml          # Infraestructura local (Airflow + PostgreSQL)
│
├── airflow/
│   ├── dags/                       # DAGs de Airflow (ingesta, transformaciones)
│   ├── logs/
│   └── plugins/
│
├── scripts/
│   └── generate_sales_data.py      # Generador de datos sintéticos de ventas
│
├── data/
│   └── raw/                        # Datos de ventas simulados (CSV)
│
├── README.md
└── .gitignore
```

---

## 5. Generación de Datos Sintéticos

Los datos de ventas son generados mediante un script en Python que simula un escenario realista de retail.

Características principales:

* Grano: **día – producto – tienda**
* Estacionalidad semanal y anual
* Tendencia temporal
* Promociones
* Ruido estadístico
* Días sin ventas
* Outliers (ventas atípicas)

Esto permite entrenar y evaluar modelos de forecasting en condiciones cercanas a la realidad.

---

## 6. Orquestación con Airflow

Apache Airflow se utiliza para orquestar el pipeline de ingesta de datos desde archivos CSV hacia PostgreSQL.

### Estado actual

- DAG de ingesta implementado y operativo
- DAG visible y cargado correctamente en la UI de Airflow
- Programación diaria (`@daily`)
- Ejecución de scripts Python mediante `BashOperator`
- Carga exitosa de datos en la tabla `sales` de PostgreSQL
- Verificación de datos mediante consultas SQL

### Flujo del DAG

1. Airflow detecta el DAG `load_sales_csv_to_postgres`
2. Se ejecuta un script Python que:
   - Lee archivos CSV de ventas
   - Inserta los registros en PostgreSQL
3. El pipeline queda listo para futuras extensiones (transformaciones, feature engineering)

Este enfoque permite desacoplar la ingesta de datos del procesamiento analítico y facilita la escalabilidad del proyecto.

## Control de Calidad de Datos

El pipeline de ingesta incluye validaciones automáticas de calidad de datos implementadas en Apache Airflow.

Antes de permitir que los datos sean utilizados para análisis o modelos de predicción, se verifican las siguientes reglas:

- Existencia de datos cargados (row count > 0)
- Ausencia de duplicados por clave natural (fecha, tienda, producto)
- Ventas no negativas
- Precios válidos (price > 0)

Si alguna de estas validaciones falla, el DAG se detiene automáticamente, garantizando la integridad del Data Warehouse.


---

## 7. Stack Tecnológico

* **Python** (pandas, numpy)
* **PostgreSQL**
* **Apache Airflow**
* **Docker & Docker Compose**
* **Git & GitHub**

---

## 8. Cómo levantar el entorno local

Requisitos:

* Docker
* Docker Compose

Pasos:

```bash
cd docker
docker compose up -d
```

Servicios disponibles:

* Airflow UI: [http://localhost:8080](http://localhost:8080)
* PostgreSQL: localhost:5432

---

## 9. Roadmap del Proyecto

* [x] Generación de datos sintéticos
* [x] Infraestructura dockerizada
* [x] Diseño del modelo de datos
* [x] DAG de ingesta en Airflow
* [ ] Transformaciones y feature engineering
* [ ] Modelos de predicción de demanda
* [ ] API de consumo (FastAPI)
* [ ] Dashboard ejecutivo

---

## 10. Autor

**Glem Ramos**
Proyecto desarrollado con fines de aprendizaje avanzado y portafolio profesional en Data Engineering y Data Analytics.
