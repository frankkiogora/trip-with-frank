import json
from src.services.s3_service import generate_upload_url, generate_view_url, list_files
from src.utils.response import build_response


def lambda_handler(event, context):
    print("EVENT:", json.dumps(event))

    path = event.get("resource")
    method = event.get("httpMethod")

    if path == "/upload-url" and method == "POST":
        try:
            body = event.get("body")

            if isinstance(body, str):
                body = json.loads(body)
            elif body is None:
                body = {}

            file_name = body.get("fileName")

            if not file_name:
                return build_response(400, {"message": "fileName is required"})

            url = generate_upload_url(file_name)
            return build_response(200, {"uploadUrl": url})

        except Exception as e:
            print("ERROR generating upload URL:", str(e))
            raise

    if path == "/files" and method == "GET":
        try:
            files = list_files()
            return build_response(200, {"files": files})

        except Exception as e:
            print("ERROR listing files:", str(e))
            raise

    if path == "/file/{key}" and method == "GET":
        try:
            path_params = event.get("pathParameters") or {}
            file_name = path_params.get("key")

            if not file_name:
                return build_response(400, {"message": "file key is required"})

            url = generate_view_url(file_name)
            return build_response(200, {"viewUrl": url})

        except Exception as e:
            print("ERROR generating view URL:", str(e))
            raise

    return build_response(400, {"message": "Invalid request"})
