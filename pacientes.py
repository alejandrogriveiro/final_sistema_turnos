"""
MÓDULO 1: GESTIÓN DE PACIENTES
Responsable: [Nombre del Estudiante A]

Este módulo se encarga de:
- Registrar nuevos pacientes
- Modificar datos de pacientes existentes
- Eliminar pacientes del sistema
- Validar datos personales (DNI, email, teléfono, nombres)
"""

import json
import os
import re
import shutil


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


def cargar_pacientes():
    """Carga los datos de pacientes desde el archivo JSON"""
    try:
        if os.path.exists("data/pacientes.json"):
            with open("data/pacientes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(centrar_texto(f"Error al cargar pacientes: {e}"))
        return {}


def guardar_pacientes(pacientes):
    """Guarda los datos de pacientes en el archivo JSON"""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/pacientes.json", "w", encoding="utf-8") as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(centrar_texto(f"Error al guardar pacientes: {e}"))
        return False


def validar_dni(dni):
    """Valida que el DNI sea un número de 7-8 dígitos"""
    return dni.isdigit() and 7 <= len(dni) <= 8


def validar_email(email):
    """Valida el formato del email"""
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None


def validar_telefono(telefono):
    """Valida que el teléfono contenga solo números, espacios y guiones"""
    patron = r"^[0-9\-\s\+()]+$"
    return (
        re.match(patron, telefono) is not None
        and len(telefono.replace(" ", "").replace("-", "")) >= 8
    )


def validar_nombre(nombre):
    """Valida que el nombre contenga solo letras y espacios"""
    return nombre.replace(" ", "").isalpha() and len(nombre.strip()) >= 2


def solicitar_datos_paciente():
    """Solicita y valida los datos de un nuevo paciente"""
    print(centrar_texto("=== DATOS DEL PACIENTE ==="))
    print()

    # Solicitar nombre
    while True:
        nombre = (
            input(centrar_texto("Ingrese nombre (0 para cancelar): ")).strip().title()
        )
        if nombre == "0":
            return None
        if not nombre:
            print(centrar_texto("❌ El nombre es obligatorio"))
            pausar()
            continue
        if not validar_nombre(nombre):
            print(centrar_texto("❌ Nombre inválido. Solo letras y espacios"))
            pausar()
            continue
        break

    # Solicitar apellido
    while True:
        apellido = (
            input(centrar_texto("Ingrese apellido (0 para cancelar): ")).strip().title()
        )
        if apellido == "0":
            return None
        if not apellido:
            print(centrar_texto("❌ El apellido es obligatorio"))
            pausar()
            continue
        if not validar_nombre(apellido):
            print(centrar_texto("❌ Apellido inválido. Solo letras y espacios"))
            pausar()
            continue
        break

    # Solicitar teléfono
    while True:
        telefono = input(centrar_texto("Ingrese teléfono (0 para cancelar): ")).strip()
        if telefono == "0":
            return None
        if not telefono:
            print(centrar_texto("❌ El teléfono es obligatorio"))
            pausar()
            continue
        if not validar_telefono(telefono):
            print(centrar_texto("❌ Teléfono inválido"))
            pausar()
            continue
        break

    # Solicitar email
    while True:
        email = (
            input(centrar_texto("Ingrese email (0 para cancelar): ")).strip().lower()
        )
        if email == "0":
            return None
        if not email:
            print(centrar_texto("❌ El email es obligatorio"))
            pausar()
            continue
        if not validar_email(email):
            print(centrar_texto("❌ Email inválido"))
            pausar()
            continue
        break

    return {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email,
    }


def alta_paciente():
    """Registra un nuevo paciente en el sistema"""
    limpiar_pantalla()
    print(centrar_texto("=== ALTA DE PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()

    # Solicitar DNI
    while True:
        dni = input(
            centrar_texto("Ingrese DNI (7-8 dígitos) o 0 para volver: ")
        ).strip()
        if dni == "0":
            return
        if not dni:
            print(centrar_texto("❌ El DNI es obligatorio"))
            pausar()
            continue
        if not validar_dni(dni):
            print(centrar_texto("❌ DNI inválido. Debe tener 7-8 dígitos"))
            pausar()
            continue
        if dni in pacientes:
            print(centrar_texto("❌ Ya existe un paciente con ese DNI"))
            pausar()
            continue
        break

    # Solicitar datos del paciente
    datos = solicitar_datos_paciente()

    if datos is None:
        print(centrar_texto("Operación cancelada"))
        pausar()
        return

    # Guardar paciente
    pacientes[dni] = datos

    if guardar_pacientes(pacientes):
        print(
            centrar_texto(
                f"✅ Paciente {datos['nombre']} {datos['apellido']} registrado correctamente"
            )
        )
    else:
        print(centrar_texto("❌ Error al guardar el paciente"))
    pausar()


def modificar_paciente():
    """Modifica los datos de un paciente existente"""
    limpiar_pantalla()
    print(centrar_texto("=== MODIFICAR PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()

    if not pacientes:
        print(centrar_texto("❌ No hay pacientes registrados"))
        pausar()
        return

    dni = input(
        centrar_texto("Ingrese DNI del paciente a modificar (0 para volver): ")
    ).strip()
    if dni == "0":
        return

    if dni not in pacientes:
        print(centrar_texto("❌ No existe un paciente con ese DNI"))
        pausar()
        return

    paciente = pacientes[dni]

    while True:
        limpiar_pantalla()
        print(centrar_texto("=== DATOS ACTUALES DEL PACIENTE ==="))
        print(centrar_texto(f"DNI: {dni}"))
        print(centrar_texto(f"1. Nombre: {paciente['nombre']}"))
        print(centrar_texto(f"2. Apellido: {paciente['apellido']}"))
        print(centrar_texto(f"3. Teléfono: {paciente['telefono']}"))
        print(centrar_texto(f"4. Email: {paciente['email']}"))
        print()

        opcion = input(
            centrar_texto("¿Qué dato desea modificar? (1-4, 0 para salir): ")
        ).strip()

        if opcion == "0":
            break

        elif opcion == "1":
            nuevo_nombre = (
                input(centrar_texto("Nuevo nombre, enter para cancelar: "))
                .strip()
                .title()
            )
            if nuevo_nombre == "":
                # El usuario no quiso modificar, volvemos al menú de opciones
                continue
            if validar_nombre(nuevo_nombre):
                paciente["nombre"] = nuevo_nombre
                print(centrar_texto("✅ Nombre actualizado"))
            else:
                print(centrar_texto("❌ Nombre inválido"))
            pausar()

        elif opcion == "2":
            nuevo_apellido = (
                input(centrar_texto("Nuevo apellido, enter para cancelar: "))
                .strip()
                .title()
            )
            if nuevo_apellido == "":
                # El usuario no quiso modificar, volvemos al menú de opciones
                continue
            if validar_nombre(nuevo_apellido):
                paciente["apellido"] = nuevo_apellido
                print(centrar_texto("✅ Apellido actualizado"))
            else:
                print(centrar_texto("❌ Apellido inválido"))
            pausar()

        elif opcion == "3":
            nuevo_telefono = input(
                centrar_texto("Nuevo teléfono, enter para cancelar: ")
            ).strip()
            if nuevo_telefono == "":
                # El usuario no quiso modificar, volvemos al menú de opciones
                continue
            if validar_telefono(nuevo_telefono):
                paciente["telefono"] = nuevo_telefono
                print(centrar_texto("✅ Teléfono actualizado"))
            else:
                print(centrar_texto("❌ Teléfono inválido"))
            pausar()

        elif opcion == "4":
            nuevo_email = (
                input(centrar_texto("Nuevo email, enter para cancelar: "))
                .strip()
                .lower()
            )
            if nuevo_email == "":
                # El usuario no quiso modificar, volvemos al menú de opciones
                continue
            if validar_email(nuevo_email):
                paciente["email"] = nuevo_email
                print(centrar_texto("✅ Email actualizado"))
            else:
                print(centrar_texto("❌ Email inválido"))
            pausar()

        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()

    pacientes[dni] = paciente
    if guardar_pacientes(pacientes):
        print(centrar_texto("✅ Cambios guardados correctamente"))
    else:
        print(centrar_texto("❌ Error al guardar los cambios"))
    pausar()


def eliminar_paciente():
    """Elimina un paciente del sistema"""
    limpiar_pantalla()
    print(centrar_texto("=== ELIMINAR PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()

    if not pacientes:
        print(centrar_texto("❌ No hay pacientes registrados"))
        pausar()
        return

    # Solicitar DNI
    dni = input(
        centrar_texto("Ingrese DNI del paciente a eliminar (0 para volver): ")
    ).strip()
    if dni == "0":
        return

    if dni not in pacientes:
        print(centrar_texto("❌ No existe un paciente con ese DNI"))
        pausar()
        return

    paciente = pacientes[dni]
    limpiar_pantalla()
    print(centrar_texto("=== CONFIRMAR ELIMINACIÓN ==="))
    print(centrar_texto(f"DNI: {dni}"))
    print(centrar_texto(f"Nombre: {paciente['nombre']} {paciente['apellido']}"))
    print(centrar_texto(f"Teléfono: {paciente['telefono']}"))
    print(centrar_texto(f"Email: {paciente['email']}"))
    print()

    confirmacion = (
        input(centrar_texto("¿Confirma la eliminación? (s/n): ")).strip().lower()
    )

    if confirmacion == "s":
        # Verificar si tiene turnos asignados
        from turnos import verificar_turnos_paciente

        if verificar_turnos_paciente(dni):
            print(
                centrar_texto(
                    "❌ No se puede eliminar. El paciente tiene turnos asignados"
                )
            )
            pausar()
            return

        del pacientes[dni]

        if guardar_pacientes(pacientes):
            print(centrar_texto("✅ Paciente eliminado correctamente"))
        else:
            print(centrar_texto("❌ Error al eliminar el paciente"))
    else:
        print(centrar_texto("Eliminación cancelada"))
    pausar()


def consultar_paciente():
    """Consulta los datos de un paciente por DNI"""
    limpiar_pantalla()
    print(centrar_texto("=== CONSULTAR PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()

    if not pacientes:
        print(centrar_texto("❌ No hay pacientes registrados"))
        pausar()
        return

    dni = input(
        centrar_texto("Ingrese DNI del paciente a consultar (0 para volver): ")
    ).strip()
    if dni == "0":
        return

    if not validar_dni(dni):
        print(centrar_texto("❌ DNI inválido"))
        pausar()
        return

    paciente = pacientes.get(dni)

    if paciente is None:
        print(centrar_texto("❌ No se encontró un paciente con ese DNI"))
        pausar()
        return

    limpiar_pantalla()
    print(centrar_texto("=== DATOS DEL PACIENTE ==="))
    print(centrar_texto(f"DNI: {dni}"))
    print(centrar_texto(f"Nombre: {paciente['nombre']} {paciente['apellido']}"))
    print(centrar_texto(f"Teléfono: {paciente['telefono']}"))
    print(centrar_texto(f"Email: {paciente['email']}"))
    pausar()


def menu_pacientes():
    """Menú principal del módulo de pacientes"""
    while True:
        limpiar_pantalla()
        print(centrar_texto("=" * 50))
        print(centrar_texto("MÓDULO DE PACIENTES"))
        print(centrar_texto("=" * 50))
        print(centrar_texto(""))
        print(centrar_texto("1. Alta de paciente"))
        print(centrar_texto("2. Modificar paciente"))
        print(centrar_texto("3. Eliminar paciente"))
        print(centrar_texto("4. Consultar paciente"))
        print(centrar_texto("5. Volver al menú principal"))

        print(centrar_texto(""))

        opcion = input(centrar_texto("Seleccione una opción (1-5): ")).strip()

        if opcion == "1":
            alta_paciente()
        elif opcion == "2":
            modificar_paciente()
        elif opcion == "3":
            eliminar_paciente()
        elif opcion == "4":
            consultar_paciente()
        elif opcion == "5":
            break
        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()


# Función para que otros módulos verifiquen si existe un paciente
def obtener_paciente(dni):
    """Obtiene los datos de un paciente por DNI"""
    pacientes = cargar_pacientes()
    return pacientes.get(dni, None)


if __name__ == "__main__":
    menu_pacientes()
