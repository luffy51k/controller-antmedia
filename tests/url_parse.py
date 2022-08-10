from urllib import parse

uri = "/0ab1aa2f098b4350b88fdf2183cc780a/websocket?stream_name=3af0c1cc49ce4e42b80ba607827eb72c&token=nuwriBjvsF"

params = parse.urlsplit(uri)
print(params.query)