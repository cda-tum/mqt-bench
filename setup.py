from setuptools import setup
import os

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

setup(
    name="mqt.bench",
    packages=[
        "mqt.benchviewer",
        "mqt.benchviewer.src",
        "mqt.benchviewer.static",
        "mqt.benchviewer.templates",
        "mqt.bench",
        "mqt.bench.utils",
        "mqt.bench.benchmarks",
        "mqt.bench.benchmarks.qiskit_application_finance",
        "mqt.bench.benchmarks.qiskit_application_ml",
        "mqt.bench.benchmarks.qiskit_application_optimization",
        "mqt.bench.benchmarks.qiskit_application_nature",
    ],
    version="0.1.0rc1",
    python_requires=">=3.8",
    license="MIT",
    description="MQT Bench - A MQT tool for Benchmarking Quantum Software Tools",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Nils Quetschlich",
    author_email="nils.quetschlich@tum.de",
    url="https://github.com/cda-tum/mqtbench",
    keywords="mqt quantum benchmarking performance testing",
    entry_points={
        "console_scripts": ["mqt.bench=mqt.benchviewer.main:start_server"],
    },
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=[
        "qiskit~=0.36.0",
        "pytket~=1.2.2",
        "pytket-qiskit~=0.25.0",
        "pandas~=1.3.5",
        "flask~=2.1.2",
        "networkx~=2.8.3",
        "pytest~=7.1.1",
        "qiskit_finance~=0.3.1",
        "qiskit_machine-learning~=0.4.0",
        "qiskit-nature[pyscf]~=0.3.1",
        "qiskit_optimization~=0.3.2",
        "packaging~=21.3",
        "tqdm~=4.64.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)
