
import json
import os
import re
import shutil

#Limpiar la pantalla
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

#Centrar el texto
def centrar_texto(texto):
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:    
        ancho_terminal = 80

    if len(texto) >= ancho_terminal:
        return texto

    espacios = (ancho_terminal - len(texto)) // 2
    return " " * espacios + texto
    
#Pausa hasta que el usuario presione enter
def pausar():
    input(centrar_texto("Presione Enter para continuar..."))
    
#-------------------------------------------------------    
    
#Carga los datos desde el archivo json
def cargar_pacientes():
    try:
        if os.path.exists("data/pacientes.json"):
            with open("data/pacientes.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(centrar_texto(f"Error al cargar pacientes: {e}"))
        return {}

#Guarda los datos en el archivo json
def guardar_pacientes(pacientes):
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/pacientes.json", "w", encoding="utf-8") as f:
            json.dump(pacientes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(centrar_texto(f"Error al guardar pacientes: {e}"))
        return False
#----------------------------------------------------------------------

#Validar formato dni
def validar_dni(dni):
    return dni.isdigit() and 7 <= len(dni) <= 8

#Validar formato email
def validar_email(email):
    patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None

#Validar formato telefono
def validar_telefono(telefono):
    patron = r"^[0-9\-\s\+()]+$"
    return (
        re.match(patron, telefono) is not None
        and len(telefono.replace(" ", "").replace("-", "")) >= 8
    )

#Validar formato de nombre 
def validar_nombre(nombre):
    return nombre.replace(" ", "").isalpha() and len(nombre.strip()) >= 2

#--------------------------------------------------------------------------

#solicitar y validar datos de nuevo paciente
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
        #devuelve un dicc con los datos del paciente
    }
#----------------------------------------------------------------

#Registra un nuevo paciente
def alta_paciente():
    limpiar_pantalla()
    print(centrar_texto("=== ALTA DE PACIENTE ==="))
    print()
 
    pacientes = cargar_pacientes() #carga los pacientes en el diccionario pacientes

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

    datos = solicitar_datos_paciente()

    if datos is None:
        print(centrar_texto("Operación cancelada"))
        pausar()
        return

    # Guardar paciente una nueva entrada
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
    

#Modificar datos de un paciente
def modificar_paciente():
    limpiar_pantalla()
    print(centrar_texto("=== MODIFICAR PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()  #carga los pacientes en el diccionario pacientes

    if not pacientes:
        print(centrar_texto("❌ No hay pacientes registrados"))
        pausar()
        return

    dni = input(
        centrar_texto("Ingrese DNI del paciente a modificar (0 para volver): ")
    ).strip()
    if dni == "0":
        return
    
    if not validar_dni(dni):
        print(centrar_texto("❌ DNI inválido.  Debe tener 7-8 dígitos"))
        pausar()
        return

    if dni not in pacientes:
        print(centrar_texto("❌ No existe un paciente con ese DNI"))
        pausar()
        return
    
    paciente = pacientes.get(dni) #guarda temporalmente el paciente a modificar

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

#Eliminar un paciente
def eliminar_paciente():
    limpiar_pantalla()
    print(centrar_texto("=== ELIMINAR PACIENTE ==="))
    print()

    pacientes = cargar_pacientes()

    if not pacientes:
        print(centrar_texto("❌ No hay pacientes registrados"))
        pausar()
        return

    dni = input(
        centrar_texto("Ingrese DNI del paciente a eliminar (0 para volver): ")
    ).strip()
    if dni == "0":
        return
   
    if not validar_dni(dni):
        print(centrar_texto("❌ DNI inválido. Debe tener 7-8 dígitos"))
        pausar()
        return

    if dni not in pacientes:
        print(centrar_texto("❌ No existe un paciente con ese DNI")) 
        
        pausar()
        return

    paciente = pacientes.get(dni) #guarda temporalmente el paciente a modificar
    
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

#Consulta datos de un paciente
def consultar_paciente():
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
        print(centrar_texto("❌ DNI inválido. Debe tener 7-8 dígitos"))
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

#Menu principal 
def menu_pacientes():
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
#Este bloque se ejecuta solo si el archivo se ejecuta directamente (por ejemplo, con python pacientes.py).