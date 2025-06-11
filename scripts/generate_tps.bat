@echo off
SET WEB2PY_PATH=C:\web2py
SET PYTHON_EXE=python
SET APP_NAME=bdvinv_python3

cd %WEB2PY_PATH%
%PYTHON_EXE% web2py.py -S %APP_NAME% -M -R applications\%APP_NAME%\scripts\generate_tps_task.py