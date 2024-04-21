import os
import shutil
from distutils.core import setup
from distutils.extension import Extension

from Cython.Build import cythonize

# Define your Cython modules here
extensions = [
    Extension("pck_lib", ["pck_lib.pyx"]),
    # Add more extensions if you have multiple Cython modules
]

setup(
    ext_modules=cythonize(extensions)
)


# Clean up generated files and directories after building
def clean():
    # Remove generated .c files
    for extension in extensions:
        if os.path.exists(extension.name + ".c"):
            os.remove(extension.name + ".c")

    # Remove the build directory
    build_dir = os.path.join(os.getcwd(), "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)


# Call the clean function
if __name__ == "__main__":
    clean()
