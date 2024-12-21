import setuptools
import re
import os

# path = os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), "pydatacraft", "__init__.py"
# )
# with open(path, "r") as f:
#     version_file_content = f.read()
# try:
#     version = re.findall(r"^__version__ = '([^']+)'\r?$", version_file_content, re.M)[0]
# except IndexError:
#     raise RuntimeError("Unable to determine version")

setuptools.setup(
    name="langnoi",
    author="langnoi dev team",
    author_email="devteam@langnoi.com",
    description="Langnoi Python Pacakge",
    license="MIT License",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=[
        # "faker",
        # "gensim",
        # "scipy==1.12.0",
        # "pandas",
        # "REaLTabFormer",
        # "openai",
        # "python-dotenv",
        # "seaborn",
        # "ray[default,train,data]",
        # "werkzeug",
        # "python-jose[cryptography]",
        # "pycryptodome==3.14.1",
    ],
)
