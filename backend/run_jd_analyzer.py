from app.services.jd_service import JDService

def main():
    service = JDService()
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

    print("\nAnalyzing JD...\n")
    result = service.analyze(jd_text)

    print(f"Quality Score: {result.quality_score}/10\n")
    print("Strengths:")
    for s in result.strengths:
        print(f"  + {s}")
    print("\nWeaknesses:")
    for w in result.weaknesses:
        print(f"  - {w}")
    print("\nMissing Elements:")
    for m in result.missing_elements:
        print(f"  - {m}")
    print("\nAmbiguous Phrases:")
    for a in result.ambiguous_phrases:
        print(f"  - \"{a}\"")
    print(f"\nImproved JD:\n{result.improved_jd}")

if __name__ == "__main__":
    main()