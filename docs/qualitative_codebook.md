# Qualitative codebook (RQ6)

Reflexive thematic analysis (Braun & Clarke, 2006, 2021) of the open-ended survey responses. Coding was inductive, carried out by the instructor-researcher in two time-separated passes, with a written reflexive journal. Critical and supportive comments were both retained. Codes are multi-label, and frequencies count respondents.

The complete coding is stored as data in `data/qualitative_coding.json` (codebook, response-to-code assignments, stage assignments for Figure 5, and exemplar quotes). `analysis/qualitative.py` counts the codes and writes the audit trail to `results/rq6_audit_trail.csv`, where every response appears next to its codes.

Responses such as "N/a" to the change question were coded as *no change*; to the Pipeline Debugger question, as *does not remember*.

## What most helped your learning? (30 responses)

> What aspect of the course most helped your learning?

| Code | Respondents | Definition |
|---|---|---|
| `labs` | 20 | Live-coding labs / in-class coding / hands-on in-class activities |
| `instructor` | 6 | Instructor explanation, walkthroughs, demonstrations, teaching quality |
| `structure` | 5 | Content structure, sequencing, flow, foundation-building |
| `project` | 4 | Course project / semester project |
| `visualization` | 3 | Diagrams / visual representations of the pipeline |
| `homework` | 2 | Homework / assignments |

## What was most challenging or least clear? (26 responses)

> What aspect of the course was most challenging or least clear?

| Code | Respondents | Definition |
|---|---|---|
| `attention_internals` | 7 | Attention / QKV / embeddings / positional encoding / stride (model internals & representation) |
| `project` | 6 | Course/final project or milestone |
| `labs_tooling` | 4 | Keeping up with in-class labs; unfamiliar tools/libraries; an unclear in-class activity |
| `rag_agents` | 3 | RAG and agents (system integration) |
| `homework` | 3 | Homework difficulty or unclear/overwhelming instructions |
| `pace` | 2 | Pace / time to absorb material |
| `interconnections` | 1 | Many interacting concepts at once felt confusing |
| `ml_background` | 1 | Lacking ML background; volume of ML concepts |

## One change that would most improve the course (22 responses)

> What is one change that would most improve this course in a future offering?

| Code | Respondents | Definition |
|---|---|---|
| `content_rebalance` | 5 | Add/rebalance content (other generative AI, more ML, more depth on specific topics) |
| `clarity_instructions` | 5 | Clearer / less open-ended homework & project instructions; consolidate turn-in requirements; library/setup support |
| `none_praise` | 4 | No change / course well structured |
| `more_labs` | 3 | More lab/hands-on/application time; dedicated lab portion |
| `logistics` | 1 | Logistics (e.g., use school lab machines) |
| `separate_sections` | 1 | Separate undergraduate and graduate sections (graduate found it too much review) |
| `group_activities` | 1 | Group/in-class activities less useful |
| `project_pacing` | 1 | Spread project requirements out; shorter, more frequent deadlines |
| `slides` | 1 | Better explanation of slide diagrams for later review |

## Pipeline Debugger (optional) (9 responses)

> Optional: If you remember the misconception-repair / Pipeline Debugger activity, what was useful about it, if anything?

| Code | Respondents | Definition |
|---|---|---|
| `dont_remember` | 5 | Does not remember the activity / N/A |
| `peer_collaboration` | 2 | Value from working with / learning from other students |
| `debugging` | 2 | Debugging practice / instructor feedback |
| `misconception_correction` | 1 | Corrected a specific misconception |
