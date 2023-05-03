base_url = "https://api.twitter.com/2/"

def likes(userId):
    return {"url": base_url + "timeline/favorites/" + userId + ".json"}

def profile(userId):
    return {"url": base_url + "timeline/profile/" + userId + ".json"}

def search(query):
    return {"url": base_url + "search/adaptive.json", "params": {"q": query}}
