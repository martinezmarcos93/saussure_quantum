"""
Setup configuration for Saussure-Quantum Fusion package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="saussure-quantum-fusion",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Fusión computacional entre semiótica saussureana y mecánica cuántica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/saussure-quantum-fusion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black>=21.0", "mypy>=0.910"],
        "quantum": ["qiskit>=0.39.0"],
    },
    include_package_data=True,
    zip_safe=False,
)