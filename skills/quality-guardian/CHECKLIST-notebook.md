# Checklist: Jupyter Notebooks (.ipynb)

- [ ] All code cells execute without errors?
- [ ] Cell outputs are current (not stale)?
- [ ] [critical] First cell contains complete metadata (Tier, Depth Levels, Prerequisites)?
- [ ] Cell structure follows Depth 1-5 progression?
  - [ ] Depth 1: Core understanding with analogy (markdown cells)
  - [ ] Depth 2: Prerequisites + quick check quiz (markdown + code)
  - [ ] Depth 3: Real-world scenarios (markdown + code)
  - [ ] Depth 4: Implementation with code examples (code cells)
  - [ ] Depth 5: Mastery exercises with solutions (code + markdown)
- [ ] Markdown explanations are pedagogically sound (clear language, no jargon before understanding)?
- [ ] Code examples build incrementally (not jumping to advanced)?
- [ ] Example data sets are realistic and runnable?
- [ ] All images referenced in _images/ folder exist?
- [ ] Cross-reference links resolve (to .md files, projects, learning plans)?
- [ ] No hardcoded absolute paths (all relative)?
- [ ] No credentials, API keys, or PII in cell outputs?
- [ ] Python kernel specified (Python 3.9, etc.)?
- [ ] Learning outcomes are testable and clear?
- [ ] [critical] notebook-registry.json entry created for this notebook?

**Verdict guidance** (global default applies)
