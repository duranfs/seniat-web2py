from gluon.scheduler import Scheduler

scheduler = Scheduler(db, dict(monitoreo=('oracle','ejecutar_monitoreo')))

# Programar la tarea para ejecutarse cada 4 horas (reducido de 1 hora)
if not db(db.scheduler_task.task_name == 'monitoreo').count():
    scheduler.queue_task(
        'ejecutar_monitoreo',
        period=14400,  # cada 4 horas (14400 segundos)
        timeout=600,   # 10 minutos máximo por ejecución
        repeats=0      # indefinidamente
    )