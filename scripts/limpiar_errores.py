import os

errors_dir = r'c:\web2py_312\applications\seniat_web2py\errors'

for filename in os.listdir(errors_dir):
    file_path = os.path.join(errors_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f'Eliminado: {file_path}')

print('Limpieza de archivos de errores completada.')