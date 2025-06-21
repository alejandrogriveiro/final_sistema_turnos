import json
import os
import shutil
from datetime import datetime


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def centrar_texto(texto):
    try:
        ancho_terminal = shutil.get_terminal_size().columns
    except:
        ancho_terminal = 80

    if len(texto) >= ancho_terminal:
        return texto

    espacios = (ancho_terminal - len(texto)) // 2
    return " " * espacios + texto


def pausar():
    input(centrar_texto("Presione Enter para continuar..."))


def cargar_turnos():
    try:
        if os.path.exists("data/turnos.json"):
            with open("data/turnos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(centrar_texto(f"Error al cargar turnos: {e}"))
        return {}


def generar_informe(tipo="dia"):
    limpiar_pantalla()
    es_informe_dia = tipo == "dia"
    titulo = (
        "=== INFORME DE TURNOS DEL DÍA ==="
        if es_informe_dia
        else "=== INFORME DE TURNOS DEL MES ==="
    )
    print(centrar_texto(titulo))
    print()

    try:
        dia = None
        if es_informe_dia:
            dia_input = input(
                centrar_texto("Ingrese día (1-31) o 0 para volver: ")
            ).strip()
            if dia_input == "0":
                return
            dia = int(dia_input)

        mes_input = input(centrar_texto("Ingrese mes (1-12) o 0 para volver: ")).strip()
        if mes_input == "0":
            return
        mes = int(mes_input)

        anio_input = input(centrar_texto("Ingrese año o 0 para volver: ")).strip()
        if anio_input == "0":
            return
        anio = int(anio_input)

        if mes < 1 or mes > 12:
            print(centrar_texto("❌ Mes inválido"))
            pausar()
            return

        if dia is not None and (dia < 1 or dia > 31):
            print(centrar_texto("❌ Día inválido"))
            pausar()
            return

        fecha_buscar = f"{dia:02d}/{mes:02d}/{anio}" if dia is not None else None

    except ValueError:
        print(centrar_texto("❌ Error en los datos ingresados"))
        pausar()
        return

    turnos = cargar_turnos()
    turnos_filtrados = []

    for turno in turnos.values():
        if turno.get("dni_paciente", "") == "":
            continue

        fecha_turno = turno.get("fecha", "")
        if not fecha_turno:
            continue

        if es_informe_dia:
            if fecha_turno == fecha_buscar:
                turnos_filtrados.append(turno)
        else:
            try:
                partes_fecha = fecha_turno.split("/")
                if len(partes_fecha) == 3:
                    mes_turno = int(partes_fecha[1])
                    anio_turno = int(partes_fecha[2])

                    if mes_turno == mes and anio_turno == anio:
                        turnos_filtrados.append(turno)
            except:
                continue

    if es_informe_dia:
        turnos_filtrados.sort(key=lambda x: x.get("horario", ""))
    else:
        turnos_filtrados.sort(key=lambda x: (x.get("fecha", ""), x.get("horario", "")))

    contenido = []
    contenido.append("=" * 60)

    if es_informe_dia:
        contenido.append(f"INFORME DE TURNOS DEL DÍA {fecha_buscar}")
    else:
        contenido.append(f"INFORME DE TURNOS DEL MES {mes:02d}/{anio}")

    contenido.append("=" * 60)
    contenido.append(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    contenido.append("")

    if turnos_filtrados:
        contenido.append(f"Total de turnos: {len(turnos_filtrados)}")
        contenido.append("")

        if es_informe_dia:
            contenido.append("DETALLE DE TURNOS:")
            contenido.append("-" * 40)

            for turno in turnos_filtrados:
                contenido.append(f"Horario: {turno.get('horario', 'N/A')}")
                contenido.append(f"Paciente: {turno.get('paciente_nombre', 'N/A')}")
                contenido.append(f"DNI: {turno.get('dni_paciente', 'N/A')}")
                contenido.append("-" * 40)
        else:
            fechas_unicas = sorted(
                list(set(t.get("fecha", "") for t in turnos_filtrados))
            )

            for fecha in fechas_unicas:
                turnos_dia = [t for t in turnos_filtrados if t.get("fecha") == fecha]

                contenido.append(f"TURNOS DEL {fecha}:")
                contenido.append("-" * 30)

                for turno in turnos_dia:
                    contenido.append(
                        f"  {turno.get('horario', 'N/A')} - {turno.get('paciente_nombre', 'N/A')} (DNI: {turno.get('dni_paciente', 'N/A')})"
                    )

                contenido.append("")
    else:
        if es_informe_dia:
            contenido.append("No hay turnos programados para esta fecha.")
        else:
            contenido.append("No hay turnos asignados para este mes.")

    contenido.append("Fin del informe")

    limpiar_pantalla()
    for linea in contenido:
        print(centrar_texto(linea))

    if es_informe_dia:
        nombre_archivo = f"turnos_dia_{dia:02d}_{mes:02d}_{anio}.txt"
    else:
        nombre_archivo = f"turnos_mes_{mes:02d}_{anio}.txt"

    ruta_archivo = os.path.join("informes", nombre_archivo)

    if not turnos_filtrados:
        print()
        if es_informe_dia:
            print(
                centrar_texto(
                    "⚠️ No hay turnos para la fecha indicada. No se generó archivo."
                )
            )
        else:
            print(
                centrar_texto(
                    "⚠️ No hay turnos para el mes indicado. No se generó archivo."
                )
            )
        pausar()
        return

    try:
        os.makedirs("informes", exist_ok=True)
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            for linea in contenido:
                f.write(linea + "\n")
        print()
        print(centrar_texto(f"✅ Informe guardado en: {ruta_archivo}"))
    except Exception as e:
        print(centrar_texto(f"❌ Error al guardar el informe: {e}"))
    pausar()


def menu_informes():
    while True:
        limpiar_pantalla()
        print(centrar_texto("=" * 50))
        print(centrar_texto("MÓDULO DE INFORMES"))
        print(centrar_texto("=" * 50))
        print(centrar_texto(""))
        print(centrar_texto("1. Informe de turnos del día"))
        print(centrar_texto("2. Informe de turnos del mes"))
        print(centrar_texto("3. Volver al menú principal"))
        print(centrar_texto(""))

        opcion = input(centrar_texto("Seleccione una opción (1-3): ")).strip()

        if opcion == "1":
            generar_informe(tipo="dia")
        elif opcion == "2":
            generar_informe(tipo="mes")
        elif opcion == "3":
            break
        else:
            print(centrar_texto("❌ Opción inválida"))
            pausar()


if __name__ == "__main__":
    menu_informes()
