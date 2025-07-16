from setuptools import setup, find_packages

setup(
    name="pq-swarm-c2",
    version="0.1.0",
    description="Post-Quantum Swarm C2 Reference Implementation",
    author="Галиев Артур",
    author_email="Tarzanchik.84@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pqcrypto",
        "networkx",
    ],
    python_requires=">=3.8",
)
