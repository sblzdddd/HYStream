from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": [],
    "zip_include_packages": ["PySide6"],
}

setup(
    name="HYStream",
    version="1.0",
    description="Ningzheng is Gae",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui", icon="./resources/images/favicon.ico")],
)
