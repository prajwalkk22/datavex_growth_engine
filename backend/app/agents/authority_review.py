def authority_review(blog: str):
    print("\n--- AUTHORITY REVIEW REQUIRED ---\n")
    print(blog[:1000])  # preview

    decision = input("\nApprove blog? (yes/no): ").strip().lower()

    return {
        "approved": decision == "yes",
        "reviewer": "human_authority"
    }