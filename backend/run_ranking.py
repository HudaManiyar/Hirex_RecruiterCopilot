from app.services.ranking_service import RankingService

def main():
    service = RankingService()
    job_requirement = input("Enter job requirement: ").strip()

    print("\nEvaluating candidates...\n")
    result = service.rank(job_requirement, top_k=5)

    for ev in result.evaluations:
        print(f"\n{'='*60}")
        print(f"Candidate: {ev.candidate_name} ({ev.source_file})")
        print(f"Grade: {ev.grade}  |  Confidence: {ev.confidence}")
        print(f"Matched Skills: {', '.join(ev.matched_skills)}")
        print(f"Missing Skills: {', '.join(ev.missing_skills)}")
        print(f"Evidence:")
        for e in ev.evidence:
            print(f"  - {e}")
        print(f"Reasoning: {ev.reasoning}")
        print(f"Suggested Interview Questions:")
        for q in ev.suggested_interview_questions:
            print(f"  - {q}")

if __name__ == "__main__":
    main()