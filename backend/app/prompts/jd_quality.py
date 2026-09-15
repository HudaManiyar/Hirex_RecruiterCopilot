JD_QUALITY_PROMPT = """You are an expert recruitment consultant reviewing a job description (JD) for clarity, completeness, and effectiveness.

Evaluate the JD below and provide a structured critique.

Rules:
- quality_score: a score from 0-10 reflecting overall JD quality (10 = excellent, clear, complete).
- strengths: what the JD does well, if anything.
- weaknesses: specific problems (e.g. too vague, missing seniority level, unrealistic combination of requirements).
- missing_elements: concrete elements a good JD should have but this one lacks (e.g. "years of experience", "required vs preferred skills distinction", "salary range", "location/remote policy", "team size or reporting structure").
- ambiguous_phrases: specific vague phrases pulled directly from the JD that could confuse candidates or produce poor-quality applicants (e.g. "rockstar developer", "fast-paced environment", "wear many hats").
- improved_jd: a rewritten, improved version of the JD that fixes the identified issues. Keep the core intent/role the same, just make it clearer, more specific, and more complete. Invent reasonable specifics only where necessary for illustration (e.g. suggested experience range), and clearly note in weaknesses if you had to do this.

Return ONLY valid JSON matching this structure:
{schema}

Job description to evaluate:
\"\"\"
{jd_text}
\"\"\"

JSON output:"""