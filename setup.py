import setuptools

PACKAGE_NAME = "vera_gpt"
REQUIRED_PYTHON = ">=3.10.6"
REQUIRED_PACKAGES = [
    "openai>=1.30.2",
    "requests",
    "beautifulsoup4",
    "playwright",
    "brotlipy",
    "html5lib",
]
VERSION = "1.0"

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    python_requires=REQUIRED_PYTHON,
    install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
)
