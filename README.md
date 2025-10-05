# F5ProjectVI_ProblemaDeClasificacion
[gestión del proyecto](https://anthonycpcode.atlassian.net/jira/software/projects/AIR/code?atlOrigin=eyJpIjoiYjlhOTA5ZGNkZmUyNDVmZjk1MDFhMDNkNDJmNTM3NTYiLCJwIjoiaiJ9)
[Airline Passenger Satisfaction dataset in Kaggle](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction/data)

## Resumen

Este proyecto entrena un modelo de clasificación supervisada que predice la satisfacción de los pasajeros de una aerolínea (satisfecho vs. neutral o insatisfecho) utilizando un dataset público de Kaggle. El flujo de trabajo limpia los datos, codifica las variables categóricas y ajusta un pipeline de random forest balanceado que supera el 96 % de exactitud en la partición de entrenamiento.

## Columnas del conjunto de datos

El dataset de entrenamiento ubicado en `datasets/train.csv` contiene 103 904 filas con los siguientes campos:

- `Gender`, `Customer Type`, `Type of Travel`, `Class`: descriptores categóricos de cada pasajero.
- `Age`, `Flight Distance`, calificaciones de servicio (wifi, reserva, ubicación de la puerta, comida, embarque, comodidad del asiento, entretenimiento, servicio a bordo, espacio para las piernas, equipaje, check-in, servicio en vuelo, limpieza) y mediciones de retrasos: entradas numéricas en una escala de 0 a 5 o en minutos.
- `satisfaction`: etiqueta objetivo que indica `satisfied` o `neutral or dissatisfied`.

El script elimina automáticamente las columnas no predictivas `Unnamed: 0` e `id`, imputa los retrasos faltantes con la mediana y aplica codificación one-hot a los atributos categóricos.

## Configuración del entorno

Instala las dependencias listadas en `requirements.txt` (se recomienda un entorno virtual):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Entrenar el modelo

Ejecuta el pipeline de entrenamiento desde la raíz del repositorio:

```powershell
.venv\Scripts\python.exe src/train_model.py
```

Los argumentos opcionales permiten personalizar las rutas de los datos, el modelo y las métricas. Usa `--help` para ver todas las opciones.

## Ejecutar con Docker

Si prefieres aislar el entorno y evitar instalaciones locales, puedes usar la imagen Docker incluida:

```powershell
docker build -t airline-satisfaction .
docker run --rm -v ${PWD}\models:/app/models -v ${PWD}\reports:/app/reports airline-satisfaction
```

El montaje de volúmenes es opcional pero recomendable para conservar `models/` y `reports/` en el host. Crea las carpetas si aún no existen:

```powershell
New-Item -ItemType Directory -Force models
New-Item -ItemType Directory -Force reports
```

Puedes sobreescribir el comando por defecto agregando argumentos al final de `docker run`, por ejemplo `docker run --rm airline-satisfaction python src/train_model.py`.

## Resumen de evaluación

La configuración predeterminada divide los datos 80/20 (estratificada) y reporta las siguientes métricas sobre el conjunto de validación:

| Métrica     | Puntaje |
|-------------|---------|
| Exactitud   | 0.9635 |
| Precisión   | 0.9697 |
| Recall      | 0.9454 |
| F1-score    | 0.9574 |
| ROC AUC     | 0.9943 |

Las métricas de clasificación detalladas y la matriz de confusión se almacenan en `reports/metrics.json`.

## Resultados

- `models/satisfaction_model.joblib`: pipeline de scikit-learn serializado para inferencia.
- `reports/metrics.json`: archivo JSON con los resultados de evaluación (exactitud, precisión, recall, F1, ROC AUC, informe de clasificación, matriz de confusión).

## Próximos pasos

- Validar el modelo en un conjunto separado o en el split de prueba de Kaggle.
- Crear scripts de inferencia y monitoreo para puntuar nuevas encuestas de pasajeros en producción.
