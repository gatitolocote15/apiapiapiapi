# 📡 Archivos para Deploy de alcanos_api.py en Render

## 📋 Contenido

Este carpeta contiene todos los archivos necesarios para deployar la API de búsqueda de facturas en Render:

```
archivos_para_api_render/
├── Procfile .................. Configuración para Render
├── requirements.txt .......... Dependencias Python
├── runtime.txt ............... Versión de Python (3.11.0)
└── .env ...................... Variables de entorno
```

## 🚀 Cómo Usarlos

### Paso 1: Subir a GitHub

1. Ve a tu repositorio: https://github.com/gatitolocote15/corspros
2. Sube estos 4 archivos a la raíz del repositorio (NO en una carpeta)
3. También sube `alcanos_api.py` (ya debe estar)

**Estructura en GitHub:**
```
corspros/
├── alcanos_api.py
├── Procfile
├── requirements.txt
├── runtime.txt
├── .env
└── [otros archivos]
```

### Paso 2: Crear Nuevo Servicio en Render

1. Ve a https://render.com
2. Dashboard → **New → Web Service**
3. Conectar GitHub
4. Seleccionar repo: `corspros`
5. Configurar:
   - **Name:** `alcanos-api-python`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python alcanos_api.py`
   - **Port:** 5000

### Paso 3: Variables de Entorno en Render

En el servicio, ve a **Environment** y agrega:
```
FLASK_ENV=production
```

### Paso 4: Deploy

Render automáticamente despliega cuando hagas push a GitHub.

## ✅ Verificar que Funciona

Una vez deployed, accede a:
```
https://alcanos-api-python.onrender.com/health
```

Debe responder:
```json
{
  "status": "ok",
  "timestamp": "...",
  "uptime": ...
}
```

## 📌 URLs Finales

```
Backend (Node.js):     https://minimals.onrender.com
Facturas (Python):     https://alcanos-api-python.onrender.com
Frontend (Azure):      https://tu-app.azurewebsites.net
```

## 🔗 Actualizar en Frontend

En `index.html` o `index2.html`, cambiar:
```javascript
// ANTES:
const API_URL = 'http://localhost:5000';

// DESPUÉS:
const API_URL = 'https://alcanos-api-python.onrender.com';
```

---

**¡Listo para subir a Render!** 🚀
