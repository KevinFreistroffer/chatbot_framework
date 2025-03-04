from setuptools import setup, find_packages

setup(
    name="chatbot_framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.49.0",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "regex>=2023.0.0",
    ],
) 