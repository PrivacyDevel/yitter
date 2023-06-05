import json

base_url = "https://twitter.com/i/api/graphql/"

def gen_features_base():
    return {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "blue_business_profile_image_shape_enabled": False,
        "verified_phone_label_enabled": False,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False, # no effect found
        "responsive_web_graphql_timeline_navigation_enabled": False # no effect found
    }

def gen_features_base_ext():
    return gen_features_base() | {
        "longform_notetweets_consumption_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled" : False,
        "tweet_awards_web_tipping_enabled" : False,
        "longform_notetweets_rich_text_read_enabled": False, #TODO consider implementing. Example tweet id: 1649150616063602693

        # this "duplicate" is required for the user_by_screen_name endpoint
        "longform_notetweets_richtext_consumption_enabled": False, # TODO consider implementing. Example tweet id: 1649150616063602693

        "tweetypie_unmention_optimization_enabled": True, # False = unmention_info, True = unmention_data
        "responsive_web_edit_tweet_api_enabled" : False, # edits on twitter?
        "freedom_of_speech_not_reach_fetch_enabled" : False, # no effect found
        "vibe_api_enabled" : False, # no effect found
        "standardized_nudges_misinfo": False, # no effect found
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled" : False, # no effect found
        "interactive_text_enabled": False, # no effect found
        "responsive_web_enhance_cards_enabled" : False, # no effect found
        "responsive_web_text_conversations_enabled" : False, # no effect found
        "rweb_lists_timeline_redesign_enabled": False, # no effect found
        "creator_subscriptions_tweet_preview_api_enabled": False, # no effect found
        "longform_notetweets_inline_media_enabled": True # no effect found
    }

def user_by_screen_name(username):

    variables = {
            "screen_name": username,
    }

    return {"url": base_url + "k26ASEiniqy4eXMdknTSoQ/UserByScreenName", "params": {"variables": json.dumps(variables), "features": json.dumps(gen_features_base())}}

def gen_paged_params(endpoint, variables, cursor, count):

    variables |= {
        "count": count,
        "includePromotedContent": False, # no effect found
        "withVoice" : False # no effect found
    }

    if cursor is not None:
        variables['cursor'] = cursor
    
    features = gen_features_base_ext()

    return {"url": base_url + endpoint, "params": {"variables": json.dumps(variables), "features": json.dumps(features)}}

def likes(user_id, cursor=None, count=20):

    variables = {
        "userId": user_id,
        "withDownvotePerspective": False,
        "withReactionsMetadata": False, # no effect found
        "withReactionsPerspective": False, # no effect found
    }

    return gen_paged_params("fN4-E0MjFJ9Cn7IYConL7g/Likes", variables, cursor, count)

def user_tweets(user_id, cursor=None, count=40):

    variables = {
        "userId" : user_id
    }

    return gen_paged_params("CdG2Vuc1v6F5JyEngGpxVw/UserTweets", variables, cursor, count)

def tweet_detail(tweet_id, cursor=None, count=20):

    variables = {
        "focalTweetId": tweet_id,
        "withBirdwatchNotes": False
    }

    return gen_paged_params("BbCrSoXIR7z93lLCVFlQ2Q/TweetDetail", variables, cursor, count)

def search(query, cursor=None, count=20):

    variables = {
        "rawQuery": query,
        "product": "Latest"
    }

    return gen_paged_params("gkjsKepM6gl_HmFWoWKfgg/SearchTimeline", variables, cursor, count)

def favoriters(tweet_id, cursor=None, count=20):

    variables = {
        "tweetId" : tweet_id
    }

    return gen_paged_params("mDc_nU8xGv0cLRWtTaIEug/Favoriters", variables, cursor, count)

def retweeters(tweet_id, cursor=None, count=20):

    variables = {
        "tweetId" : tweet_id
    }

    return gen_paged_params("RCR9gqwYD1NEgi9FWzA50A/Retweeters", variables, cursor, count)

def following(user_id, cursor=None, count=20):

    variables = {
        "userId" : user_id
    }

    return gen_paged_params("JPZiqKjET7_M1r5Tlr8pyA/Following", variables, cursor, count)

def followers(user_id, cursor=None, count=20):

    variables = {
        "userId" : user_id
    }

    return gen_paged_params("EAqBhgcGr_qPOzhS4Q3scQ/Followers", variables, cursor, count)
