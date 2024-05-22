from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": [],
    "zip_include_packages": [],
}

setup(
    name="HYStream",
    version="1.0",
    description="Aio stream assets extraction solution for some specific anime games",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui", icon="./resources/images/favicon.ico")],
)
