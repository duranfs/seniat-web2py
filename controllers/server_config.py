def server_config():
    import threading
    rocket_threads = [t for t in threading.enumerate() if 'Rocket' in t.name]
    return dict(
        max_threads=len(rocket_threads),
        thread_names=[t.name for t in rocket_threads]
    )