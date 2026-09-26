import os.path



def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        directory_abs_path_norm = os.path.normpath(os.path.join(working_directory_abs_path, directory))

        valid_target_dir = os.path.commonpath([working_directory_abs_path, directory_abs_path_norm]) == working_directory_abs_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory_abs_path_norm):
            return f'Error: "{directory}" is not a directory'

        # Here succeeds the validation
        list_of_items = []
        for item in os.listdir(directory_abs_path_norm):
            item_abs_route = os.path.join(directory_abs_path_norm, item)
            list_of_items.append(f"\t- {item}: file_size={os.path.getsize(item_abs_route)} bytes, is_dir={os.path.isdir(item_abs_route)}")

        return f"Result for current directory:\n{"\n".join(list_of_items)}"
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}