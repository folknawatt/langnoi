# วิธีการติดตั้ง
**Clone the Repository**
```bash
    pip install git+https://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@github.com/folknawatt/langnoi.git#egg=pylangnoi
```

# Run.py
```python
    system_prompt = Langnoi(
        db_uri= "<Database URI>", 
        api_key= "<API KEY>", 
        model= "<Model name>",
        )

    result_table, sql_query = system_prompt.chain_table(
        {"question": "<The question you would like to ask about data in your database>"}
    )
    print(result_table, sql_query)
```