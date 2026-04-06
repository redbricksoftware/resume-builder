# Resume Builder

A Claude Code skill that tailors your resume for specific job postings and generates ATS-optimized Word documents.

## What It Does

1. You provide a job posting URL
2. Claude analyzes the job description against your master resume
3. Identifies your top 3-5 most relevant experiences
4. Asks targeted questions to fill gaps and strengthen bullets
5. Updates your master resume with new info (so it grows over time)
6. Generates a tailored, ATS-optimized 2-page Word document
7. (Optional) Opens Chrome to help you apply directly

## Install

### As a Claude Code Plugin (recommended)

From inside Claude Code, run these slash commands:

```
/plugin marketplace add redbricksoftware/resume-builder
/plugin install resume-builder@redbrick-tools
```

Then install the Python dependencies:

```bash
pip3 install python-docx pdfplumber playwright
```

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.8+
- Google Chrome (only needed for the optional apply step)

### Create Your Resume

**Option A: Import from an existing resume file**

If you already have a resume as `.docx`, `.pdf`, or `.txt`, just tell Claude:

```
Here's my resume: /path/to/my_resume.pdf
```

Claude will extract the content, convert it to the `resume.md` format, and ask you to review it.

**Option B: Start from the template**

```bash
cp resume_example.md resume.md
```

Edit `resume.md` with all of your experience, achievements, and skills.

**Tips for `resume.md`:**
- This is your **master resume** — include everything
- Quantify achievements whenever possible ($X revenue, Y% growth, Z team members)
- Include all roles going back 10-15 years
- List all technical skills, tools, and certifications
- Don't worry about length — the skill curates what goes into the final doc

## Usage

Open Claude Code in any directory and say:

```
I want to apply for this job: https://example.com/job-posting
```

The `/build-resume` skill triggers automatically and walks you through:

1. **Analysis** — scores your resume against the job requirements
2. **Q&A** — asks about gaps and ways to strengthen bullets (1-2 rounds)
3. **Updates** — adds new info to your `resume.md` for future use
4. **Review** — presents the tailored selection for your approval
5. **Generate** — creates `resume_[company]_[role].docx`
6. **Apply** (optional) — opens Chrome to help submit the application

## Files

| File | Purpose |
|------|---------|
| `resume.md` | Your master resume (you create this, gitignored) |
| `resume_example.md` | Template to get started |

## ATS Optimization

The generated resumes are designed to pass Applicant Tracking Systems:

- No tables — pure paragraph-based layout
- Standard section headings (Professional Summary, Professional Experience, Education, Core Competencies)
- Calibri font throughout
- Simple bullet points
- Keywords mirrored from the job description
- Contact info in the document body (not headers/footers)

## How the Master Resume Grows

Each time you use the skill, Claude asks about experience not yet in `resume.md`. When you share new details, they're permanently added. Over time, your master resume becomes a comprehensive record of everything you've done — making future applications faster and more complete.
