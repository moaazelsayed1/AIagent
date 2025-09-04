import os

def get_files_info(working_directory, directory="."):
    # print(os.listdir(working_directory))
    # print(os.path.abspath(directory))
    # print(os.path.abspath(directory).split('/')[-1])
    abs_path = os.path.abspath(directory)
    working_directory_content = os.listdir(working_directory)
    formatted_content = "Result for current directory:\n" if directory == "." else f"Result for '{directory}' directory:\n"
    print(formatted_content)

    # print("CONTENT", working_directory_content)
    # print(os.path.abspath(working_directory+ '/' +directory))
    if directory != '.' and abs_path.split('/')[-1] not in working_directory_content:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    directory = os.path.abspath(working_directory+ '/' +directory)
    if not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'

    return content_format(directory)


def content_format(directory):
    directory_content = os.listdir(directory)
    formatted_content = ''

    for file in directory_content:
        full_path = os.path.join(directory, file)
        formatted_content += (
            f"- {file}: file_size={os.path.getsize(full_path)}, "
            f"is_dir={os.path.isdir(full_path)}\n"
        )

    return formatted_content
