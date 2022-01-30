def get_big_url(url_key, redis_connect):
    url_key = str(url_key)
    if not url_key.isalnum():
        return "url is invalid", 400
    return redis_connect.get(url_key)


def get_request_url(request):
    form_url = request.form["big_url"]
    body_url = request.get_json(force=True).get("url")
    if form_url is None:
        return body_url
    return form_url
