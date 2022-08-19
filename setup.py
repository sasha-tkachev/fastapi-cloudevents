from pathlib import Path
import setuptools


def _read_requirements(filename):
    return [
        line.strip()
        for line in Path(filename).read_text().splitlines()
        if not line.startswith("#")
    ]


setuptools.setup(
    name="fastapi-cloudevents",
    version="1.0.0",
    author="Alexander Tkachev",
    author_email="sasha64sasha@gmail.com",
    description="FastAPI plugin for CloudEvents Integration",
    url="https://github.com/sasha-tkachev/fastapi-cloudevents",
    keywords=[
        "fastapi",
        "cloudevents",
        "ce",
        "cloud",
        "events",
        "event",
        "middleware",
        "rest",
        "rest-api",
        "plugin",
        "pydantic",
        "fastapi-extension"
    ],
    packages=setuptools.find_packages(),
    install_requires=_read_requirements("requirements.txt"),
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
