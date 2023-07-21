from setuptools import setup

# python setup.py py2app
APP = ["app.py"]
DATA_FILES = []  # Agrega cualquier otro archivo necesario
OPTIONS = {
    "argv_emulation": True,
    "plist": {
        "LSUIElement": True,
    },
    "packages": [],  # Agrega cualquier paquete adicional utilizado en tu_script.py
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
