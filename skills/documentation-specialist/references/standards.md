# Documentation: Writing Standards

Consistency and exactness are non-negotiable.

## Formatting
- **Headings:** Sentence case. Max 3 levels in README, 4 in deep dives.
- **Code:** Always use language tags (e.g. ` ```bash `).
- **Paths/Names:** Backticked and relative (e.g. `` `src/main.py` ``).
- **Links:** Relative markdown links only.
- **Tables:** Preferred for comparisons and structured data.
- **Timestamp:** "Last Updated: YYYY-MM-DD" at the **bottom** only.

## Style
- **Problem-first:** Start with "why".
- **Active voice:** "Run script" not "The script should be run".
- **Zero fluff:** Remove transition filler ("important to note", "simply").
- **Facts only:** Document what IS, not roadmaps or theories.
- **No Credentials:** Use `<placeholder>` for all secrets/PII.

## Enforcement
- **Registry:** `projects/README.md` must be updated for every change.
- **Index:** `projects/{service}/README.md` must have a Status Table.
- **No root-clutter:** Unauthorized files at `documentation/` root will be moved.
