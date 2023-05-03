base_url = "https://api.twitter.com/1.1/"

def guest_token():
    return {"url": base_url + "guest/activate.json", "method": "post"}

