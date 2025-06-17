import json
import os
import shutil
from datetime import datetime, timedelta

# FUNCIONES DE PANTALLA


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


#### MENÚ DE CONFIGURACIÓN Y LOGICA ####


def menu_configuracion():
    while True:
        limpiar_pantalla()
        print(centrar_texto("=" * 50))
        print(centrar_texto("MÓDULO DE CONFIGURACIÓN"))
        print(centrar_texto("=" * 50))
        print()
        print(centrar_texto("1. Generar turnos del mes"))
        print(centrar_texto("2. Configurar horarios"))
        print(centrar_texto("3. Volver al menú principal"))
        print()
        opcion = input(centrar_texto("Seleccione una opción (1-3): ")).strip()
        match opcion:
            case "1":
                generar_turnos_mes()
            case "2":
                configurar_horarios()
            case "3":
                break
            case _:
                print(centrar_texto("❌ Opción inválida"))
                pausar()


#### FUNCIONES DE ARCHIVO ####


def cargar_configuracion():
    try:
        if os.path.exists("data/configuracion.json"):
            with open("data/configuracion.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    except:
        return None


def guardar_configuracion(config):
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/configuracion.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False


def cargar_turnos():
    try:
        if os.path.exists("data/turnos.json"):
            with open("data/turnos.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}


def guardar_turnos(turnos):
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/turnos.json", "w", encoding="utf-8") as f:
            json.dump(turnos, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False


#### FUNCIONES AUXILIARES ####


def obtener_siguiente_id():
    turnos = cargar_turnos()
    if not turnos:
        return 1
    ids = [int(k) for k in turnos.keys() if k.isdigit()]
    return max(ids) + 1 if ids else 1


def generar_horarios(hora_inicio, hora_fin, intervalo):
    horarios = []
    hora = hora_inicio
    minutos = 0
    while hora < hora_fin:
        horarios.append(f"{hora:02d}:{minutos:02d}")
        minutos += intervalo
        if minutos >= 60:
            hora += 1
            minutos = 0
    return horarios


def obtener_dias_laborables(mes, anio):
    primer_dia = datetime(anio, mes, 1)
    if mes == 12:
        ultimo_dia = datetime(anio + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia = datetime(anio, mes + 1, 1) - timedelta(days=1)
    dias = []
    actual = primer_dia
    while actual <= ultimo_dia:
        if actual.weekday() < 5:
            dias.append(actual.strftime("%d/%m/%Y"))
        actual += timedelta(days=1)
    return dias


# GENERAR TURNOS DEL MES


def generar_turnos_mes():
    limpiar_pantalla()
    print(centrar_texto("=== GENERAR TURNOS DEL MES ==="))
    print()

    config = cargar_configuracion()
    if not config:
        print(centrar_texto("❌ Primero debe configurar los horarios"))
        pausar()
        return

    try:
        mes_input = input(centrar_texto("Ingrese mes (1-12) o 0 para volver: ")).strip()
        if mes_input == "0":
            return
        mes = int(mes_input)
        if mes < 1 or mes > 12:
            print(centrar_texto("❌ Mes inválido"))
            pausar()
            return

        anio_actual = datetime.now().year
        anio_input = input(
            centrar_texto(f"Ingrese año (mínimo {anio_actual}) o 0 para volver: ")
        ).strip()
        if anio_input == "0":
            return
        anio = int(anio_input)
        if anio < anio_actual:
            print(centrar_texto(f"❌ El año debe ser mayor o igual a {anio_actual}"))
            pausar()
            return

    except ValueError:
        print(centrar_texto("❌ Ingrese números válidos"))
        pausar()
        return

    turnos = cargar_turnos()

    for t in turnos.values():
        fecha = t.get("fecha", "")
        if fecha.endswith(f"/{mes:02d}/{anio}"):
            print()
            print(
                centrar_texto(
                    f"⚠️ Ya fueron generados los turnos del mes {mes:02d} año {anio}"
                )
            )
            pausar()
            return

    dias = obtener_dias_laborables(mes, anio)
    horarios = generar_horarios(
        config["hora_inicio"], config["hora_fin"], config["intervalo_minutos"]
    )
    siguiente_id = obtener_siguiente_id()
    generados = 0

    for fecha in dias:
        for horario in horarios:
            turnos[str(siguiente_id)] = {
                "dni_paciente": "",
                "fecha": fecha,
                "horario": horario,
                "paciente_nombre": "",
            }
            siguiente_id += 1
            generados += 1

    if guardar_turnos(turnos):
        limpiar_pantalla()
        print(centrar_texto("=== TURNOS GENERADOS EXITOSAMENTE ==="))
        print(centrar_texto(f"Mes: {mes:02d}/{anio}"))
        print(centrar_texto(f"Días laborables: {len(dias)}"))
        print(centrar_texto(f"Horarios por día: {len(horarios)}"))
        print(centrar_texto(f"Turnos generados: {generados}"))
    else:
        print(centrar_texto("❌ Error al guardar turnos"))
    pausar()


#### CONFIGURAR HORARIOS ####


def configurar_horarios():
    limpiar_pantalla()
    print(centrar_texto("=== CONFIGURAR HORARIOS ==="))
    print()

    try:
        hora_inicio_input = input(
            centrar_texto("Ingrese hora de inicio (1-23) o 0 para salir: ")
        ).strip()
        if hora_inicio_input == "0":
            return
        hora_inicio = int(hora_inicio_input)
        if hora_inicio < 1 or hora_inicio > 23:
            print(centrar_texto("❌ Hora inválida"))
            pausar()
            return

        hora_fin_input = input(
            centrar_texto(
                "Ingrese hora de fin (mayor a inicio, máx 23) o 0 para salir: "
            )
        ).strip()
        if hora_fin_input == "0":
            return
        hora_fin = int(hora_fin_input)
        if hora_fin <= hora_inicio or hora_fin > 23:
            print(centrar_texto("❌ Hora de fin inválida"))
            pausar()
            return

        print()
        print(centrar_texto("Seleccione intervalo entre turnos:"))
        print(centrar_texto("1. 15 minutos"))
        print(centrar_texto("2. 20 minutos"))
        print(centrar_texto("3. 30 minutos"))
        print(centrar_texto("0. Cancelar y volver"))
        opcion = input(centrar_texto("Opción (0-3): ")).strip()

        match opcion:
            case "1":
                intervalo = 15
            case "2":
                intervalo = 20
            case "3":
                intervalo = 30
            case "0":
                return
            case _:
                print(centrar_texto("❌ Opción inválida"))
                pausar()
                return

    except ValueError:
        print(centrar_texto("❌ Entrada inválida"))
        pausar()
        return

    config = {
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "intervalo_minutos": intervalo,
    }

    limpiar_pantalla()
    print(centrar_texto("=== NUEVA CONFIGURACIÓN ==="))
    print(centrar_texto(f"Inicio: {hora_inicio:02d}:00"))
    print(centrar_texto(f"Fin: {hora_fin:02d}:00"))
    print(centrar_texto(f"Intervalo: {intervalo} minutos"))
    print()

    if input(centrar_texto("¿Confirmar cambios? (s/n): ")).strip().lower() == "s":
        if guardar_configuracion(config):
            print(centrar_texto("✅ Configuración guardada"))
        else:
            print(centrar_texto("❌ Error al guardar"))
    else:
        print(centrar_texto("❌ Cambios cancelados"))
    pausar()
