@echo off
setlocal
title MatrixCypher Build Tool (Auto-VENV)

:: --- Configuración ---
set VENV_PATH=.venv
set SCRIPT_NAME=main.py
set EXE_NAME=MatrixCypher
set ICON_NAME=MatrixCypher.ico
set REQS_FILE=requirements.txt

echo ====================================================
echo   Herramienta de Construcción: %EXE_NAME%
echo ====================================================

:: 1. Verificar si existe el entorno virtual, si no, crearlo
if not exist %VENV_PATH%\Scripts\activate (
    echo [INFO] No se encontro el entorno virtual. Creando %VENV_PATH%...
    python -m venv %VENV_PATH%
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo crear el entorno virtual. Asegurate de tener Python instalado.
        pause
        exit /b
    )
    
    echo [INFO] Entorno creado. Activando para instalar dependencias...
    call %VENV_PATH%\Scripts\activate
    
    echo [INFO] Actualizando pip...
    python -m pip install --upgrade pip
    
    if exist %REQS_FILE% (
        echo [INFO] Instalando requerimientos desde %REQS_FILE%...
        pip install -r %REQS_FILE%
    ) else (
        echo [ADVERTENCIA] No se encontro %REQS_FILE%. Instalando dependencias base...
        pip install numpy sympy questionary pyinstaller
    )
) else (
    echo [INFO] Activando entorno virtual existente...
    call %VENV_PATH%\Scripts\activate
)

:: 2. Asegurar que PyInstaller este presente
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller no detectado. Instalando...
    pip install pyinstaller
)

:: 3. Ejecutar PyInstaller
echo [INFO] Compilando %SCRIPT_NAME%...
:: Nota: No usamos --windowed porque questionary requiere una terminal activa.
pyinstaller --onefile ^
    --name "%EXE_NAME%" ^
    --icon "%ICON_NAME%" ^
    "%SCRIPT_NAME%"

if %errorlevel% equ 0 (
    echo.
    echo ====================================================
    echo   EXITO: Ejecutable creado en la carpeta \dist
    echo ====================================================
) else (
    echo.
    echo [ERROR] Hubo un fallo en la compilacion.
)

:: 4. Desactivar y finalizar
call deactivate
pause