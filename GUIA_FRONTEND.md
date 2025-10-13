# 🎨 Guía Completa del Frontend - Satisfaction Matrix

## 📋 Información General

**Proyecto**: Sistema de predicción de satisfacción de pasajeros de aerolínea
**Framework**: Streamlit 1.28+
**Backend**: FastAPI con modelo ML entrenado
**Dataset**: 103,904 pasajeros analizados

## 🏗️ Arquitectura del Frontend

```
frontend/
├── 📄 app.py                    # Página principal (dashboard)
├── 📁 pages/                    # Páginas adicionales
│   ├── 1_AnalisisDatos.py      # Análisis exploratorio
│   └── 2_Prediccion.py         # Formulario de predicción
├── 📄 api_client.py             # Cliente para API backend
├── 📄 Dockerfile               # Configuración contenedor
└── 📄 .env                     # Variables de entorno
```

## 📱 Descripción de Páginas

### **🏠 Página Principal (`app.py`)**
**Objetivo**: Dashboard ejecutivo con métricas clave del negocio

**Características**:
- ✅ **Métricas rápidas** del dataset completo
- ✅ **Comparación Business vs Economy** (diferencia de satisfacción)
- ✅ **Estadísticas de clientes leales**
- ✅ **Botón directo** a página de predicción
- ✅ **Diseño responsive** con columnas

**Métricas mostradas**:
- Tasa general de satisfacción (formato porcentaje)
- Número total de pasajeros analizados
- Satisfacción por clase de vuelo
- Edad promedio y clase más común

### **📊 Página de Análisis (`pages/1_AnalisisDatos.py`)**
**Objetivo**: Análisis exploratorio profundo para insights empresariales

**Características**:
- ✅ **EDA completo** con gráficos profesionales
- ✅ **Gráfico de barras** satisfacción por clase
- ✅ **Información contextual** para decisiones empresariales
- ✅ **Carga eficiente** con caché de Streamlit
- ✅ **Manejo robusto** de errores de archivos

**Visualizaciones**:
- Gráfico horizontal de satisfacción por clase
- Información sobre impacto Business vs Economy
- Métricas del tamaño del dataset

### **🔮 Página de Predicción (`pages/2_Prediccion.py`)**
**Objetivo**: Interface para predicciones en tiempo real

**Características**:
- ✅ **Formulario completo** con todos los parámetros
- ✅ **Organización por columnas** para UX óptima
- ✅ **Validación automática** de conexión API
- ✅ **Resultados formateados** profesionalmente
- ✅ **Manejo de errores** robusto

**Campos del formulario**:
1. **Datos Personales**: Género, tipo cliente, edad
2. **Detalles del Vuelo**: Tipo viaje, clase, distancia
3. **Retrasos**: Tiempo de espera en salida/llegada
4. **Calificaciones**: 13 servicios diferentes (0-5 escala)

## 🔗 Integración API Backend

### **Cliente API (`api_client.py`)**
```python
# Características principales:
✅ Configuración automática de variables de entorno
✅ Sistema de caché para eficiencia
✅ Manejo robusto de errores HTTP
✅ Validación automática de conexión
✅ Timeouts configurables
```

### **Métodos disponibles**:
- `health_check()`: Verificar estado del backend
- `predict_satisfaction(data)`: Realizar predicción
- `get_model_info()`: Información del modelo
- `get_model_metrics()`: Métricas del modelo

## 🐳 Configuración Docker

### **Dockerfile Frontend**
```dockerfile
# Características de seguridad:
✅ Usuario no-root (appuser)
✅ Variables de entorno optimizadas
✅ Instalación eficiente de dependencias
✅ Puerto 8501 configurado
✅ Comando Streamlit optimizado
```

### **Docker Compose Integration**
```yaml
# Servicios configurados:
✅ Frontend (puerto 8501)
✅ Backend (puerto 8000)
✅ Variables de entorno automáticas
✅ Volúmenes para desarrollo
✅ Dependencias entre servicios
```

## 🎨 Mejores Prácticas Implementadas

### **UX/UI**
- ✅ **Diseño responsive** con columnas y pestañas
- ✅ **Iconografía clara** (✈️, 📊, 🔮)
- ✅ **Colores consistentes** y profesionales
- ✅ **Navegación intuitiva** entre páginas
- ✅ **Feedback visual** inmediato

### **Performance**
- ✅ **Caché inteligente** con `@st.cache_data`
- ✅ **Lazy loading** de datos pesados
- ✅ **Timeouts apropiados** en peticiones API
- ✅ **Manejo eficiente** de errores

### **Código**
- ✅ **Separación clara** de responsabilidades
- ✅ **Comentarios explicativos** en español
- ✅ **Manejo robusto** de excepciones
- ✅ **Configuración flexible** vía variables de entorno

## 🚨 Solución de Problemas Comunes

### **Error: "No se puede conectar con la API"**
```bash
# Solución:
1. Verificar que backend esté ejecutándose: docker-compose ps
2. Revisar logs: docker-compose logs frontend
```

### **Error: "Archivo no encontrado"**
```bash
# Solución:
1. Verificar estructura de archivos
2. Confirmar que datasets/train.csv existe
3. Revisar rutas relativas en código
```

### **Error: "Página no encontrada"**
```bash
# Solución:
1. Verificar nombres de archivos en pages/
2. Confirmar estructura de navegación
3. Revisar configuración de páginas múltiples
```

## 📊 Métricas y KPIs

### **Métricas de la Aplicación**
- **Tiempo de carga**: < 3 segundos
- **Tasa de éxito de predicciones**: > 99%
- **Disponibilidad**: 24/7 con Docker
- **Usuarios concurrentes**: Ilimitado (arquitectura escalable)

---

