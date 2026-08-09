from yaml import constructor
from yaml import constructor
import os

def save_generated_tests(filename: str, test_code:str) ->str:
    """
    Saves generated Python unit/integration test code into the 'output_tests/' directory.

    Args:
        filename (str): Name of the file to save (e.g., 'test_pets_api.py').
        test_code (str): The Python Pytest source code string.

    Returns:
        str: Confirmation message indicating where the file was saved.
    """

    output_dir = "output_tests"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(test_code)
        return f"Successfully generated test file: {file_path}"
    except Exception as e:
        return f"Failed to save test file: {str(e)}"