#!/usr/bin/env python3
"""
API simplificada para consultar datos de facturas
Versión sin Playwright - compatible con Render Free
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============================================================
# DATOS MOCKEADOS (Para testing)
# En producción, aquí irían consultas a la BD
# ============================================================
MOCK_DATA = {
    "400727": {
        "status": True,
        "data": {
            "nombre": "JUAN CARLOS PEREZ GARCIA",
            "codigo": "12345",
            "numeroFactura": "400727",
            "fechaEmision": "2026-10-05",
            "fechaVencimiento": "2026-11-05",
            "valorFactura": 500000,
            "detalleSaldo": [
                {"subtotal": 250000}
            ]
        },
        "LastLogin": "2026-10-07T06:00:00"
    },
    "400728": {
        "status": True,
        "data": {
            "nombre": "MARIA GONZALEZ RODRIGUEZ",
            "codigo": "12346",
            "numeroFactura": "400728",
            "fechaEmision": "2026-10-06",
            "fechaVencimiento": "2026-11-06",
            "valorFactura": 750000,
            "detalleSaldo": [
                {"subtotal": 0}
            ]
        },
        "LastLogin": "2026-10-07T05:30:00"
    }
}

# ============================================================
# ENDPOINTS
# ============================================================

@app.get('/health')
def health():
    """Healthcheck endpoint"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "API funcionando"
    })

@app.get('/api/factura/<codigo>')
def get_factura(codigo):
    """
    Obtener información de una factura

    Args:
        codigo: Número de factura (ej: 400727)

    Returns:
        JSON con datos de la factura o error
    """
    codigo = str(codigo).strip()

    print(f"[GET /api/factura] Consultando código: {codigo}")

    # Buscar en datos mockeados
    if codigo in MOCK_DATA:
        return jsonify(MOCK_DATA[codigo])

    # Si no encuentra, devolver error
    return jsonify({
        "status": False,
        "error": f"Factura {codigo} no encontrada",
        "data": None
    }), 404

@app.post('/api/factura')
def post_factura():
    """Endpoint POST alternativo"""
    data = request.get_json()
    codigo = data.get('codigo', '').strip()

    if codigo in MOCK_DATA:
        return jsonify(MOCK_DATA[codigo])

    return jsonify({
        "status": False,
        "error": "Factura no encontrada",
        "data": None
    }), 404

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": False,
        "error": "Endpoint no encontrado"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "status": False,
        "error": "Error interno del servidor"
    }), 500

# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    print(f"""
╔════════════════════════════════════════════╗
║  🚀 API FACTURAS SIMPLIFICADA - ONLINE    ║
╚════════════════════════════════════════════╝

Puerto: {PORT}
Endpoints:
  ✓ GET  /health
  ✓ GET  /api/factura/<codigo>
  ✓ POST /api/factura

Modo: MOCK DATA (testing)

Para producción, integrar con BD real.
    """)
    app.run(host='0.0.0.0', port=PORT, debug=False)
