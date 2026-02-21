def publish_social_assets(blog: str, strategy):
    linkedin_post = blog[:300] + "\n\n#RevOps #AI #DataVex"
    twitter_thread = [
        blog[:240],
        blog[240:480],
        "Full article 👇"
    ]

    return {
        "linkedin": linkedin_post,
        "twitter": twitter_thread,
        "status": "ready_to_post"
    }