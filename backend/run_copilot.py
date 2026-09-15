from app.services.recruiter_copilot import RecruiterCopilot


def main():
    copilot = RecruiterCopilot()
    print("Recruiter Copilot ready. Type a query (or 'quit' to exit).\n")

    while True:
        query = input("Recruiter query: ").strip()
        if query.lower() in ("quit", "exit"):
            break
        if not query:
            continue

        print("\nSearching and generating response...\n")
        answer = copilot.query(query)
        print(answer)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()