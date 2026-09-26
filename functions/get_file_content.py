import os.path

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path_norm = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        valid_target_file = os.path.commonpath(
            [working_directory_abs_path, file_abs_path_norm]) == working_directory_abs_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs_path_norm):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs_path_norm) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Reads the content and truncates it if it is longer than {MAX_CHARS} characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}