import os
from langchain.document_loaders import DirectoryLoader, JSONLoader, CSVLoader, PyPDFLoader

# Function to create a loader instance based on file type
def create_loader(file_type, relative_path, script_dir=None):
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_path = os.path.join(script_dir) 
    absolute_path = os.path.join(root_path, relative_path)

    if file_type == '.pdf':
        return DirectoryLoader(
            path=absolute_path,
            glob=f"**/*{file_type}",
            loader_cls=PyPDFLoader,
        )
    elif file_type == '.json':
        return JSONLoader(
            file_path=absolute_path,
            jq_schema='.features[]',
            text_content=False
        )
    elif file_type == '.csv':
        return CSVLoader(
            file_path=absolute_path,
            csv_args={
                "delimiter": ";",
                "quotechar": '"',
                "fieldnames": ["place_number", "booking_weezpay_account", "stall_name", "drink_categories", "food_types"],
            },
            encoding="latin-1"
        )
