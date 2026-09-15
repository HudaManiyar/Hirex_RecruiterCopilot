# HireX

HireX is an AI-assisted recruiter copilot that helps a recruiter screen resumes against a job description faster, with **explainable, evidence-based grading** instead of an opaque match score. Given a job requirement, it retrieves the closest candidates from a resume pool via semantic search, then has an LLM grade each candidate (A–D), cite specific evidence from the resume, name missing skills, and flag its own confidence — so a recruiter can trust and verify the output rather than take it on faith.

It also includes a job-description quality checker that critiques a JD for vagueness, missing details, and unrealistic requirement combinations, and suggests an improved rewrite.

## How it works

- **Resume parsing** — resumes (PDF) are parsed into structured JSON (skills, experience, education, projects, certifications) via an LLM extraction prompt that is instructed never to invent or infer information not explicitly present in the text.
- **Semantic retrieval** — parsed resumes are embedded (`all-MiniLM-L6-v2`) and stored in a local ChromaDB vector store. A job requirement query retrieves the top-k closest candidates.
- **Explainable ranking** — retrieved candidates are graded A–D by an LLM against the job requirement, with per-candidate evidence, matched/missing skills, a confidence level, and suggested interview questions — never a raw numeric match percentage.
- **JD quality analysis** — a separate LLM pass scores a job description's clarity/completeness, flags ambiguous phrases, and produces an improved rewrite.

## Tech stack

- **Backend:** FastAPI, Google Gemini (`gemini-flash-lite-latest`), ChromaDB, Sentence-Transformers, Pydantic
- **Frontend:** React 19, Vite, Tailwind CSS, React Router

## Project structure

```
backend/    FastAPI app, services, prompts, and resume-processing scripts
frontend/   React + Vite dashboard (rankings, JD analyzer, candidate search)
data/       Raw resumes (by category), parsed JSON, job descriptions, synthetic eval resumes
vector_db/  ChromaDB store (generated, not committed)
```

## Getting started

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env` from `backend/.env.example` and add your Gemini API key:

```
MODEL_NAME=gemini-flash-lite-latest
GEMINI_API_KEY=your_key_here
```

Build the vector store (embeds everything in `data/parsed_json/`), then start the API:

```bash
python build_vector_db.py
uvicorn app.api.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Testing

HireX was validated through qualitative, scenario-based testing rather than a statistical evaluation against a labeled ground truth (which would require multiple recruiters independently grading the same candidates). Test scenarios included:

- A strong, clearly-matching candidate against a real job description → correctly graded A with accurate, traceable evidence
- Candidates with partial skill overlap → correctly graded lower with the specific gap named
- Clearly mismatched candidates (e.g. HR/staffing background against a Backend Engineer role) → correctly graded D with honest, specific reasoning rather than a generic dismissal
- A query with no genuine match in the pool → the system correctly stated no strong match existed rather than inventing a justification
- A deliberately vague or contradictory job description → correctly scored low and flagged specific issues

## Known Limitations

- **No live ATS integration.** HireX operates on a batch of resumes a recruiter already has, not a real-time career-portal feed. This is a scoping decision, not an oversight.
- **Retrieval noise on a small dataset.** A 134-resume pool across 8 categories does not always contain five genuinely close matches for every query; the ranking layer grades honestly but does not eliminate this at the retrieval step.
- **No formal bias audit.** A lightweight fairness check (swapping names and gendered terms across resume pairs and comparing resulting grades) was scoped but not completed. "Explainable" and "fair" are not the same claim, and only the former has been demonstrated here.
- **Free-text experience durations do not parse.** Phrasing like "more than six years" is stored as null rather than guessed at.

## What's Next

- Complete the bias/fairness audit
- Hybrid (keyword + semantic) retrieval to reduce retrieval-stage noise
- Real ATS integration via the existing FastAPI layer
- A larger, labeled evaluation dataset for statistical (not just qualitative) evaluation

## Acknowledgements

Design decisions in this project were informed by an interview with an HR/Talent Acquisition professional regarding real-world resume screening practices, and by an informal review of recruiter discussions in public online recruiting communities.
