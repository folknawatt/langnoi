import setuptools

setuptools.setup(
    name="pylangnoi",
    author="langnoi dev team",
    author_email="devteam@langnoi.com",
    description="Langnoi Python Pacakge",
    license="MIT License",
    version="0.1.7",
    packages=setuptools.find_packages(),
    install_requires=[
        "langchain-community",
        "langchainhub",
        "langgraph",
        "mysql-connector-python",
        "langchain_openai",
        "langchain-groq",
        "openpyxl",
        "python-dotenv",
        "pymysql",
        "cryptography",
        "oauth2client",
        "gspread",
    ],
)
