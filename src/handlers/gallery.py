import json
from src.services.s3_service import generate_upload_url, list_files
from src.utils.response import build_response


def lambda_handler(event, context):
    path = event['resource']
    method = event['httpMethod']

    if path == "/upload-url" and method == "POST":
        body = json.loads(event['body'])
        file_name = body.get("fileName")

        url = generate_upload_url(file_name)
        return build_response(200, {"uploadUrl": url})

    elif path == "/files" and method == "GET":
        files = list_files()
        return build_response(200, {"files": files})

    return build_response(400, {"message": "Invalid request"})