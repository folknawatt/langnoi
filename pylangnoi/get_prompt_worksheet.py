import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_worksheet(spreadsheet_name: str, key_file: str, sheet_name: str = None):
    """
    Fetches a worksheet and converts it to a Pandas DataFrame.

    Args:
        spreadsheet_name (str): The name of the Google Sheet.
        key_file (str): Path to the JSON key file for authentication.
        sheet_name (str, optional): The name of the worksheet. Defaults to None.

    Returns:
        pd.DataFrame: Data from the worksheet as a Pandas DataFrame.
    """
    try:
        # Set up the scope and credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open(spreadsheet_name)
        if sheet_name:
            worksheet = spreadsheet.worksheet(sheet_name)
            print(f"Read worksheet '{sheet_name}' successfully.")
        else:
            worksheets = spreadsheet.worksheets()
            if len(worksheets) == 1:
                worksheet = worksheets[0]
                print(f"Single worksheet '{worksheet.title}' found. Using it.")
            else:
                print("Available Worksheets:")
                for idx, sheet in enumerate(worksheets, start=1):
                    print(f"{idx}: {sheet.title}")
                while True:
                    try:
                        user_choice = int(input("Enter the number of the worksheet you want to access: "))
                        worksheet = worksheets[user_choice - 1]
                        print(f"Read worksheet '{worksheet.title}' successfully.")
                        break
                    except (IndexError, ValueError):
                        print("Invalid choice. Please enter a valid number.")

        return worksheet

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Spreadsheet '{spreadsheet_name}' not found.")
    except FileNotFoundError:
        print(f"Key file '{key_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    spreadsheet_name = "Botnoi Langchain"
    sheet_name = "Prompt_warehouse"
    api_key = "secretKey.json"

    sheet = get_worksheet(spreadsheet_name, sheet_name, api_key)
    sheet