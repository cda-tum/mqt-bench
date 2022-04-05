from setuptools import setup
import os

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

setup(
    name="mqt.bench",
    packages=[
        "mqt.bench",
        "mqt.bench.utils",
        "mqt.bench.benchmarks",
        "mqt.bench.benchmarks.qiskit_application_finance",
        "mqt.bench.benchmarks.qiskit_application_ml",
        "mqt.bench.benchmarks.qiskit_application_optimization",
        "mqt.bench.benchmarks.qiskit_application_nature",
    ],
    version="0.1.16",
    license="MIT",
    description="MQT Bench - A MQT tool for Benchmarking Quantum Software Tools",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Nils Quetschlich",
    author_email="nils.quetschlich@tum.de",
    url="https://github.com/cda-tum/mqtbench",
    download_url="https://github.com/user/reponame/archive/v_01.tar.gz",
    keywords="mqt quantum benchmarking performance testing",
    install_requires=[
        "numpy~=1.22.3",
        "matplotlib~=3.5.1",
        "qiskit~=0.34.1",
        "qiskit-finance~=0.3.1",
        "qiskit-machine-learning==0.3.1",
        "qiskit-nature[pyscf]~=0.3.1",
        "qiskit-optimization~=0.3.1",
        "qiskit-aqua~=0.9.5",
        "pandas~=1.3.5",
        "flask~=2.0.2",
        "networkx~=2.7.1",
        "pytest~=7.1.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
)
