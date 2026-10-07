#!/usr/bin/env python3
"""
API para consultar datos de Alcanos de Colombia
Usa Playwright para manejar reCAPTCHA automaticamente
"""

import asyncio
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from playwright.async_api import async_playwright

app = Flask(__name__)
CORS(app)

BASE_URL = "https://pagosvirtuales.alcanosesp.com"

async def consultar_alcanos(codigo_usuario):
    """
    Consulta Alcanos usando Playwright para pasar reCAPTCHA v3.
    Intercepta la respuesta de list.php directamente de la red.
    """
    resultado = None
    error = None

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            locale='es-CO',
        )
        page = await context.new_page()

        # Capturar la respuesta de list.php directamente de la red
        respuesta_api = asyncio.get_event_loop().create_future()

        async def capturar_respuesta(response):
            if 'list.php' in response.url and not respuesta_api.done():
                try:
                    body = await response.json()
                    respuesta_api.set_result(body)
                except Exception as e:
                    respuesta_api.set_result({"raw": await response.text(), "parse_error": str(e)})

        page.on('response', capturar_respuesta)

        try:
            # 1. Cargar la pagina (esto inicializa reCAPTCHA)
            await page.goto(BASE_URL + '/', wait_until='networkidle', timeout=30000)

            # 2. Ingresar el codigo de usuario
            await page.fill('input[name="pf_numero"]', str(codigo_usuario))

            # 3. Hacer clic en Continuar (reCAPTCHA se ejecuta automaticamente)
            await page.click('button[type="submit"], button:has-text("CONTINUAR"), .btn-primary')

            # 4. Esperar la respuesta de list.php (max 15 segundos)
            resultado = await asyncio.wait_for(respuesta_api, timeout=15)

        except asyncio.TimeoutError:
            error = "Timeout: no se recibio respuesta de Alcanos"
        except Exception as e:
            error = str(e)
        finally:
            await browser.close()

    if error:
        return {"status": False, "error": error, "errors": [error]}
    return resultado

def run_async(coro):
    """Ejecutar corrutina async desde contexto sincrono"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# ============================================
# RUTAS API
# ============================================

@app.route('/api/consultar', methods=['POST', 'GET'])
def api_consultar():
    """GET /api/consultar?codigo=400727  o  POST con JSON {"codigo": "400727"}"""
    codigo = request.args.get('codigo')
    if not codigo and request.is_json:
        codigo = request.json.get('codigo')

    if not codigo:
        return jsonify({'status': False, 'error': 'Parametro "codigo" requerido', 'errors': ['Falta el codigo de usuario']}), 400

    resultado = run_async(consultar_alcanos(codigo))
    return jsonify(resultado)


@app.route('/api/factura/<codigo>', methods=['GET'])
def api_factura_por_codigo(codigo):
    """GET /api/factura/400727"""
    resultado = run_async(consultar_alcanos(codigo))
    return jsonify(resultado)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'Alcanos API'}), 200


if __name__ == '__main__':
    print("=" * 50)
    print("Alcanos API iniciada")
    print("=" * 50)
    print("  GET  http://localhost:5000/api/factura/400727")
    print("  GET  http://localhost:5000/api/consultar?codigo=400727")
    print("  GET  http://localhost:5000/health")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
