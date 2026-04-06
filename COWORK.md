# Automate Your Job Search with Cowork

Claude's **cowork** feature lets you schedule an agent to automatically search for matching jobs on a recurring basis — daily, multiple times a day, or whatever cadence you want. It runs in the cloud, so you don't need to keep your computer open.

## What the Scheduled Agent Does

Every time it runs, the agent will:

1. Search across job boards (LinkedIn, Indeed, Greenhouse, Lever, Glassdoor) for roles matching your criteria
2. Filter out old postings, low-salary roles, and jobs you've already seen
3. Log every role it finds to a job tracker spreadsheet so nothing gets lost
4. Commit the updated tracker to your repo so you can review it anytime

**What it won't do:** The agent runs autonomously, so it can't ask you questions or build tailored resumes — that part is still interactive. Think of it as your personal recruiter surfacing the best leads. You review the list, pick the ones you like, and then run the resume builder yourself.

## How to Set It Up

### Step 1: Open Claude Code

Cowork scheduling is set up through Claude Code (the CLI or desktop developer tool). If you don't have it, install it from [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code).

### Step 2: Tell Claude to create a scheduled job search

Open Claude Code in your resume-builder directory and say something like:

```
I want to schedule a daily job search using cowork. Here are my criteria:

Titles: [e.g., "VP of Product", "Senior Director of Product", "Head of AI"]
Locations: [e.g., "Remote", "New York, NY", "San Francisco, CA"]
Minimum salary: [e.g., "$200,000"]
Industries or companies of interest: [e.g., "AI/ML startups", "enterprise SaaS"]
Max posting age: [e.g., "7 days"]

Run it every morning at 8am.
```

Claude will walk you through the setup, including:
- Crafting the search prompt
- Setting the schedule (converted to UTC for you)
- Connecting your GitHub repo so the tracker stays updated
- Reviewing everything before it goes live

### Step 3: Review your results

After each run, check the `job_application_tracker.xlsx` file in your repo. It will have new rows for every role the agent found, with:

| Column | What It Shows |
|--------|---------------|
| Date Found | When the agent surfaced this role |
| Company | Company name |
| Job Title | Full title |
| Location | City/state or Remote |
| Salary | Range if listed |
| Job Posting URL | Clickable link to the posting |
| Status | "New" for fresh finds |
| Notes | Why the agent thinks it's a good match |

### Step 4: Build resumes for the roles you like

When you see a role you want to apply for, open the resume builder (in Claude Desktop or Claude Code) and say:

```
I want to apply for this job: [paste the URL from the tracker]
```

The resume builder will take over from there — analyzing the fit, asking you targeted questions, and generating a tailored resume.

## Managing Your Schedule

You can manage your scheduled agents at any time:

- **View all schedules:** Open Claude Code and say "list my scheduled agents"
- **Pause a schedule:** Say "disable my job search schedule"
- **Change the timing:** Say "update my job search to run twice a day at 8am and 6pm"
- **Run it right now:** Say "run my job search agent now"
- **View online:** Visit [claude.ai/code/scheduled](https://claude.ai/code/scheduled) to see all your scheduled agents

## Example Search Prompt

Here's an example of what the agent's search prompt looks like under the hood. You don't need to write this yourself — Claude builds it for you during setup — but it helps to understand what's happening:

```
Search for job postings matching these criteria:

Titles: "VP of Product", "Senior Director of Product", "Head of AI Product"
Locations: Remote, New York NY, San Francisco CA
Minimum salary: $200,000
Posting age: Last 7 days
Exclude companies: [any from tracker in last 30 days]

Search LinkedIn, Indeed, Greenhouse, Lever, Glassdoor, and major company career pages.

For each matching role, record:
- Date found, company, title, location, salary, URL, and a 1-2 sentence note
  on why it matches

Add all results to job_application_tracker.xlsx:
- New matches: Status = "New"
- Previously seen URLs: skip (dedup)
- Same company within 30 days: skip unless different role level

Commit the updated tracker with message: "Daily job search: [date] - [N] new roles found"
```

## Tips

- **Start broad, then narrow.** Cast a wide net at first, then refine your titles and filters after seeing the first few batches of results.
- **Check the tracker regularly.** Job postings move fast — the best ones get filled within days.
- **Let the base resume grow.** Each time you use the resume builder, it adds new details to your base resume. After a few applications, the Q&A rounds get shorter because most of your experience is already captured.
- **Combine with the cross-check tip.** After generating a tailored resume, paste it and the job description into a different AI (like Gemini) to score the fit before you apply.
