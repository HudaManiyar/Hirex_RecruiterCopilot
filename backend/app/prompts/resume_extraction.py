RESUME_EXTRACTION_PROMPT = """You are a precise resume parser. Extract structured information from the resume text below.

Rules:
- Return ONLY valid JSON. No markdown fences, no explanation, no preamble.
- If a field is not present in the resume, use null (or an empty list for list fields). Do NOT invent or guess information.
- Every value you output must be traceable to text actually present in the resume below.
- Never infer skills that are not explicitly present. If "Python" is not written anywhere, do not include it.
- If dates are missing, leave total_years_experience null.
- Never guess CGPA if not explicitly stated.
- Never infer or invent projects.

For skills specifically:
- Only extract genuine standalone skills, tools, technologies, or competencies (e.g. "Python", "Project Management", "Crystal Reports").
- Do NOT extract fragments of product names, version numbers, years, or generic words that merely appear near skill-related text (e.g. do not extract "2000" from "PCFS 2000", do not extract "Laser" from "Laser Pro Lending" unless "Laser Pro Lending" itself is the skill).
- If a phrase is a full product/tool name, extract the full name as one skill, not its individual words.
- Deduplicate skills that differ only in casing or whitespace (e.g. "Python" and "python" should appear once).

Return JSON matching exactly this structure:
{schema}

Resume text:
\"\"\"
{resume_text}
\"\"\"

JSON output:"""