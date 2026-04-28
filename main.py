"""
╔══════════════════════════════════════════════════════════════╗
║           CIFRADO DE HILL — Encriptación Matricial           ║
║         Basado en álgebra lineal sobre Z₂₆ (mod 26)         ║
╚══════════════════════════════════════════════════════════════╝

TEORÍA:
  El Cifrado de Hill usa una matriz clave K (n×n) invertible en Z₂₆.
  - Encriptar: C = K · P  (mod 26)
  - Desencriptar: P = K⁻¹ · C  (mod 26)
  donde K⁻¹ es la inversa modular de K en Z₂₆.

  Para que K sea invertible en Z₂₆, se requiere:
    gcd(det(K), 26) = 1

ALFABETO: A=0, B=1, ..., Z=25
"""

import numpy as np
from math import gcd
import questionary


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
    # "3": {
    #     "name": "Clave 3x3 Estándar",
    #     "matrix": np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]]),
    #     "desc": "Mayor seguridad con bloques de 3",
    # },
    # "4": {
    #     "name": "Clave 3x3 Compacta",
    #     "matrix": np.array([[1, 2, 3], [0, 1, 4], [5, 6, 0]]),
    #     "desc": "Estructura triangular modificada",
    # },
}


# ─── Utilerías matemáticas ────────────────────────────────────────────────────


def mod_inverse(a: int, m: int) -> int:
    """Inversa modular de 'a' en Z_m usando algoritmo extendido de Euclides."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No existe inversa modular de {a} en Z_{m}")


def determinant_mod(matrix: np.ndarray, mod: int) -> int:
    """Determinante de una matriz entera, reducido módulo `mod`."""
    det = int(round(np.linalg.det(matrix)))
    return det % mod


def matrix_mod_inverse(matrix: np.ndarray, mod: int) -> np.ndarray:
    """
    Inversa modular de una matriz cuadrada en Z_mod.
    Usa la fórmula: K⁻¹ = det(K)⁻¹ · adj(K)  (mod m)
    donde adj(K) es la matriz adjunta (transpuesta de la cofactora).
    """
    n = matrix.shape[0]
    det = determinant_mod(matrix, mod)

    if gcd(det, mod) != 1:
        raise ValueError(
            f"La matriz NO es invertible en Z_{mod}.\n"
            f"  det(K) = {det},  gcd({det}, {mod}) = {gcd(det, mod)} ≠ 1"
        )

    det_inv = mod_inverse(det, mod)

    # Matriz adjunta mediante cofactores
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            # Minor: eliminar fila i, columna j
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            cofactor = int(round(np.linalg.det(minor))) * ((-1) ** (i + j))
            adj[j][i] = cofactor  # Transpuesta de cofactores

    return (det_inv * adj) % mod


# ─── Funciones generales ───────────────────────────────────────────────────────────
def pad_message(message, matrix_size):
    # Calcula cuántos carácteres se ocupan para rellenar la matriz cuadrada
    padding_length = matrix_size - (len(message) % matrix_size)

    # Se añaden espacios para rellenar la matriz
    if padding_length != matrix_size:
        message += " " * padding_length

    return message


def text_to_numbers(text: str) -> list[int]:
    """Convierte texto a lista de números 0–256."""
    return [ord(c) for c in text.upper()]


def encrypt(msg: str, matrix: np.ndarray):
    """
    Encripta usando el Cifrado de Hill.
    C = K · P  (mod 226)
    Retorna (texto_cifrado, pasos_de_visualización)
    """
    matrix_size = matrix.shape[0]

    pass


# ─── Visualización de consola ───────────────────────────────────────────────────────────
def print_banner():
    banner = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║  ░█░█░▀█▀░█░░░█░░░░░█▀▀░▀█▀░█▀▀░█░█░█▀▀░█▀▄          ║
  ║  ░█▀█░░█░░█░░░█░░░░░█░░░░█░░█▀▀░█▀█░█▀▀░█▀▄          ║
  ║  ░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░░░▀░▀░▀▀▀░▀░▀          ║
  ║           C I F R A D O   D E   H I L L              ║
  ║         Encriptación Matricial en Z₂₅₆               ║
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
        [
            "1",
            "2"
        ]
    ).ask()

    if choice == "1":
        matrix = PRESET_KEYS["1"]["matrix"]
    elif choice == "2":
        matrix = PRESET_KEYS["2"]["matrix"]
    print(f"{C.BOLD}{C.CYAN} Matriz seleccionada: {C.RESET}")
    print_matrix(matrix, color = C.BLUE)


    choice = questionary.select(
        "Selecciona una opción:", 
        [
            "Encriptar texto", 
            "Desencriptar texto"
        ]
    ).ask()

    if choice == "Encriptar texto":
        msg = input(f"{C.BOLD}Ingresa un texto a encriptar: {C.RESET}")
        encrypt(msg, matrix)


if __name__ == "__main__":
    main()
