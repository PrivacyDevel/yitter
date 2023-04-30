
base_url = "https://api.twitter.com/2/"

def likes(userId, headers):
    return {"url": base_url + "timeline/favorites/" + userId + ".json", "headers": headers}

def profile(userId, headers):
    return {"url": base_url + "timeline/profile/" + userId + ".json", "headers": headers}
