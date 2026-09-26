import os.path
import subprocess


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        file_abs_path_norm = os.path.normpath(os.path.join(working_directory_abs_path, file_path))

        valid_target_file = os.path.commonpath(
            [working_directory_abs_path, file_abs_path_norm]) == working_directory_abs_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_abs_path_norm):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_abs_path_norm.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_abs_path_norm]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_directory_abs_path, capture_output=True, text=True,
                                           timeout=30)
        output = []

        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stderr and not completed_process.stdout:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR: {completed_process.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a .py file and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments to pass to the .py script",
                },
            },
            "required": ["file_path"],
        },
    },
}