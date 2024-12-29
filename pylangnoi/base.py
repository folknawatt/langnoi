from typing import List
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from pylangnoi.classmodel import State, Table, QueryOutput
from pylangnoi.baseprompt import table_prompt, query_prompt

class Langnoi:
    """
    Langnoi is a class designed to connect a Language Model with the capability to retrieve data from a database.

    **Attributes:**

    - `db_uri`: A string representing the URI of the database.
    - `api_key`: A string representing the API Key for the Language Model.
    - `model`: A string representing the name of the language model in use.
    - `table_prompt` and `query_prompt`: Special values from the configuration defined for specific problems and questions.
    """
    def __init__(self, db_uri: str, api_key: str, model: str, **config: dict):
        self.db_uri = db_uri
        self.api_key = api_key
        self.model = model
        self.table_prompt = f"""{config.get("table_prompt")}"""
        self.query_prompt = config["query_prompt"] if "query_prompt" in config.keys() else query_prompt

        # เชื่อม model
        if self.model == "gpt-4o-mini":
            self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=self.api_key)
        else:
            self.llm = ChatGroq(model=self.model, api_key=self.api_key)

    def query_question(self, state: State):
        """Generate SQL query to fetch information."""
        llm_with_tools = self.llm.bind_tools([Table])
        output_parser = PydanticToolsParser(tools=[Table])

        # Database ที่ใช้
        db = SQLDatabase.from_uri(self.db_uri)

        dialect = db.dialect
        top_k = 10
        input = state["question"]

        # # Defualt table_prompt #################################################################################
        # if self.table_prompt :
        #     try:
        #         # Fetch table names and construct the default table prompt
        #         table_names = "\n".join(db.get_usable_table_names())
        #         self.table_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question.\n
        #             The tables are:\n

        #             {table_names}

        #             Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

        #     except Exception as e:
        #         # Handle potential errors in fetching table names
        #         raise RuntimeError("Failed to fetch usable table names.") from e
        # ########################################################################################################
        prompt_table = ChatPromptTemplate.from_messages(
            [
                ("system", self.table_prompt),
                ("human", "{question}"),
            ]
        )

        category_chain = prompt_table | llm_with_tools | output_parser

        def get_tables(categories: List[Table]) -> List[str]:
            tables = []
            for category in categories:
                tables.append(category.name)
            return tables

        table_chain = category_chain | get_tables
        table_answer = table_chain.invoke(input)

        table_info = db.get_table_info(table_answer)

        query_prompt = self.query_prompt.format(
            input = input,
            top_k = top_k,
            dialect = dialect,
            table_info = table_info,
            
        )

        structured_llm = self.llm.with_structured_output(schema=QueryOutput)
        result = structured_llm.invoke(query_prompt)
        query_result = result["query"].replace("`", '"')
        return table_answer, {"query": query_result}
