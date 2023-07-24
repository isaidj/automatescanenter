import sys
from cx_Freeze import setup, Executable

# Reemplaza 'nombre_del_script.py' con el nombre de tu script principal
script_file = "socketServer.py"

# Opciones de configuración para el ejecutable
build_exe_options = {
    "packages": [],  # Lista de paquetes a incluir
    "excludes": [],  # Lista de módulos o paquetes para excluir
    "include_files": [],  # Lista de archivos adicionales a incluir
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Si es una aplicación GUI de Windows

# Define el ejecutable
executables = [Executable(script_file, base=base)]

# Configuración para crear el ejecutable
setup(
    name="App",  # Nombre de la aplicación
    version="1.0",  # Versión de la aplicación
    description="Descripción de la aplicación",  # Descripción de la aplicación
    options={
        "build_exe": build_exe_options,
    },
    executables=executables,
)
