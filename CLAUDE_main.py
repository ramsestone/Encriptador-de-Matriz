"""
╔══════════════════════════════════════════════════════════════╗
║           CIFRADO DE HILL — Encriptación Matricial           ║
║         Basado en álgebra lineal sobre Z₂₆ (mod 26)          ║
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


# ─── Utilerías matemáticas ────────────────────────────────────────────────────


def mod_inverse(a: int, m: int) -> int:
    """Inversa modular de `a` en Z_m usando algoritmo extendido de Euclides."""
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


def is_valid_key_matrix(matrix: np.ndarray, mod: int = 26) -> bool:
    """Verifica si la matriz puede usarse como clave Hill."""
    det = determinant_mod(matrix, mod)
    return gcd(det, mod) == 1


# ─── Procesamiento de texto ───────────────────────────────────────────────────


def text_to_numbers(text: str) -> list[int]:
    """Convierte texto (solo letras) a lista de números 0–25."""
    return [ord(c) - ord("A") for c in text.upper() if c.isalpha()]


def numbers_to_text(numbers: list[int]) -> str:
    """Convierte lista de números 0–25 a texto en mayúsculas."""
    return "".join(chr(n % 26 + ord("A")) for n in numbers)


def pad_text(numbers: list[int], block_size: int, pad_char: int = 23) -> list[int]:
    """Rellena con 'X' (23) hasta completar bloques de `block_size`."""
    while len(numbers) % block_size != 0:
        numbers.append(pad_char)
    return numbers


# ─── Cifrado y descifrado ─────────────────────────────────────────────────────


def encrypt(plaintext: str, key_matrix: np.ndarray) -> tuple[str, list]:
    """
    Encripta usando el Cifrado de Hill.
    C = K · P  (mod 26)
    Retorna (texto_cifrado, pasos_de_visualización)
    """
    n = key_matrix.shape[0]
    numbers = text_to_numbers(plaintext)
    padded = pad_text(numbers[:], n)

    steps = []
    ciphertext_nums = []

    for i in range(0, len(padded), n):
        block = np.array(padded[i : i + n])
        result = key_matrix @ block % 26
        steps.append(
            {
                "block_in": block.tolist(),
                "block_out": result.tolist(),
                "chars_in": numbers_to_text(block.tolist()),
                "chars_out": numbers_to_text(result.tolist()),
            }
        )
        ciphertext_nums.extend(result.tolist())

    return numbers_to_text(ciphertext_nums), steps


def decrypt(ciphertext: str, key_matrix: np.ndarray) -> tuple[str, list]:
    """
    Desencripta usando el Cifrado de Hill.
    P = K⁻¹ · C  (mod 26)
    """
    n = key_matrix.shape[0]
    key_inv = matrix_mod_inverse(key_matrix, 26)
    numbers = text_to_numbers(ciphertext)
    padded = pad_text(numbers[:], n)

    steps = []
    plaintext_nums = []

    for i in range(0, len(padded), n):
        block = np.array(padded[i : i + n])
        result = key_inv @ block % 26
        steps.append(
            {
                "block_in": block.tolist(),
                "block_out": result.tolist(),
                "chars_in": numbers_to_text(block.tolist()),
                "chars_out": numbers_to_text(result.tolist()),
            }
        )
        plaintext_nums.extend(result.tolist())

    return numbers_to_text(plaintext_nums), steps


# ─── Visualización en terminal ────────────────────────────────────────────────


def print_banner():
    banner = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════╗
  ║  ░█░█░▀█▀░█░░░█░░░░░█▀▀░▀█▀░█▀▀░█░█░█▀▀░█▀▄        ║
  ║  ░█▀█░░█░░█░░░█░░░░░█░░░░█░░█▀▀░█▀█░█▀▀░█▀▄        ║
  ║  ░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀░░░▀░▀░▀▀▀░▀░▀        ║
  ║           C I F R A D O   D E   H I L L             ║
  ║         Encriptación Matricial en Z₂₆               ║
  ╚══════════════════════════════════════════════════════╝{C.RESET}
"""
    print(banner)


def print_matrix(matrix: np.ndarray, label: str, color: str = C.CYAN):
    """Imprime una matriz de forma visual."""
    n = matrix.shape[0]
    print(f"\n  {color}{C.BOLD}{label}{C.RESET}")
    for i, row in enumerate(matrix):
        top = "  ┌" if i == 0 else ("  └" if i == n - 1 else "  │")
        bottom = "┐" if i == 0 else ("┘" if i == n - 1 else "│")
        vals = "  ".join(f"{color}{int(v):3d}{C.RESET}" for v in row)
        print(f"  {top}  {vals}  {bottom}")
    print()


def print_step(step: dict, idx: int, color: str):
    """Muestra un paso del cifrado/descifrado."""
    ci = numbers_to_text(step["block_in"])
    co = numbers_to_text(step["block_out"])
    ni = step["block_in"]
    no = step["block_out"]
    print(
        f"  {C.DIM}Bloque {idx+1}:{C.RESET}  "
        f"{color}{ci}{C.RESET} {C.DIM}({ni}){C.RESET}  →  "
        f"{C.WHITE}{C.BOLD}{co}{C.RESET} {C.DIM}({no}){C.RESET}"
    )


def print_section(title: str, color: str = C.YELLOW):
    print(f"\n{color}{C.BOLD}  {'─'*52}")
    print(f"  {title}")
    print(f"  {'─'*52}{C.RESET}\n")


# ─── Matrices de clave predefinidas ──────────────────────────────────────────

PRESET_KEYS = {
    "1": {
        "name": "Clave 2×2 Simple",
        "matrix": np.array([[3, 3], [2, 5]]),
        "desc": "Clásica 2×2, fácil de visualizar",
    },
    "2": {
        "name": "Clave 2×2 Alternativa",
        "matrix": np.array([[6, 24], [1, 13]]),
        "desc": "Otro ejemplo 2×2 válido",
    },
    "3": {
        "name": "Clave 3×3 Estándar",
        "matrix": np.array([[6, 24, 1], [13, 16, 10], [20, 17, 15]]),
        "desc": "Mayor seguridad con bloques de 3",
    },
    "4": {
        "name": "Clave 3×3 Compacta",
        "matrix": np.array([[1, 2, 3], [0, 1, 4], [5, 6, 0]]),
        "desc": "Estructura triangular modificada",
    },
}


def choose_key() -> np.ndarray:
    """Menú interactivo para seleccionar o ingresar una clave."""
    print_section("SELECCIÓN DE CLAVE MATRICIAL", C.MAGENTA)

    print(f"  {C.CYAN}Claves predefinidas:{C.RESET}\n")
    for k, v in PRESET_KEYS.items():
        print(f"  {C.BOLD}[{k}]{C.RESET} {v['name']}")
        print(f"      {C.DIM}{v['desc']}{C.RESET}")
        print_matrix(v["matrix"], "", C.BLUE)

    print(f"  {C.BOLD}[5]{C.RESET} Ingresar mi propia matriz 2×2")
    print(f"  {C.BOLD}[6]{C.RESET} Ingresar mi propia matriz 3×3\n")

    while True:
        choice = input(f"  {C.YELLOW}Elige opción (1-6): {C.RESET}").strip()

        if choice in PRESET_KEYS:
            return PRESET_KEYS[choice]["matrix"]

        elif choice == "5":
            print(
                f"\n  {C.DIM}Ingresa los 4 valores de tu matriz 2×2 (fila por fila):{C.RESET}"
            )
            try:
                vals = []
                for i in range(2):
                    row = input(
                        f"  Fila {i+1} (2 números separados por espacio): "
                    ).split()
                    vals.append([int(x) for x in row])
                matrix = np.array(vals)
                if is_valid_key_matrix(matrix):
                    print(f"  {C.GREEN}✓ Matriz válida.{C.RESET}")
                    return matrix
                else:
                    det = determinant_mod(matrix, 26)
                    print(
                        f"  {C.RED}✗ Matriz inválida. det={det}, gcd({det},26)={gcd(det,26)} ≠ 1{C.RESET}"
                    )
            except Exception as e:
                print(f"  {C.RED}Error: {e}{C.RESET}")

        elif choice == "6":
            print(
                f"\n  {C.DIM}Ingresa los 9 valores de tu matriz 3×3 (fila por fila):{C.RESET}"
            )
            try:
                vals = []
                for i in range(3):
                    row = input(
                        f"  Fila {i+1} (3 números separados por espacio): "
                    ).split()
                    vals.append([int(x) for x in row])
                matrix = np.array(vals)
                if is_valid_key_matrix(matrix):
                    print(f"  {C.GREEN}✓ Matriz válida.{C.RESET}")
                    return matrix
                else:
                    det = determinant_mod(matrix, 26)
                    print(
                        f"  {C.RED}✗ Matriz inválida. det={det}, gcd({det},26)={gcd(det,26)} ≠ 1{C.RESET}"
                    )
            except Exception as e:
                print(f"  {C.RED}Error: {e}{C.RESET}")
        else:
            print(f"  {C.RED}Opción no válida.{C.RESET}")


# ─── Menú principal ───────────────────────────────────────────────────────────


def demo_mode(key_matrix: np.ndarray):
    """Muestra un ejemplo completo encriptando y desencriptando."""
    demo_text = "HOLA"
    print_section("MODO DEMO", C.CYAN)
    print(f"  Texto de prueba: {C.BOLD}{demo_text}{C.RESET}\n")

    cipher, enc_steps = encrypt(demo_text, key_matrix)
    print(f"  {C.GREEN}▶ Encriptando:{C.RESET}")
    for i, s in enumerate(enc_steps):
        print_step(s, i, C.GREEN)

    print(f"\n  {C.YELLOW}Texto cifrado: {C.BOLD}{cipher}{C.RESET}")

    plain, dec_steps = decrypt(cipher, key_matrix)
    print(f"\n  {C.CYAN}▶ Desencriptando:{C.RESET}")
    for i, s in enumerate(dec_steps):
        print_step(s, i, C.CYAN)

    print(f"\n  {C.GREEN}Texto recuperado: {C.BOLD}{plain[:len(demo_text)]}{C.RESET}")


def main():
    print_banner()

    key_matrix = choose_key()
    n = key_matrix.shape[0]

    print_section("CLAVE SELECCIONADA", C.CYAN)
    print_matrix(key_matrix, "Matriz clave K:", C.CYAN)

    # Calcular y mostrar inversa
    try:
        key_inv = matrix_mod_inverse(key_matrix, 26)
        print_matrix(key_inv, "Matriz inversa K⁻¹ (mod 26):", C.MAGENTA)
        det = determinant_mod(key_matrix, 26)
        det_inv = mod_inverse(det, 26)
        print(f"  {C.DIM}det(K) = {det},  det(K)⁻¹ mod 26 = {det_inv}{C.RESET}")
    except ValueError as e:
        print(f"  {C.RED}Error: {e}{C.RESET}")
        return

    # Verificación de producto K · K⁻¹ = I
    identity_check = (key_matrix @ key_inv) % 26
    is_identity = np.allclose(identity_check, np.eye(n))
    check_str = (
        f"{C.GREEN}✓ K · K⁻¹ = I (mod 26){C.RESET}"
        if is_identity
        else f"{C.RED}✗ Error de verificación{C.RESET}"
    )
    print(f"\n  {check_str}")

    while True:
        print_section("MENÚ PRINCIPAL", C.YELLOW)
        print(f"  {C.BOLD}[1]{C.RESET} Encriptar texto")
        print(f"  {C.BOLD}[2]{C.RESET} Desencriptar texto")
        print(f"  {C.BOLD}[3]{C.RESET} Encriptar + Desencriptar (verificación)")
        print(f"  {C.BOLD}[4]{C.RESET} Demo automático")
        print(f"  {C.BOLD}[5]{C.RESET} Cambiar clave")
        print(f"  {C.BOLD}[6]{C.RESET} Mostrar teoría matemática")
        print(f"  {C.BOLD}[0]{C.RESET} Salir\n")

        opt = input(f"  {C.YELLOW}Opción: {C.RESET}").strip()

        if opt == "0":
            print(f"\n  {C.DIM}¡Hasta luego! Matriz y datos descartados.{C.RESET}\n")
            break

        elif opt == "1":
            text = input(f"\n  {C.GREEN}Texto a encriptar: {C.RESET}").strip()
            if not text:
                continue
            clean = "".join(c for c in text.upper() if c.isalpha())
            if not clean:
                print(f"  {C.RED}Sin letras válidas.{C.RESET}")
                continue
            cipher, steps = encrypt(clean, key_matrix)
            print(f"\n  {C.GREEN}▶ Pasos de encriptación (bloques de {n}):{C.RESET}")
            for i, s in enumerate(steps):
                print_step(s, i, C.GREEN)
            print(f"\n  {C.WHITE}{C.BOLD}  Texto cifrado: {cipher}{C.RESET}\n")

        elif opt == "2":
            text = input(f"\n  {C.CYAN}Texto a desencriptar: {C.RESET}").strip()
            if not text:
                continue
            clean = "".join(c for c in text.upper() if c.isalpha())
            if not clean:
                print(f"  {C.RED}Sin letras válidas.{C.RESET}")
                continue
            try:
                plain, steps = decrypt(clean, key_matrix)
                print(
                    f"\n  {C.CYAN}▶ Pasos de desencriptación (bloques de {n}):{C.RESET}"
                )
                for i, s in enumerate(steps):
                    print_step(s, i, C.CYAN)
                print(f"\n  {C.WHITE}{C.BOLD}  Texto descifrado: {plain}{C.RESET}\n")
            except ValueError as e:
                print(f"  {C.RED}Error: {e}{C.RESET}")

        elif opt == "3":
            text = input(f"\n  {C.GREEN}Texto original: {C.RESET}").strip()
            if not text:
                continue
            clean = "".join(c for c in text.upper() if c.isalpha())
            cipher, _ = encrypt(clean, key_matrix)
            recovered, _ = decrypt(cipher, key_matrix)
            print(f"\n  Original  : {C.BOLD}{clean}{C.RESET}")
            print(f"  Cifrado   : {C.YELLOW}{C.BOLD}{cipher}{C.RESET}")
            print(f"  Recuperado: {C.GREEN}{C.BOLD}{recovered[:len(clean)]}{C.RESET}")
            match = clean == recovered[: len(clean)]
            print(
                f"  {'  ✓ Verificación exitosa' if match else '  ✗ Error de verificación'}",
                f"{C.GREEN if match else C.RED}{C.RESET}\n",
            )

        elif opt == "4":
            demo_mode(key_matrix)

        elif opt == "5":
            key_matrix = choose_key()
            n = key_matrix.shape[0]
            print_matrix(key_matrix, "Nueva clave K:", C.CYAN)
            try:
                key_inv = matrix_mod_inverse(key_matrix, 26)
                print_matrix(key_inv, "Inversa K⁻¹ (mod 26):", C.MAGENTA)
            except ValueError as e:
                print(f"  {C.RED}{e}{C.RESET}")

        elif opt == "6":
            print_section("TEORÍA DEL CIFRADO DE HILL", C.BLUE)
            theory = f"""
  {C.BOLD}¿Qué es el Cifrado de Hill?{C.RESET}
  ──────────────────────────
  Propuesto por Lester Hill en 1929. Es un criptosistema de
  sustitución polialfabética basado en álgebra lineal.

  {C.BOLD}Representación del alfabeto:{C.RESET}
  A=0  B=1  C=2  D=3  E=4  F=5  G=6  H=7  I=8  J=9
  K=10 L=11 M=12 N=13 O=14 P=15 Q=16 R=17 S=18 T=19
  U=20 V=21 W=22 X=23 Y=24 Z=25

  {C.BOLD}Encriptación:{C.RESET}
  {C.CYAN}C = K · P  (mod 26){C.RESET}
  Donde:
    K = matriz clave n×n invertible en Z₂₆
    P = vector de texto plano (n letras → n números)
    C = vector de texto cifrado

  {C.BOLD}Desencriptación:{C.RESET}
  {C.MAGENTA}P = K⁻¹ · C  (mod 26){C.RESET}
  Donde:
    K⁻¹ = inversa modular de K en Z₂₆

  {C.BOLD}Inversa Modular de la Matriz:{C.RESET}
  {C.YELLOW}K⁻¹ = det(K)⁻¹ · adj(K)  (mod 26){C.RESET}
  Condición: gcd(det(K), 26) = 1

  {C.BOLD}Ejemplo con K = [[3,3],[2,5]]:{C.RESET}
    det(K) = 3·5 - 3·2 = 9
    det⁻¹ mod 26 = 3  (porque 9·3 = 27 ≡ 1 mod 26)
    K⁻¹ = 3 · [[5,-3],[-2,3]] mod 26 = [[15,17],[20,9]]

  {C.BOLD}Seguridad:{C.RESET}
  Con matrices n×n el espacio de claves crece exponencialmente.
  Un bloque de n letras se transforma simultáneamente, haciendo
  inútil el análisis de frecuencia de monogramas.
"""
            print(theory)

        else:
            print(f"  {C.RED}Opción no válida.{C.RESET}")


if __name__ == "__main__":
    main()
