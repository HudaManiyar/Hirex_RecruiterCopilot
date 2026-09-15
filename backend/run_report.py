from app.services.report_service import ReportService

def main():
    service = ReportService()
    print("Paste the job description, then press Enter twice when done:\n")

    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)

    jd_text = "\n".join(lines).strip()
    if not jd_text:
        print("No JD provided.")
        return

    print("\nGenerating full recruiter report...\n")
    report = service.generate_report(jd_text, top_k=5)

    jd = report["jd_analysis"]
    print("=" * 70)
    print("JOB DESCRIPTION QUALITY ANALYSIS")
    print("=" * 70)
    print(f"Quality Score: {jd.quality_score}/10\n")
    if jd.weaknesses:
        print("Weaknesses:")
        for w in jd.weaknesses:
            print(f"  - {w}")
    if jd.quality_score < 6:
        print(f"\nNote: JD quality is low. Candidate matching below may be less reliable")
        print(f"since the requirement itself is ambiguous. Consider using the improved JD.")

    print("\n" + "=" * 70)
    print("TOP CANDIDATES")
    print("=" * 70)
    for i, ev in enumerate(report["candidate_evaluations"], start=1):
        print(f"\n[{i}] {ev.candidate_name} ({ev.source_file}) — Grade: {ev.grade} | Confidence: {ev.confidence}")
        print(f"    Matched: {', '.join(ev.matched_skills) if ev.matched_skills else 'None'}")
        print(f"    Missing: {', '.join(ev.missing_skills) if ev.missing_skills else 'None'}")
        print(f"    Reasoning: {ev.reasoning}")

if __name__ == "__main__":
    main()