---
name: resume-checker
description: >
  Analyze a resume against a job description and generate a professional report with match score, gap analysis,
  and rewrite suggestions. Use this skill whenever a user wants to check, review, evaluate, or optimize their
  resume for a specific job posting. Also trigger when a user mentions "resume check", "resume review", "resume
  score", "JD match", "ATS check", "resume feedback", "how does my resume look", "improve my resume for this
  job", "resume gap analysis", or any request comparing a resume to a job description — even if they don't
  explicitly say "resume checker".
---

# Resume Checker

Analyze a resume against a job description and produce a detailed report with a match score, dimensional analysis, and actionable rewrite suggestions.

## Inputs

The user provides two things:

1. **Job Description (JD)** — as text, a URL, a file, or pasted content
2. **Resume** — as a PDF, DOCX, or pasted text

If either is missing, ask for it before proceeding. If the JD is a URL, fetch and extract the relevant content. If the resume is a PDF/DOCX, extract the text.

## Analysis Framework

Run all five dimensions below. Each dimension gets a status (PASS / NEEDS WORK / MISSING) and specific findings.

### 1. Content

Check whether resume bullet points are impactful and error-free.

**Measurable Results:** Flag bullet points that lack quantifiable outcomes. Vague descriptions like "managed a team" or "improved processes" should be flagged with a suggestion to add numbers, percentages, timeframes, or scale. Good bullets include specifics like "reduced pipeline latency by 40%" or "processed 2M+ records daily."

**Spelling & Grammar:** Identify any spelling mistakes, grammatical errors, awkward phrasing, or inconsistent tense. Pay special attention to the summary/objective statement — it's the first thing recruiters read and sets the tone.

### 2. Skills

Compare skills mentioned in the JD against skills present in the resume. This is the core keyword-gap analysis that determines ATS compatibility.

**Hard Skills:** Extract every technical skill, tool, framework, methodology, and technology from the JD. For each, note:
- Whether it appears in the resume (matched or missing)
- Whether the JD marks it as required or preferred
- Count of mentions in JD vs resume

Present as a table with columns: Skill | Required/Preferred | In JD | In Resume | Status (match/gap)

**Soft Skills:** Same approach for soft skills (communication, collaboration, leadership, etc.). These are less critical for ATS but still matter for human reviewers.

### 3. Format

Check structural quality that affects both readability and ATS parsing.

- **Date Formatting:** Are dates consistent throughout? (e.g., don't mix "Jan 2024" with "2024/01" with "January 2024")
- **Resume Length:** Is the length appropriate for experience level? (1 page for <10 years, up to 2 pages for more)
- **Bullet Points:** Are bullets clear, concise, and action-verb-led? Flag bullets that are too long (>2 lines) or too vague.

### 4. Sections

Verify the resume contains all standard sections a recruiter and ATS expect:

- Name ✓/✗
- Job Title ✓/✗
- Phone Number ✓/✗
- Email Address ✓/✗
- Portfolio or Website Link ✓/✗
- Summary/Objective ✓/✗
- Work Experience ✓/✗
- Education ✓/✗
- Hard Skills ✓/✗
- Soft Skills ✓/✗

### 5. Style

Check tone alignment and language quality.

**Voice:** Analyze the JD's tone (e.g., professional, collaborative, innovative, technical) and check if the resume's language matches. Flag mismatches — for example, a startup-culture JD paired with overly formal corporate language, or vice versa.

**Buzzwords & Cliches:** Flag overused phrases that weaken impact: "results-driven", "team player", "go-getter", "synergy", "passionate about", etc. These add noise without signal.

## Match Score

Calculate an overall match score (0–100) based on weighted dimensions:

| Dimension | Weight |
|-----------|--------|
| Skills    | 40%    |
| Content   | 25%    |
| Style     | 15%    |
| Sections  | 10%    |
| Format    | 10%    |

The Skills dimension dominates because keyword matching is what gets a resume past ATS filters. The formula:

- **Skills sub-score:** (matched required skills / total required skills) × 70 + (matched preferred skills / total preferred skills) × 30
- **Content sub-score:** Based on ratio of bullets with measurable results and absence of errors
- **Style sub-score:** Voice alignment + absence of cliches
- **Sections sub-score:** Proportion of expected sections present
- **Format sub-score:** Date consistency + appropriate length + bullet quality

Final score = weighted sum, rounded to nearest integer.

## Output Structure

Generate two files:

### 1. Markdown Report (`resume-checker-report.md`)

Use this structure:

```
# Resume Checker Report

## Overview

**Match Score: [score]/100**

[2-3 sentence summary of overall fit]

### Highlights
- [Top 3 strengths as bullet points]

### Key Improvements
- [Top 3 most impactful improvements needed]

---

## 1. Content

**Status: [PASS / NEEDS WORK]**

### Measurable Results
[Count] bullet points lack quantifiable impact.

[For each flagged bullet, show:]
> [Original bullet text]
> → Suggestion: [Rewritten version with measurable result]

### Spelling & Grammar
[Count] issues found.

[For each issue, show:]
> [Original text] → [Issue description and fix]

---

## 2. Skills

**Status: [PASS / NEEDS WORK]**

### Hard Skills

| Skill | Required/Preferred | In JD | In Resume | Status |
|-------|-------------------|-------|-----------|--------|
| ...   | Required          | 1     | 0         | ✗ Gap  |
| ...   | Required          | 1     | 1         | ✓ Match|

### Soft Skills

[Same table format]

### Suggestions
[For each missing required skill, suggest where and how to incorporate it — which bullet point could be reworded, or which experience could highlight it]

---

## 3. Format

**Status: [PASS / NEEDS WORK]**

- Date Formatting: [PASS/FAIL + details]
- Resume Length: [PASS/FAIL + details]
- Bullet Points: [PASS/FAIL + details]

---

## 4. Sections

**Status: [PASS / NEEDS WORK]**

[Checklist of expected sections with ✓/✗]

---

## 5. Style

**Status: [PASS / NEEDS WORK]**

### Voice
JD tone: [detected tone tags, e.g., #professional #collaborative #innovative]
[Findings and suggestions]

### Buzzwords & Cliches
[PASS or list of flagged phrases with alternatives]

---

## Rewrite Suggestions

### Summary/Objective
**Original:** [current summary]
**Suggested:** [rewritten summary tailored to the JD]

### Bullet Point Rewrites
[For each bullet that needs improvement, show before/after with explanation]

| # | Original | Suggested Rewrite | Why |
|---|----------|-------------------|-----|
| 1 | ...      | ...               | ... |
```

### 2. PDF Report

After generating the markdown, convert it to a well-formatted PDF using reportlab. The PDF should include:

- A clear header with "Resume Checker Report" and the date
- The match score prominently displayed
- Color-coded status indicators (green for PASS, amber for NEEDS WORK, red for MISSING)
- Clean tables for the skills comparison
- The rewrite suggestions section

Use the `scripts/generate_report_pdf.py` script to produce the PDF. Read it before running — it handles the layout, colors, and table formatting.

## Workflow

1. Extract text from both JD and resume (handle PDF/DOCX/URL/text)
2. Run all 5 dimension analyses
3. Calculate the match score
4. Generate the rewrite suggestions (summary + weak bullets)
5. Write the markdown report
6. Generate the PDF report using the script
7. Present both files to the user

## Important Notes

- Be objective and constructive. The goal is to help the user improve, not to discourage them.
- A score below 50 doesn't mean the resume is bad — it means it's not well-tailored to this specific JD.
- When suggesting rewrites, preserve the candidate's authentic experience. Don't fabricate achievements. Reframe and highlight what's already there.
- The skill gap table is the single most actionable section. Make it thorough.
- Keep the report language professional but approachable — imagine you're a career coach, not a judge.
