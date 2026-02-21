from backend.app.linkedin_poster import post_to_linkedin

def approval_and_publish(post_text: str):
    decision = input("\nApprove blog? (yes/no): ").strip().lower()

    if decision == "yes":
        print("🚀 Approved. Posting to LinkedIn...")
        post_to_linkedin(post_text)
        print("✅ Posted successfully.")
    else:
        print("❌ Rejected. Not posting.")