def normalize_path(request):
    path = str(request.path) if request.path else ""
    if path == "/":
        return path
    path = path + "/" if path.startswith("/") and not path.endswith("/") else path
    return path
