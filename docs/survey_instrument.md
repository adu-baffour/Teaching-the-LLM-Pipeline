# Survey instrument (as deployed)

Anonymous end-of-semester survey administered in Qualtrics. An information sheet was shown before the screening questions. The survey did not ask for names, student ID numbers, email addresses, or other direct identifiers. The same instrument appears as Appendix B of the paper.

All closed items use a deliberate three-point scale (chosen to reduce respondent burden): **Disagree / Neutral / Agree** for perception items and **Low / Moderate / High** for knowledge items. The column names in `data/survey.csv` are given in brackets.

## Screening and entry

- S1. Are you at least 18 years old? Yes / No.
- S2. Are you currently enrolled in the cross-listed Generative AI and Large Language Models course? Yes / No.
- S3. By continuing, you confirm that you are eligible and agree to participate in the survey portion of this study. Continue / Do not continue.

## Background

1. Which course are you enrolled in? Undergraduate course / Graduate course. [`course_level`]
2. What is your academic level? Junior undergraduate / Senior undergraduate / Master's student / Doctoral student / Other. [`acad_level`]
3. Before this course, how familiar were you with large language models? Not at all familiar / Slightly familiar / Very familiar. [`prior_llm`]
4. Before this course, how much experience did you have with machine learning or deep learning? None / Limited / Moderate / Extensive. [`prior_ml`]

## Core course experience (Disagree / Neutral / Agree)

5. This course helped me understand how the major parts of the LLM pipeline fit together. [`core_1`]
6. Earlier topics prepared me for later topics in a logical way. [`core_2`]
7. I leave this course with a clearer understanding of tokenization, attention, pretraining, adaptation, and system integration than I had before. [`core_3`]
8. The course improved my confidence in explaining how GPT-style systems work. [`core_4`]
9. The course improved my confidence in evaluating LLM behavior, not just using LLM tools. [`core_5`]
10. The pace of the course was appropriate for the level of difficulty. [`core_6`]
11. The workload was appropriate for a 3-credit course. [`core_7`]
12. The quizzes, homework, and project work helped me connect concepts across the semester. [`core_8`]
13. The live coding labs helped me better understand the concepts. [`core_9`]
14. The expectations for my course level were clear. [`core_10`]
15. The shared undergraduate/graduate classroom format worked well. [`core_11`]

## Retrospective knowledge (Low / Moderate / High)

Asked once, at the end of the semester. For each stage, respondents rated their knowledge **before the course** and **now**. No pre-course survey was given, so the "before" ratings are retrospective self-reports.

16. Representation: tokenization, token IDs, embeddings, positional information. [`before_1`, `now_1`]
17. Model internals: attention, masking, GPT-style architecture. [`before_2`, `now_2`]
18. Training and evaluation: pretraining, decoding, loss/perplexity, interpretation of results. [`before_3`, `now_3`]
19. Adaptation: fine-tuning, instruction tuning, LoRA/PEFT. [`before_4`, `now_4`]
20. System integration: RAG and agents. [`before_5`, `now_5`]

## Differentiation and misconception repair (Disagree / Neutral / Agree)

21. The differences between undergraduate and graduate expectations were appropriate. [`diff_1`]
22. Students at my course level were challenged appropriately. [`diff_2`]
23. Activities that focused on repairing misconceptions helped me understand relationships among LLM components. [`diff_3`]
24. I still feel uncertain about how some parts of the LLM pipeline connect to one another. (Negatively worded; agreement is unfavorable.) [`diff_4`]
25. Undergraduate students only: The course appropriately emphasized building and evaluating feasible working systems. [`diff_5`]
26. Graduate students only: The course appropriately emphasized grounding in literature, reproducibility, comparison, or scholarly justification. [`diff_6`]

## Open-ended

27. What aspect of the course most helped your learning? [`most_helped`]
28. What aspect of the course was most challenging or least clear? [`most_challenging`]
29. How did you experience the undergraduate/graduate structure of the course, if at all? (Not analyzed in the paper and not included in the released data.)
30. What is one change that would most improve this course in a future offering? [`one_change`]
31. Optional: If you remember the misconception-repair / Pipeline Debugger activity, what was useful about it, if anything? [`pipeline_debugger`]
