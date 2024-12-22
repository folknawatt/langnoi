# วิธีการติดตั้ง
**Install package**
```bash
pip install git+https://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@github.com/folknawatt/langnoi.git#egg=pylangnoi
```

# ตัวอย่าง prompt config
กำหนด table_prompt, query_prompt ซึ่งหากไม่กำหนดจะใช้ default prompt ดังตัวอย่าง
```python
prompt_config = {
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
    "query_prompt" : """Given an input question, create a syntactically correct {dialect} query to run to help find the answer.
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
        """
}
```

# ตัวอย่าง Run.py
กำหนด instance ของ class Langnoi โดยจะมี parameters 4 อย่าง
1. db_uri คือ ลิงก์ uri ของ Database ที่เราจะใช้
2. api_key คือ api key ของโมเดลที่จะใช้
3. model คือ ชื่อโมเดล โดยมีให้ใช้ 2 ตัว คือ gpt-4o-mini และ llama-3.2-90b-vision-preview โดย llama จะเป็นการใช้ API key จาก groq 
4. config  คือ prompt config 

โดยภายใน class ของ Langnoi จะมี medthod ชื่อ query_question 
มี parameter state ไว้รับ question ของผู้ใช้
```python
system_prompt = Langnoi(
    db_uri= "<Database URI>", 
    api_key= "<API KEY>", 
    model= "<Model name>",
    config= "<prompt_config>"
    )

result_table, sql_query = system_prompt.query_question(
    {"question": "<The question you would like to ask about data in your database>"}
)
print(result_table, sql_query)
```