"""
MÓDULO 4: INTERFAZ Y REPORTES (REFACTORIZADO)
Responsable: [Nombre del Estudiante D]

Este módulo se encarga de:
- Generación de informes y reportes
- Menú de informes
- Funciones auxiliares para reportes
"""

import json
import os
import shutil
from datetime import datetime

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

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
    """Carga los turnos desde el archivo JSON"""
    try:
        if os.path.exists("data/turnos.json"):
            with open("data/turnos.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(centrar_texto(f"Error al cargar turnos: {e}"))
        return {}

def generar_informe(tipo="dia"):
    """
    Genera informe de turnos según el tipo especificado
    
    Args:
        tipo (str): Tipo de informe ('dia' o 'mes')
    """
    limpiar_pantalla()
    es_informe_dia = tipo == "dia"
    titulo = "=== INFORME DE TURNOS DEL DÍA ===" if es_informe_dia else "=== INFORME DE TURNOS DEL MES ==="
    print(centrar_texto(titulo))
    print()
    
    # Solicitar datos de fecha
    try:
        dia = None
        if es_informe_dia:
            dia_input = input(centrar_texto("Ingrese día (1-31) o 0 para volver: ")).strip()
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
    
    # Buscar turnos según el criterio
    turnos = cargar_turnos()
    turnos_filtrados = []
    
    for turno in turnos.values():
        if turno.get("dni_paciente", "") == "":
            continue
            
        fecha_turno = turno.get("fecha", "")
        if not fecha_turno:
            continue
            
        if es_informe_dia:
            # Para informe diario, comparamos la fecha exacta
            if fecha_turno == fecha_buscar:
                turnos_filtrados.append(turno)
        else:
            # Para informe mensual, comparamos solo mes y año
            try:
                partes_fecha = fecha_turno.split('/')
                if len(partes_fecha) == 3:
                    mes_turno = int(partes_fecha[1])
                    anio_turno = int(partes_fecha[2])
                    
                    if mes_turno == mes and anio_turno == anio:
                        turnos_filtrados.append(turno)
            except:
                continue
    
    # Ordenar los turnos
    if es_informe_dia:
        # Para informe diario, ordenar solo por horario
        turnos_filtrados.sort(key=lambda x: x.get("horario", ""))
    else:
        # Para informe mensual, ordenar por fecha y horario
        turnos_filtrados.sort(key=lambda x: (x.get("fecha", ""), x.get("horario", "")))
    
    # Generar contenido del informe
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
            # Formato para informe diario
            contenido.append("DETALLE DE TURNOS:")
            contenido.append("-" * 40)
            
            for turno in turnos_filtrados:
                contenido.append(f"Horario: {turno.get('horario', 'N/A')}")
                contenido.append(f"Paciente: {turno.get('paciente_nombre', 'N/A')}")
                contenido.append(f"DNI: {turno.get('dni_paciente', 'N/A')}")
                contenido.append("-" * 40)
        else:
            # Formato para informe mensual (agrupado por día)
            fechas_unicas = sorted(list(set(t.get("fecha", "") for t in turnos_filtrados)))
            
            for fecha in fechas_unicas:
                turnos_dia = [t for t in turnos_filtrados if t.get("fecha") == fecha]
                
                contenido.append(f"TURNOS DEL {fecha}:")
                contenido.append("-" * 30)
                
                for turno in turnos_dia:
                    contenido.append(f"  {turno.get('horario', 'N/A')} - {turno.get('paciente_nombre', 'N/A')} (DNI: {turno.get('dni_paciente', 'N/A')})")
                
                contenido.append("")
    else:
        if es_informe_dia:
            contenido.append("No hay turnos programados para esta fecha.")
        else:
            contenido.append("No hay turnos asignados para este mes.")
    
    contenido.append("Fin del informe")
    
    # Mostrar informe en pantalla
    limpiar_pantalla()
    for linea in contenido:
        print(centrar_texto(linea))
    
    # Guardar informe en archivo
    if es_informe_dia:
        nombre_archivo = f"turnos_dia_{dia:02d}_{mes:02d}_{anio}.txt"
    else:
        nombre_archivo = f"turnos_mes_{mes:02d}_{anio}.txt"
        
    ruta_archivo = os.path.join("informes", nombre_archivo)
    
    try:
        # Asegurar que el directorio existe
        os.makedirs("informes", exist_ok=True)
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            for linea in contenido:
                f.write(linea + '\n')
        print()
        print(centrar_texto(f"✅ Informe guardado en: {ruta_archivo}"))
    except Exception as e:
        print(centrar_texto(f"❌ Error al guardar el informe: {e}"))
    pausar()

def menu_informes():
    """Menú del módulo de informes"""
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
    # Para pruebas individuales del módulo
    menu_informes()
