# Rewrite Rules Reference

| Anti-pattern | Replace with |
|---|---|
| "Please make sure to..." | Imperative verb |
| "I would like you to..." | Start with the verb |
| "In order to X, you should Y" | "To X: Y" |
| "It is important that you never..." | "Never:" |
| "Feel free to ask for clarification" | Delete |
| "As an AI language model..." | Delete |
| Prose routing logic | Skill trigger blocks |
| Timestamp in system prompt | Move to user turn |
| Pretty-printed JSON in context | Minify before sending |
| Full file in context | Send method/class only |
| Long tool description paragraph | One sentence max |
| Vague description ("helps with X") | Add WHEN + trigger phrases |
| Missing "Do NOT trigger for" | Add with routing alternatives |
| Output path as example only | Replace with template pattern |
| Example output filename | Template: `[prefix]-[name]-[YYYY-MM-DD].ext` |
