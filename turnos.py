"""
MÓDULO 2: GESTIÓN DE TURNOS
Responsable: [Nombre del Estudiante B]

Este módulo se encarga de:
- Asignar turnos a pacientes
- Cancelar turnos existentes
- Buscar turnos por paciente
- Validar fechas y disponibilidad
"""

import json
import os
import shutil
from datetime import datetime


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system("cls" if os.name == "nt" else "clear")


def centrar_texto(texto):
    """Centra el texto en la pantalla"""
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:
        ancho_terminal = 80

    if len(texto) >= ancho_terminal:
        return texto

    espacios = (ancho_terminal - len(texto)) // 2
    return " " * espacios + texto


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter"""
    input(centrar_texto("Presione Enter para continuar..."))


def cargar_turnos():
    """Carga los datos de turnos desde el archivo JSON"""
    try:
        if os.path.exists("data/turnos.json"):
            with open("data/turnos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(centrar_texto(f"Error al cargar turnos: {e}"))
        return {}


def guardar_turnos(turnos):
    """Guarda los datos de turnos en el archivo JSON"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/turnos.json", "w", encoding="utf-8") as f:
            json.dump(turnos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(centrar_texto(f"Error al guardar turnos: {e}"))
        return False


def validar_fecha(dia, mes, anio):
    """Valida que la fecha sea válida y futura"""
    try:
        fecha = datetime(int(anio), int(mes), int(dia))
        hoy = datetime.now().date()
        if fecha.date() < hoy:
            return False, "La fecha no puede ser anterior a hoy"
        return True, ""
    except ValueError:
        return False, "Fecha inválida"


def obtener_turnos_disponibles(fecha_str):
    """Obtiene los turnos disponibles para una fecha específica"""
    turnos = cargar_turnos()
    turnos_disponibles = []

    for id_turno, turno in turnos.items():
        if turno.get("fecha") == fecha_str and turno.get("dni_paciente") == "":
            turnos_disponibles.append((id_turno, turno))

    return sorted(turnos_disponibles, key=lambda x: x[1].get("horario", ""))


def obtener_turnos_paciente(dni):
    """Obtiene todos los turnos de un paciente específico"""
    turnos = cargar_turnos()
    turnos_paciente = []

    for id_turno, turno in turnos.items():
        if turno.get("dni_paciente") == dni:
            turnos_paciente.append((id_turno, turno))

    return sorted(
        turnos_paciente, key=lambda x: (x[1].get("fecha", ""), x[1].get("horario", ""))
    )


def verificar_turnos_paciente(dni):
    """Verifica si un paciente tiene turnos asignados"""
    turnos_paciente = obtener_turnos_paciente(dni)
    return len(turnos_paciente) > 0


def asignar_turno():
    """Asigna un nuevo turno a un paciente"""
    limpiar_pantalla()
    print(centrar_texto("=== ASIGNAR TURNO ==="))
    print()

    # Solicitar DNI del paciente
    dni = input(centrar_texto("Ingrese DNI del paciente (0 para volver): ")).strip()
    if dni == "0":
        return

    # Verificar si el paciente existe
    from pacientes import obtener_paciente

    paciente = obtener_paciente(dni)

    if not paciente:
        print(centrar_texto("❌ No existe un paciente con ese DNI"))
        pausar()
        return

    print(centrar_texto(f"Paciente: {paciente['nombre']} {paciente['apellido']}"))
    print()

    # Solicitar fecha del turno
    print(centrar_texto("Ingrese la fecha del turno:"))
    try:
        dia_input = input(centrar_texto("Día (1-31) o 0 para volver: ")).strip()
        if dia_input == "0":
            return
        dia = int(dia_input)

        mes_input = input(centrar_texto("Mes (1-12) o 0 para volver: ")).strip()
        if mes_input == "0":
            return
        mes = int(mes_input)

        anio_input = input(centrar_texto("Año o 0 para volver: ")).strip()
        if anio_input == "0":
            return
        anio = int(anio_input)

        valida, mensaje = validar_fecha(dia, mes, anio)
        if not valida:
            print(centrar_texto(f"❌ {mensaje}"))
            pausar()
            return

    except ValueError:
        print(centrar_texto("❌ Error en la fecha ingresada"))
        pausar()
        return

    fecha_str = f"{dia:02d}/{mes:02d}/{anio}"

    # Mostrar turnos disponibles
    turnos_disponibles = obtener_turnos_disponibles(fecha_str)

    if not turnos_disponibles:
        print(centrar_texto(f"❌ No hay turnos disponibles para {fecha_str}"))
        pausar()
        return

    limpiar_pantalla()
    print(centrar_texto(f"=== TURNOS DISPONIBLES PARA {fecha_str} ==="))
    print()
    for i, (id_turno, turno) in enumerate(turnos_disponibles, 1):
        print(centrar_texto(f"{i}. {turno.get('horario', 'N/A')}"))
    print()

    # Seleccionar turno
    try:
        opcion = int(
            input(centrar_texto(f"Seleccione turno (1-{len(turnos_disponibles)}): "))
        )
        if 1 <= opcion <= len(turnos_disponibles):
            id_turno_seleccionado, turno_seleccionado = turnos_disponibles[opcion - 1]
        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()
            return
    except ValueError:
        print(centrar_texto("❌ Ingrese un número válido"))
        pausar()
        return

    # Confirmar turno
    limpiar_pantalla()
    print(centrar_texto("=== CONFIRMAR TURNO ==="))
    print(centrar_texto(f"Paciente: {paciente['nombre']} {paciente['apellido']}"))
    print(centrar_texto(f"DNI: {dni}"))
    print(centrar_texto(f"Fecha: {fecha_str}"))
    print(centrar_texto(f"Horario: {turno_seleccionado.get('horario', 'N/A')}"))
    print()

    confirmacion = input(centrar_texto("¿Confirma el turno? (s/n): ")).strip().lower()

    if confirmacion == "s":
        turnos = cargar_turnos()
        turnos[id_turno_seleccionado]["dni_paciente"] = dni
        turnos[id_turno_seleccionado][
            "paciente_nombre"
        ] = f"{paciente['nombre']} {paciente['apellido']}"

        if guardar_turnos(turnos):
            print(centrar_texto("✅ Turno asignado correctamente"))
        else:
            print(centrar_texto("❌ Error al guardar el turno"))
    else:
        print(centrar_texto("Turno cancelado"))
    pausar()


def cancelar_turno():
    """Cancela un turno existente"""
    limpiar_pantalla()
    print(centrar_texto("=== CANCELAR TURNO ==="))
    print()

    dni = input(centrar_texto("Ingrese DNI del paciente (0 para volver): ")).strip()
    if dni == "0":
        return

    # Buscar turnos del paciente
    turnos_paciente = obtener_turnos_paciente(dni)

    if not turnos_paciente:
        print(centrar_texto("❌ El paciente no tiene turnos asignados"))
        pausar()
        return

    limpiar_pantalla()
    print(centrar_texto("=== TURNOS DEL PACIENTE ==="))
    print(
        centrar_texto(
            f"Paciente: {turnos_paciente[0][1].get('paciente_nombre', 'N/A')}"
        )
    )
    print()

    for i, (id_turno, turno) in enumerate(turnos_paciente, 1):
        print(
            centrar_texto(
                f"{i}. {turno.get('fecha', 'N/A')} - {turno.get('horario', 'N/A')}"
            )
        )
    print()

    # Seleccionar turno a cancelar
    try:
        opcion = int(
            input(
                centrar_texto(
                    f"Seleccione turno a cancelar (1-{len(turnos_paciente)}): "
                )
            )
        )
        if 1 <= opcion <= len(turnos_paciente):
            id_turno_seleccionado, turno_seleccionado = turnos_paciente[opcion - 1]
        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()
            return
    except ValueError:
        print(centrar_texto("❌ Ingrese un número válido"))
        pausar()
        return

    # Confirmar cancelación
    limpiar_pantalla()
    print(centrar_texto("=== CONFIRMAR CANCELACIÓN ==="))
    print(
        centrar_texto(f"Paciente: {turno_seleccionado.get('paciente_nombre', 'N/A')}")
    )
    print(centrar_texto(f"Fecha: {turno_seleccionado.get('fecha', 'N/A')}"))
    print(centrar_texto(f"Horario: {turno_seleccionado.get('horario', 'N/A')}"))
    print()

    confirmacion = (
        input(centrar_texto("¿Confirma la cancelación? (s/n): ")).strip().lower()
    )

    if confirmacion == "s":
        turnos = cargar_turnos()
        # Limpiar el turno (vuelve a estar disponible)
        turnos[id_turno_seleccionado]["dni_paciente"] = ""
        turnos[id_turno_seleccionado]["paciente_nombre"] = ""

        if guardar_turnos(turnos):
            print(centrar_texto("✅ Turno cancelado correctamente"))
        else:
            print(centrar_texto("❌ Error al cancelar el turno"))
    else:
        print(centrar_texto("Cancelación cancelada"))
    pausar()


def buscar_turnos_paciente():
    """Busca y muestra todos los turnos de un paciente"""
    limpiar_pantalla()
    print(centrar_texto("=== BUSCAR TURNOS POR PACIENTE ==="))
    print()

    dni = input(centrar_texto("Ingrese DNI del paciente (0 para volver): ")).strip()
    if dni == "0":
        return

    turnos_paciente = obtener_turnos_paciente(dni)

    limpiar_pantalla()
    print(centrar_texto(f"=== TURNOS DEL PACIENTE DNI {dni} ==="))
    print()

    if not turnos_paciente:
        print(centrar_texto("❌ No hay turnos asignados a este paciente"))
    else:
        for i, (id_turno, turno) in enumerate(turnos_paciente, 1):
            print(
                centrar_texto(
                    f"{i}. {turno.get('fecha', 'N/A')} - {turno.get('horario', 'N/A')}"
                )
            )

    print()
    pausar()


def menu_turnos():
    """Menú principal del módulo de turnos"""
    while True:
        limpiar_pantalla()
        print(centrar_texto("=" * 50))
        print(centrar_texto("MÓDULO DE TURNOS"))
        print(centrar_texto("=" * 50))
        print(centrar_texto(""))
        print(centrar_texto("1. Asignar turno"))
        print(centrar_texto("2. Cancelar turno"))
        print(centrar_texto("3. Buscar turnos por paciente"))
        print(centrar_texto("4. Volver al menú principal"))
        print(centrar_texto(""))

        opcion = input(centrar_texto("Seleccione una opción (1-4): ")).strip()

        if opcion == "1":
            asignar_turno()
        elif opcion == "2":
            cancelar_turno()
        elif opcion == "3":
            buscar_turnos_paciente()
        elif opcion == "4":
            break
        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()


if __name__ == "__main__":
    menu_turnos()
