"""
╔══════════════════════════════════════════════════════════════╗
║           CIFRADO DE HILL — Encriptación Matricial           ║
║         Basado en álgebra lineal sobre Z₂₆ (mod 26)          ║
╚══════════════════════════════════════════════════════════════╝

TEORÍA:
  El Cifrado de Hill usa una matriz clave K (nxn) invertible en Z₂₆.
  - Encriptar: C = K · P  (mod 26)
  - Desencriptar: P = K⁻¹ · C  (mod 26)
  donde K⁻¹ es la inversa modular de K en Z₂₆.

  Para que K sea invertible en Z₂₆, se requiere:
    gcd(det(K), 26) = 1

ALFABETO: A=0, B=1, ..., Z=25
"""

import numpy as np
from sympy import Matrix
import questionary
import string

# ─── Constantes ───────────────────────────────────────────────
# Usamos módulo 95 para tomar todos los carácteres imprimibles de string.printable
# Rango de 0-94
ALPHANUMERIC_CHARS = string.printable[:-5]
MOD = len(ALPHANUMERIC_CHARS)

# ─── Colores ANSI para terminal ───────────────────────────────────────────────
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLK = "\033[40m"
    BG_BLU = "\033[44m"


# ─── Matrices de clave predefinidas ────────────────────────────────────────────────────
PRESET_KEYS = {
    "1": {
        "name": "Clave 2x2 Simple",
        "matrix": np.array([[3, 3], [2, 5]]),
        "desc": "Clásica 2x2, fácil de visualizar",
    },
    "2": {
        "name": "Clave 2x2 Alternativa",
        "matrix": np.array([[6, 24], [1, 13]]),
        "desc": "Otro ejemplo 2x2 válido",
    },
    "3": {
        "name": "Clave 3x3 Estándar",
        "matrix": np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]]),
        "desc": "Mayor seguridad con bloques de 3",
    },
    # "4": {
    #     "name": "Clave 3x3 Compacta",
    #     "matrix": np.array([[1, 2, 3], [0, 1, 4], [5, 6, 0]]),
    #     "desc": "Estructura triangular modificada",
    # },
}


# ─── Utilerías matemáticas ────────────────────────────────────────────────────


def get_modular_inverse(key_matrix, modulo=MOD):
    # Convierte el arreglo de numpy a una Matrix de SymPy para exactitud aritmética
    sympy_matrix = Matrix(key_matrix)
    
    try:
        # Calcula la matriz inversa modulo m
        inverse_matrix = sympy_matrix.inv_mod(modulo)
    except ValueError:
        raise ValueError(f"The matrix is not invertible under modulo {modulo}.")
        
    return np.array(inverse_matrix).astype(int)


# ─── Funciones de texto ───────────────────────────────────────────────────────────
def pad_text(message, matrix_size) -> str:
    # Calcula cuántos carácteres se ocupan para rellenar la matriz cuadrada
    padding_length = matrix_size - (len(message) % matrix_size)

    # Se añaden espacios para rellenar la matriz
    if padding_length != matrix_size:
        message += " " * padding_length

    return message

def text_to_numbers(text: str) -> list[int]:
    clean_text = "".join([char for char in text if char in ALPHANUMERIC_CHARS])
    return [ALPHANUMERIC_CHARS.index(char) for char in clean_text]

def numbers_to_text(numeric_vectors):
    cipher_text = ""

    for vector in numeric_vectors:
        for number in vector:
            cipher_text += ALPHANUMERIC_CHARS[int(number)]
            
    return cipher_text

def prepare_cipher_matrix(cipher_text, block_size):
    """
    Convierte el texto cifrado a una matriz de vectores
    """
    numeric_values = [ord(char) for char in cipher_text]
    cipher_matrix = np.array(numeric_values).reshape(-1, block_size)
    return cipher_matrix

def clean_text(text: str) -> str:
    clean_text = "".join([char if char in ALPHANUMERIC_CHARS else "_" for char in text])
    return clean_text


def encrypt(plaintext: str, key_matrix: np.ndarray) -> str:
    """
    Encripta usando el Cifrado de Hill.
    C = K · P  (mod 95)
    Retorna (texto_cifrado)
    """

    plaintext = clean_text(plaintext)

    transformed_numbers = []

    n = key_matrix.shape[0]
    padded = pad_text(plaintext, n)
    numbers = text_to_numbers(padded)
    # Dividimos la lista de números en matrices bidimensionales
    reshaped_vectors = np.array(numbers).reshape(-1, n)

    for vector in reshaped_vectors:
        transformed_vector = (key_matrix @ vector )% MOD
        transformed_numbers.append(transformed_vector)

    cyphered_numbers = np.array(transformed_numbers)

    return numbers_to_text(cyphered_numbers)

def decrypt(cipher_text: str, key_matrix: np.ndarray) -> str:
    """
    Decrypts a message using the Hill Cipher.
    P = K^-1 @ C (mod m)
    Returns the decrypted plain text string.
    """
    # 1. Transforma el texto ingresado en una matriz cifrada
    block_size = key_matrix.shape[0]
    
    # A cada caracter le corresponde un indice en nuestro diccionario de caracteres disponibles
    numeric_values = [ALPHANUMERIC_CHARS.index(char) for char in cipher_text]
    
    cipher_matrix = np.array(numeric_values).reshape(-1, block_size)
    
    inverse_key_matrix = get_modular_inverse(key_matrix, MOD)
    
    decrypted_matrix = []
    
    for vector in cipher_matrix:
        # P_i = (K^-1 @ C_i) mod m
        decrypted_vector = (inverse_key_matrix @ vector) % MOD
        decrypted_matrix.append(decrypted_vector)
        
    decrypted_array = np.array(decrypted_matrix)
    
    plain_text = "" 
    
    # Volver a convertir el vector numerico a string
    for vector in decrypted_array:
        for number in vector:
            plain_text += ALPHANUMERIC_CHARS[int(number)]

    return plain_text

# ─── Visualización de consola ───────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║  ░█░█░▀█▀░█░░░█░░░░░█▀▀░▀█▀░█▀▀░█░█░█▀▀░█▀▄          ║
  ║  ░█▀█░░█░░█░░░█░░░░░█░░░░█░░█▀▀░█▀█░█▀▀░█▀▄          ║
  ║  ░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░░░▀░▀░▀▀▀░▀░▀ v1.0     ║
  ║           C I F R A D O   D E   H I L L              ║
  ║               Encriptación Matricial                 ║
  ╚══════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)


def print_matrix(matrix: np.ndarray, label: str = "", color: str = C.CYAN):
    """Imprime una matriz de forma visual."""
    n = matrix.shape[0]
    if label != "":
        print(f"\n  {color}{C.BOLD}{label}{C.RESET}")
    for i, row in enumerate(matrix):
        top = "  ┌" if i == 0 else ("  └" if i == n - 1 else "  │")
        bottom = "┐" if i == 0 else ("┘" if i == n - 1 else "│")
        vals = "  ".join(f"{color}{int(v):3d}{C.RESET}" for v in row)
        print(f"  {top}  {vals}  {bottom}")
    print()

def print_section(title: str, color: str = C.YELLOW):
    print(f"\n{color}{C.BOLD}  {'─'*52}")
    print(f"  {title}")
    print(f"  {'─'*52}{C.RESET}\n")


# ─── Menú principal ───────────────────────────────────────────────────────────


def main():
    print_banner()
    matrix = None


    print(f"  {C.CYAN}Claves predefinidas:{C.RESET}\n")
    for k, v in PRESET_KEYS.items():
        print(f"  {C.BOLD}[{k}]{C.RESET} {v['name']}")
        print(f"      {C.DIM}{v['desc']}{C.RESET}")
        print_matrix(v["matrix"], "", C.BLUE)

    choice = questionary.select(
        "Selecciona una matriz clave para encriptar",
        list(PRESET_KEYS)
    ).ask()

    if choice in PRESET_KEYS.keys():
        matrix = PRESET_KEYS[choice]["matrix"]

    print(f"{C.BOLD}{C.CYAN} Matriz seleccionada: {C.RESET}")
    print_matrix(matrix, color = C.BLUE)

    while True:

        choice = questionary.select(
            "Selecciona una opción:", 
            [
                "Encriptar texto", 
                "Desencriptar texto",
                "Salir"
            ]
        ).ask()

        if choice == "Encriptar texto":
            msg = questionary.text(
                f"Ingresa un texto a encriptar: ",
                style=questionary.Style([
                    ("question", "fg:#1ADBDB bold"),
                    ("answer", "fg:#FFFFFF bold")
                    ])
            ).ask()
            crypted_msg = encrypt(msg, matrix)

            print_section(f"Tu mensaje encriptado: {crypted_msg}", C.MAGENTA)

        if choice == "Desencriptar texto":
            msg = questionary.text(
                f"Ingresa un texto a desencriptar: ",
                style=questionary.Style([
                    ("question", "fg:#1ADBDB bold"),
                    ("answer", "fg:#FFFFFF bold")
                    ])
            ).ask()
            crypted_msg = decrypt(msg, matrix)

            print_section(f"Tu mensaje desencriptado: {crypted_msg}", C.GREEN)

        if choice == "Salir":
            print_section("Ciao! :)", C.CYAN)
            break


if __name__ == "__main__":
    main()
