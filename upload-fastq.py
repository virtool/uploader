import click
from upload import upload_files
import os


def main(path, api_key, user_handle, url, file_type):
    try:
        file_list = os.listdir(path)
    except FileNotFoundError:
        print("Directory not found, check path and try again")
        exit(1)

    upload_files(file_list, path, api_key, user_handle, url, file_type)


valid_file_types = ["hmm", "reference", "reads", "subtraction"]


@click.command()
@click.option("--path", "-p", help="Target file directory", required=True)
@click.option("--api-key", "-k", help="api-key", required=True)
@click.option("--user-handle", "-h", help="Users handle corresponding to the provided api key", required=True)
@click.option("--url", "-u", help="target virtool host url", required=True)
@click.option("--file-type", "-t", help=f"File type to be uploaded. Valid types: {valid_file_types}", required=True)
def config(path, api_key, user_handle, url, file_type):
    if file_type not in valid_file_types:
        print(f'Invalid value for --read-type, valid values are: {valid_file_types}')
    main(path, api_key, user_handle, url, file_type)


if __name__ == "__main__":
    config(auto_envvar_prefix='VT_UPLOAD')
