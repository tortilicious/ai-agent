import os.path

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path_norm = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        valid_target_file = os.path.commonpath(
            [working_directory_abs_path, file_abs_path_norm]) == working_directory_abs_path

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_abs_path_norm):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(file_abs_path_norm), exist_ok=True)

        with open(file_abs_path_norm, mode="w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content into a file, replacing its prior content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text that replaces the prior content of the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}