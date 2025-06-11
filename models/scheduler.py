from gluon.scheduler import Scheduler

scheduler = Scheduler(db, dict(monitoreo=('oracle','ejecutar_monitoreo')))

# Programar la tarea para ejecutarse cada hora
if not db(db.scheduler_task.task_name == 'monitoreo').count():
    scheduler.queue_task(
        'ejecutar_monitoreo',
        period=3600,  # cada hora
        timeout=300,  # 5 minutos máximo por ejecución
        repeats=0     # indefinidamente
    )