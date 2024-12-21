from typing import List
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from classmodel import State, Table, QueryOutput


class Langnoi:

    def __init__(self, config: dict):
        self.db_url = config["db_url"] if "db_url" in config.keys() else "mysql+mysqlconnector://root:root@localhost:3306/Mock_CP_Data"
        self.apikey = config["apikey"]
        self.table_prompt = config["table_prompt"]
        self.query_prompt = config["query_prompt"]

        # เชื่อม model
        self.llm = ChatGroq(
            model="llama-3.2-90b-vision-preview",
            api_key=self.apikey,
        )

    def chain_table(self, state: State):
        """Generate SQL query to fetch information."""
        llm_with_tools = self.llm.bind_tools([Table])
        output_parser = PydanticToolsParser(tools=[Table])

        # Database ที่ใช้
        db = SQLDatabase.from_uri(self.db_url)

        dialect = db.dialect
        top_k = 10
        input = state["question"]

        # system = """Return the names of any SQL tables in MySQL that are relevant to the user question.
        # The tables are:

        # "name": "Products"
        # "description": "The Products table stores information about the products available in inventory, including Product_ID, Product_Name, Quantity, and Price."

        # "name": "Branches"
        # "description": "The Branches table stores information about different branches, including Branch_ID and Branch_Name."

        # "name": "Employees"
        # "description": "The Employees table stores information about employees, including Employee_ID, Employee_Name, and the Branch_ID where they are assigned."

        # "name": "Sales"
        # "description": "The Sales table records information about product sales, including Sales_ID, Product_ID (linked to Products.Product_ID), Branch_ID (linked to Branches.Branch_ID), Employee_ID (linked to Employees.Employee_ID), Total_Sales, Sales_By_Branch, Sales_By_Employee, and Total_Sales_Amount."

        # "name": "Profits"
        # "description": "The Profits table contains information about profits made from product sales, including Product_ID (linked to Products.Product_ID), Branch_ID (linked to Branches.Branch_ID), Employee_ID (linked to Employees.Employee_ID), Total_Profit, Profit_By_Branch, and Profit_By_Employee."

        # Column Relationships:
        # 1. Sales.Product_ID < Products.Product_ID
        # 2. Sales.Branch_ID < Branches.Branch_ID
        # 3. Sales.Employee_ID < Employees.Employee_ID
        # 4. Profits.Product_ID < Products.Product_ID
        # 5. Profits.Branch_ID < Branches.Branch_ID
        # 6. Profits.Employee_ID < Employees.Employee_ID
        # 7. Employees.Branch_ID < Branches.Branch_ID

        # Remember to include ALL POTENTIALLY RELEVANT tables."""

        prompt_table = ChatPromptTemplate.from_messages(
            [
                ("system", self.table_prompt),
                ("human", "{question}"),
            ]
        )

        category_chain = prompt_table | llm_with_tools | output_parser
        # table = category_chain.invoke(input)

        def get_tables(categories: List[Table]) -> List[str]:
            # [Table(name='countries')] -> ['countries']
            tables = []
            for category in categories:
                tables.append(category.name)
            return tables

        table_chain = category_chain | get_tables
        table_answer = table_chain.invoke(input)

        table_info = db.get_table_info(table_answer)

        # prompt = f"""Given an input question, create a syntactically correct {dialect} query to run to help find the answer.
        # Unless the user specifies in his question a specific number of examples they wish to obtain, always limit
        # your query to at most {top_k} results. You can order the results by a relevant column to return the most
        # interesting examples in the database.

        # Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

        # Pay attention to use only the column names that you can see in the schema description. Be careful to not
        # query for columns that do not exist. Also, pay attention to which column is in which table.

        # Only use the following tables:{table_info}
        # Question: {input}
        
        # For example:
        # Input: สาขาไหน และพนักงานคนไหนขายน้ำมันหอย กำไรสูงสุด
        # Expected Output: 
        # """
        
        query_prompt = self.query_prompt.format(
            input = input,
            top_k = top_k,
            dialect = dialect,
            table_info = table_info,
            
        )

        structured_llm = self.llm.with_structured_output(schema=QueryOutput)
        result = structured_llm.invoke(query_prompt)
        return table_answer, {"query": result["query"]}


if __name__== "__main__":

    system_prompt = {
        "apikey": "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",
        "table_prompt": """Return the names of any SQL tables in MySQL that are relevant to the user question.
        The tables are:

        "name": "Products"
        "description": "The Products table stores information about the products available in inventory, including Product_ID, Product_Name, Quantity, and Price."

        "name": "Branches"
        "description": "The Branches table stores information about different branches, including Branch_ID and Branch_Name."

        "name": "Employees"
        "description": "The Employees table stores information about employees, including Employee_ID, Employee_Name, and the Branch_ID where they are assigned."

        "name": "Sales"
        "description": "The Sales table records information about product sales, including Sales_ID, Product_ID (linked to Products.Product_ID), Branch_ID (linked to Branches.Branch_ID), Employee_ID (linked to Employees.Employee_ID), Total_Sales, Sales_By_Branch, Sales_By_Employee, and Total_Sales_Amount."

        "name": "Profits"
        "description": "The Profits table contains information about profits made from product sales, including Product_ID (linked to Products.Product_ID), Branch_ID (linked to Branches.Branch_ID), Employee_ID (linked to Employees.Employee_ID), Total_Profit, Profit_By_Branch, and Profit_By_Employee."

        Column Relationships:
        1. Sales.Product_ID < Products.Product_ID
        2. Sales.Branch_ID < Branches.Branch_ID
        3. Sales.Employee_ID < Employees.Employee_ID
        4. Profits.Product_ID < Products.Product_ID
        5. Profits.Branch_ID < Branches.Branch_ID
        6. Profits.Employee_ID < Employees.Employee_ID
        7. Employees.Branch_ID < Branches.Branch_ID

        Remember to include ALL POTENTIALLY RELEVANT tables.""",
        "query_prompt": """Given an input question, create a syntactically correct {dialect} query to run to help find the answer.
        Unless the user specifies in his question a specific number of examples they wish to obtain, always limit
        your query to at most {top_k} results. You can order the results by a relevant column to return the most
        interesting examples in the database.

        Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

        Pay attention to use only the column names that you can see in the schema description. Be careful to not
        query for columns that do not exist. Also, pay attention to which column is in which table.

        Only use the following tables:{table_info}
        Question: {input}
        
        For example:
        Input: สาขาไหน และพนักงานคนไหนขายน้ำมันหอย กำไรสูงสุด
        Expected Output: 
        
        """,
    }

    system = Langnoi(system_prompt)
    result_table, sql_query = system.chain_table({"question": "Show all data of Product table"})
    print(result_table, sql_query)
