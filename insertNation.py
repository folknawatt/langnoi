import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
_pathname = os.path.dirname(os.path.abspath(__file__))

def import_sql_file(host, user, password, database, sql_file_path):
    try:
        # เชื่อมต่อกับฐานข้อมูล MySQL
        connection = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

        # สร้าง cursor เพื่อ execute คำสั่ง SQL
        cursor = connection.cursor()

        # เปิดและอ่านไฟล์ .sql
        with open(sql_file_path, "r") as file:
            sql_script = file.read()

        # แยกคำสั่ง SQL ออกเป็นชุด (กรณีมีหลาย statement)
        sql_commands = sql_script.split(";")

        # รันแต่ละคำสั่ง SQL
        for command in sql_commands:
            # ตัดช่องว่างและ whitespace ออก
            command = command.strip()
            if command:
                cursor.execute(command)

        # ยืนยันการเปลี่ยนแปลง
        connection.commit()

        print("Import SQL file สำเร็จ!")

    except mysql.connector.Error as error:
        print(f"เกิดข้อผิดพลาดในการ import: {error}")

    finally:
        # ปิดการเชื่อมต่อ
        if connection.is_connected():
            cursor.close()
            connection.close()


# ตัวอย่างการใช้งาน
host = "mydb"
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database_mock_cp = "Mock_CP_Data"

sql_file_path = os.path.join(_pathname, "scriptdb/Mock_CP_Data.sql")
import_sql_file(host, user, password, database_mock_cp, sql_file_path)
