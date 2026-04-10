# Resume Checker

**Analyze your resume against any job description**

A comprehensive resume analysis tool that evaluates how well your resume matches a job posting using a 5-dimensional analysis: Content, Skills, Format, Sections, and Style.

## What It Does

- **Match Score (0–100)** based on weighted dimensions
- **Skills Gap Analysis** — keyword matching for ATS compatibility
- **Content Review** — measurable results, spelling/grammar
- **Rewrite Suggestions** — summary and bullet point rewrites
- **PDF Report** — professionally formatted output

### Match Score Weights

| Dimension | Weight |
|-----------|--------|
| Skills    | 40%    |
| Content   | 25%    |
| Style     | 15%    |
| Sections  | 10%    |
| Format    | 10%    |

---

## Installation

### Prerequisites

- Python 3.8+
- `reportlab` for PDF generation

```bash
pip install reportlab
```

### Install the Skill

**Option 1: From GitHub URL**

```bash
/skills add https://github.com/yezuochen/resume-checker
```

**Option 2: Manual Installation**

1. Download the repository
2. Copy `resume-checker.skill` to your Claude skills directory:
   - **Windows:** `%USERPROFILE%\.claude\skills\`
   - **macOS/Linux:** `~/.claude/skills/`

```bash
# Example on macOS/Linux
mkdir -p ~/.claude/skills
cp /path/to/resume-checker.skill ~/.claude/skills/
```

---

## Usage

Once installed, simply describe what you want. The skill triggers on phrases like:

| What you say | What happens |
|---|---|
| "check my resume against this job" | Skill activates |
| "resume review for this posting" | Skill activates |
| "how does my resume match this JD" | Skill activates |
| "improve my resume for this job" | Skill activates |
| "ATS check for my resume" | Skill activates |

### How It Works

1. **You provide:**
   - Job Description (as text, URL, file, or pasted content)
   - Resume (as PDF, DOCX, or pasted text)

2. **The skill:**
   - Extracts text from both sources
   - Runs 5-dimensional analysis
   - Calculates match score
   - Generates rewrite suggestions
   - Outputs `resume-checker-report.md` and `resume-checker-report.pdf`

---

## Development

For development, the source files are kept as readable markdown and Python:

```
resume-checker/
├── SKILL.md              # Skill definition (readable source)
├── scripts/
│   └── generate_report_pdf.py  # PDF generation script
└── README.md
```

### Building the Skill Bundle

The `.skill` binary is a ZIP containing `SKILL.md` + `scripts/`. To regenerate it locally:

```bash
cd resume-checker
zip -r ../resume-checker.skill SKILL.md scripts/
```

---

## Requirements

- Python 3.8+
- reportlab (for PDF generation)

---

## License

MIT
