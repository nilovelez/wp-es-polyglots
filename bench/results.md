# Bench results

One row per case and run. Columns: found / reference changes (same wording), extra / candidate changes, missed.

| Date | Skill commit | Model | Case | Found | Same wording | Extra | Missed | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-11-11 | 5b2b9b2 (single skill, before the plugin) | Haiku | 01-jetpack-videopress-stable | 4/4 | 4 | 0/4 | 0 | Round 34 itself: the run that produced the reference proposals; the reviewer kept all four. Not a blind run. |
| 2026-11-11 | eb3922d (plugin) | Haiku | 02-gdpr-compliance-cookie-consent-stable | 18/18 | 18 | 0/18 | 0 | Round 35 itself, with the review skill: the reviewer kept all 18 proposals. Not a blind run. |
| 2026-11-11 | b981d44 (plugin) | Haiku | 03-zinn-connector-stable | 79/81 | 77 | 0/79 | 2 | Round 36 itself, review skill. Edited: «plugin de Zinn®» (#19), «Publicación» for the tab (#80). Missed: #85 reversed relation, #93 «Publicando» as a tab name. Not a blind run. |
