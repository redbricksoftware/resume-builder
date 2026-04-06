# Resume Builder

An AI-powered resume builder that tailors your resume for specific job postings. Works with **Claude Desktop** (no coding required) or **Claude Code** (for developers who want Word document generation and automated applications).

## What It Does

1. You provide a job posting URL
2. Claude analyzes the job description against your base resume
3. Identifies your top 3-5 most relevant experiences
4. Asks targeted questions to fill gaps and strengthen bullets
5. Updates your base resume with new info (so it grows over time)
6. Generates a tailored, ATS-optimized 2-page Word document
7. (Optional) Opens Chrome to help you apply directly

## Install

### Option A: Claude Desktop (easiest — no coding required)

You can use this resume builder directly in the Claude Desktop app with no installation or coding. Here's how to set it up:

#### Step 1: Open Claude Desktop

If you don't have Claude Desktop yet, download it from [claude.ai/download](https://claude.ai/download) and create an account.

#### Step 2: Create a new Project

1. Open Claude Desktop
2. Click the **menu icon** (three horizontal lines) in the top-left corner
3. Click **Projects** in the sidebar
4. Click **Create Project** (or the **+** button)
5. Give it a name like "Resume Builder"

#### Step 3: Add the resume builder instructions

1. Inside your new project, click **Set up project** (or the gear icon)
2. Under **Project knowledge**, click **Add content** then **Add text content**
3. Open this link in your browser: [SKILL-claude-desktop.md on GitHub](https://github.com/redbricksoftware/resume-builder/blob/main/SKILL-claude-desktop.md)
4. Click the **Raw** button near the top-right of the file content — this shows the plain text
5. Select all the text on the page (Ctrl+A on Windows, Cmd+A on Mac), then copy it (Ctrl+C / Cmd+C)
6. Go back to Claude Desktop and paste it into the text content area (Ctrl+V / Cmd+V)
7. Give it a title like "Resume Builder Instructions"
8. Click **Save**

#### Step 4: Add your resume

1. Still in the project settings under **Project knowledge**, click **Add content** then **Upload files**
2. Upload your resume file (PDF, Word, or text file)
   - Don't have a digital resume? No problem — start a conversation in the project and tell Claude about your work experience. It will help you build one from scratch.

#### Step 5: Start building tailored resumes

1. Go back to your project and start a new conversation
2. Type something like:

   ```
   I want to apply for this job: https://example.com/job-posting
   ```

3. Claude will walk you through the process step by step:
   - It analyzes the job posting and compares it to your resume
   - It asks you targeted questions to fill in any gaps
   - It shows you a draft for approval
   - It generates your tailored resume as formatted text you can copy into Word or Google Docs

#### Tips for Claude Desktop users

- **Save your updated base resume.** After each session, Claude will give you an updated version of your resume with new details added. Copy this and upload it to your project knowledge (replacing the old one) so future applications are faster.
- **Review before submitting.** Always copy the output into a Word document or Google Doc, make manual edits, save as PDF, and submit yourself.
- **Cross-check with another AI.** After generating your resume, paste it along with the job description into a different AI tool (like Google's Gemini) and ask it to score how well your resume matches. Great sanity check.

---

### Option B: Claude Code Plugin (for developers)

If you use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (the CLI/desktop developer tool), you can install this as a plugin for a more integrated experience including Word document generation and optional automated job applications.

From inside Claude Code, run these slash commands:

```
/install-plugin redbricksoftware/resume-builder
```

Then install the Python dependencies:

```bash
pip3 install python-docx pdfplumber playwright
```

#### Prerequisites

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
- This is your **base resume** — include everything
- Quantify achievements whenever possible ($X revenue, Y% growth, Z team members)
- Include all roles going back 10-15 years
- List all technical skills, tools, and certifications
- Don't worry about length — the skill curates what goes into the final doc

## Usage (Claude Code)

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
| `resume.md` | Your base resume (you create this, gitignored) |
| `resume_example.md` | Template to get started |

## ATS Optimization

The generated resumes are designed to pass Applicant Tracking Systems:

- No tables — pure paragraph-based layout
- Standard section headings (Professional Summary, Professional Experience, Education, Core Competencies)
- Calibri font throughout
- Simple bullet points
- Keywords mirrored from the job description
- Contact info in the document body (not headers/footers)

## Automate Your Job Search with Cowork

Want to have Claude search for matching jobs automatically every day? See **[COWORK.md](COWORK.md)** for setup instructions. The scheduled agent searches across job boards, filters results, and logs everything to a tracker — so you just review the list and build resumes for the roles you like.

## How the Base Resume Grows

Each time you use the skill, Claude asks about experience not yet in `resume.md`. When you share new details, they're permanently added. Over time, your base resume becomes a comprehensive record of everything you've done — making future applications faster and more complete.
