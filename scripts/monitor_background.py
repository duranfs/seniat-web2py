# -*- coding: utf-8 -*-
"""
Script de monitoreo en background para web2py.
Debe ejecutarse con:
python web2py.py -S seniat_python3 -M -R applications/seniat_python3/scripts/monitor_background.py
"""
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('monitor_background.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

try:
    from applications.seniat_python3.controllers.default import actualizar_y_mostrar_monitor_parallel
except ImportError:
    import importlib.util
    import os
    APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_path = os.path.join(APP_PATH, 'controllers', 'default.py')
    spec = importlib.util.spec_from_file_location('default', default_path)
    default_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(default_mod)
    actualizar_y_mostrar_monitor_parallel = default_mod.actualizar_y_mostrar_monitor_parallel

def main(loop=False, interval=120):
    """
    Ejecuta el monitoreo en background.
    :param loop: Si True, ejecuta en bucle cada 'interval' segundos.
    :param interval: Intervalo en segundos entre ejecuciones.
    """
    while True:
        logging.info("Iniciando monitoreo de rutinas en background...")
        try:
            resultado = actualizar_y_mostrar_monitor_parallel()
            logging.info(f"Monitoreo completado: {resultado['resumen']}")
        except Exception as e:
            logging.error(f"Error en monitoreo: {str(e)}")
        if not loop:
            break
        logging.info(f"Esperando {interval} segundos para la próxima ejecución...")
        time.sleep(interval)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Monitoreo de rutinas en background para web2py")
    parser.add_argument('--loop', action='store_true', help='Ejecutar en modo daemon (bucle infinito)')
    parser.add_argument('--interval', type=int, default=120, help='Intervalo en segundos entre ejecuciones (default: 120)')
    args = parser.parse_args()
    main(loop=args.loop, interval=args.interval)
