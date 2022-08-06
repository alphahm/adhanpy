from setuptools import setup, find_packages

setup(
    name="adhanpy",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="alphahm",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
