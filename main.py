import os
import sys
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


#### CREACION DE DIRECTORIOS SI NO EXISTEN ####


def crear_directorios():
    """Crea los directorios necesarios si no existen"""
    directorios = ["data", "informes"]
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)


#### MENU PRINCIPAL Y LOGICA DE LA APLICACION  ####


def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    limpiar_pantalla()
    print(centrar_texto("=" * 60))
    print(centrar_texto("SISTEMA DE GESTIÓN DE TURNOS - CONSULTORIO MÉDICO"))
    print(centrar_texto("=" * 60))
    print(centrar_texto(""))
    print(centrar_texto("1. Gestión de Pacientes"))
    print(centrar_texto("2. Gestión de Turnos"))
    print(centrar_texto("3. Configuración y Generación"))
    print(centrar_texto("4. Informes y Reportes"))
    print(centrar_texto("5. Salir"))
    print(centrar_texto(""))
    print(centrar_texto("-" * 60))
    print(centrar_texto("By UNER - Programación I - Grupo 38"))
    print(centrar_texto("Todos los derechos reservados 2025"))
    print(centrar_texto("-" * 60))


def main():
    """Función principal del programa"""
    crear_directorios()

    while True:
        mostrar_menu_principal()

        try:
            opcion = input(centrar_texto("Seleccione una opción (1-5): ")).strip()

            match opcion:
                case "1":
                    from pacientes import menu_pacientes

                    menu_pacientes()
                case "2":
                    from turnos import menu_turnos

                    menu_turnos()
                case "3":
                    from configuracion import menu_configuracion

                    menu_configuracion()
                case "4":
                    from interfaz_reportes import menu_informes

                    menu_informes()
                case "5":
                    limpiar_pantalla()
                    print(centrar_texto("¡Gracias por usar el sistema!"))
                    print(centrar_texto("Hasta luego"))
                    sys.exit()
                case _:
                    print(
                        centrar_texto(
                            "❌ Opción inválida. Seleccione una opción del 1 al 5."
                        )
                    )
                    pausar()

        except KeyboardInterrupt:
            limpiar_pantalla()
            print(centrar_texto("Programa interrumpido por el usuario"))
            sys.exit()
        except Exception as e:
            print(centrar_texto(f"❌ Error inesperado: {str(e)}"))
            pausar()


if __name__ == "__main__":
    main()
