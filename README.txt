================================================================================
                    SISTEMA DE GESTIÓN DE TURNOS - CONSULTORIO MÉDICO
================================================================================

DESCRIPCIÓN GENERAL
===================
Sistema integral para la gestión de turnos médicos desarrollado en Python.
Permite administrar pacientes, asignar y cancelar turnos, configurar horarios
de atención y generar reportes detallados.

CARACTERÍSTICAS PRINCIPALES
===========================
✓ Gestión completa de pacientes (alta, modificación, eliminación)
✓ Sistema de turnos con asignación y cancelación
✓ Configuración flexible de horarios de atención
✓ Generación automática de turnos mensuales
✓ Reportes diarios y mensuales
✓ Interfaz de consola centrada y amigable
✓ Validación robusta de datos
✓ Persistencia de datos en formato JSON

ESTRUCTURA DEL PROYECTO
=======================
sistema-turnos/
├── main.py                    # Archivo principal del sistema
├── pacientes.py              # Módulo de gestión de pacientes
├── turnos.py                 # Módulo de gestión de turnos
├── configuracion.py          # Módulo de configuración y generación
├── interfaz_reportes.py      # Módulo de informes y reportes
├── data/                     # Directorio de datos (se crea automáticamente)
│   ├── pacientes.json        # Base de datos de pacientes
│   ├── turnos.json          # Base de datos de turnos
│   └── configuracion.json   # Configuración del sistema
├── informes/                # Directorio de informes (se crea automáticamente)
└── README.txt              # Este archivo

MÓDULOS DEL SISTEMA
===================

1. MÓDULO DE PACIENTES (pacientes.py)
   - Alta de nuevos pacientes
   - Modificación de datos existentes
   - Eliminación de pacientes
   - Validación de DNI, email, teléfono y nombres
   - Verificación de duplicados

2. MÓDULO DE TURNOS (turnos.py)
   - Asignación de turnos a pacientes
   - Cancelación de turnos existentes
   - Búsqueda de turnos por paciente
   - Validación de fechas futuras
   - Control de disponibilidad

3. MÓDULO DE CONFIGURACIÓN (configuracion.py)
   - Configuración de horarios de atención
   - Definición de intervalos entre turnos (15, 20 o 30 minutos)
   - Generación automática de turnos mensuales
   - Solo días laborables (lunes a viernes)

4. MÓDULO DE REPORTES (interfaz_reportes.py)
   - Informes diarios de turnos por pantalla y en formato txt
   - Informes mensuales de turnos por pantalla y en formato txt
   - Exportación a archivos de texto
   - Ordenamiento cronológico

5. MÓDULO PRINCIPAL (main.py)
   - Coordinación de todos los módulos
   - Menú principal del sistema
   - Creación automática de directorios
   - Manejo de errores globales

REQUISITOS DEL SISTEMA
======================
- Python 3.6 o superior
- Sistema operativo: Windows, Linux o macOS
- Librerías estándar de Python (json, os, re, shutil, datetime)
- Terminal/consola para ejecución

INSTALACIÓN
===========
1. Descargar todos los archivos .py en un directorio
2. Asegurar que Python esté instalado en el sistema
3. No requiere instalación de librerías adicionales

EJECUCIÓN
=========
1. Abrir terminal/consola
2. Navegar al directorio del proyecto
3. Ejecutar: python main.py
4. Seguir las instrucciones del menú

CONFIGURACIÓN INICIAL
=====================
1. Al ejecutar por primera vez, ir a "Configuración y Generación"
2. Seleccionar "Configurar horarios"
3. Definir:
   - Hora de inicio (ej: 8)
   - Hora de fin (ej: 18)
   - Intervalo entre turnos (15, 20 o 30 minutos)
4. Generar turnos del mes deseado

FLUJO DE TRABAJO RECOMENDADO
============================
1. Configurar horarios de atención
2. Generar turnos del mes
3. Registrar pacientes
4. Asignar turnos a pacientes
5. Generar reportes según necesidad

VALIDACIONES IMPLEMENTADAS
===========================
- DNI: 7-8 dígitos numéricos únicos
- Email: formato válido con @ y dominio
- Teléfono: números, espacios, guiones, mínimo 8 dígitos
- Nombres: solo letras y espacios, mínimo 2 caracteres
- Fechas: formato válido y fechas futuras únicamente

ARCHIVOS DE DATOS
=================
Los datos se almacenan en formato JSON en el directorio 'data/':

- pacientes.json: Información de pacientes indexada por DNI
- turnos.json: Turnos disponibles y asignados con ID único
- configuracion.json: Configuración de horarios del consultorio

REPORTES GENERADOS
==================
Los informes se guardan en el directorio 'informes/':

- turnos_dia_DD_MM_AAAA.txt: Reporte diario
- turnos_mes_MM_AAAA.txt: Reporte mensual

FUNCIONALIDADES DESTACADAS
===========================
✓ Interfaz centrada que se adapta al tamaño de terminal
✓ Limpieza automática de pantalla multiplataforma
✓ Manejo robusto de errores y excepciones
✓ Validación exhaustiva de datos de entrada
✓ Navegación intuitiva con opción de cancelar (0)
✓ Confirmaciones para operaciones críticas
✓ Ordenamiento automático de turnos por fecha/hora
✓ Verificación de integridad referencial


MANTENIMIENTO
=============
- Los archivos JSON se crean automáticamente
- Backup recomendado del directorio 'data/'
- Los informes se acumulan en 'informes/'
- No requiere mantenimiento de base de datos

SOLUCIÓN DE PROBLEMAS
=====================
- Si no aparecen turnos: verificar configuración de horarios
- Si error al guardar: verificar permisos de escritura o archivo dañado


CRÉDITOS
========
Desarrollado para UNER - Programación I - TRABAJO FINAL INTEGRADOR - Grupo 38
Año: 2025
Todos los derechos reservados

PARTICIPANTES
=============

Cintia Rios
Adriana Quiroga
Luis Gutiérrez
Gabriel Alejandro Riveiro

CONTACTO Y SOPORTE
==================
Para consultas sobre el sistema, contactar al equipo de desarrollo
del Grupo 38 de Programación I - UNER.

================================================================================
                                FIN DEL DOCUMENTO
================================================================================