# 🔐 MatrixCypher — Cifrado de Hill

Un motor de encriptación matricial desarrollado en **Python** que utiliza álgebra lineal sobre el cuerpo de los enteros módulo $n$ ($Z_n$). Este proyecto permite cifrar y descifrar mensajes utilizando matrices de $2 \times 2$ y $3 \times 3$ con un alfabeto extendido de 95 caracteres.

## 🚀 Características

* **Matemáticas Exactas:** Uso de `SymPy` para el cálculo de la inversa modular, evitando errores de precisión de punto flotante.
* **Alfabeto Robusto:** Soporta hasta 95 caracteres (letras, números, símbolos y espacios) gracias al uso de `string.printable`.
* **Interfaz Profesional:** Experiencia de usuario en terminal mediante menús interactivos con `Questionary`.
* **Automatización:** Incluye un script de construcción (`build_exe.bat`) que gestiona el entorno virtual e instala dependencias automáticamente.

## 🛠️ Requisitos del Sistema

* **Python 3.8+**
* **Bibliotecas necesarias:**
    * `numpy`: Para operaciones de álgebra lineal.
    * `sympy`: Para el cálculo simbólico de la inversa modular.
    * `questionary`: Para la interfaz de usuario.

## 📦 Instalación y Uso

### Opción 1: Ejecución desde el código fuente
1. Clona el repositorio o descarga los archivos.
2. Crea un entorno virtual: `python -m venv .venv`
3. Activa el entorno e instala las dependencias:
   ```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
5. Ejecuta el programa
   ```bash
   python main.py
### Opción 2: Compilación automática (Windows)
Si deseas generar el archivo ejecutable .exe de forma automática:

Haz doble clic en el archivo build_exe.bat.

El script creará el entorno virtual, instalará las dependencias y generará el ejecutable en la carpeta dist/.
