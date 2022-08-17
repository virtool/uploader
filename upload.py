import requests
import re
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from auth import authenticate
from logger import logger, UploadStatus
import os


def open_file(path, file_name):
    try:
        return open(os.path.join(path, file_name), "rb")
    except IsADirectoryError:
        return UploadStatus("skipped", f"Directory skipped: {file_name} ", file_name)


def format_params(file_name, file_type):
    return {"name": file_name, "type": file_type}


def upload_file(path, file_name, url, file_type, auth):
    file = open_file(path, file_name)

    if isinstance(file, UploadStatus):
        return file

    encoder = MultipartEncoder(
        {'file': ("helloWorld.txt", file, "application/gzip", {'Expires': '0'})}
    )

    monitor = MultipartEncoderMonitor(encoder, progress_printer(encoder, file_name))

    params = format_params(file_name, file_type)
    headers = {"Content-Type": encoder.content_type}

    result = requests.post(url, data=monitor, auth=auth, params=params, headers=headers)

    if result.status_code == 201:
        return UploadStatus("complete", "Upload complete", file_name)
    else:
        return UploadStatus("failed", "Upload failed", file_name)


def upload_files(file_list, path, api_key, user_handle, url, file_type):
    auth = authenticate(url, user_handle, api_key)

    for file_name in file_list:
        if re.search("\.fq(?:\.gz|\.gzip)$", file_name):
            result = upload_file(path, file_name, url, file_type, auth)
        else:
            result = UploadStatus("skipped", "File skipped, incorrect filetype", file_name)
        logger(result)


LINE_CLEAR = '\x1b[2K'


def progress_printer(encoder, file_name):
    file_length = encoder.len

    def callback(monitor):
        print(f'Uploading "{file_name}": {100*monitor.bytes_read/file_length:.1f}% \r', end="")
        if monitor.bytes_read == file_length:
            print(LINE_CLEAR, end="")

    return callback
