def gen_headers_base():
    return {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
    }

def gen_authenticated_headers_base(auth):
    return gen_headers_base() | {
        "x-csrf-token": auth['ct0'],
        "Cookie": f"ct0={auth['ct0']}; auth_token={auth['auth_token']}",
    }
