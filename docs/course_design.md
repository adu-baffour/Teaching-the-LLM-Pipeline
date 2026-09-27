# Course design: a pipeline-centered LLM course

A three-credit, cross-listed undergraduate/graduate special topics course on generative AI and large language models (LLMs), taught in person twice a week for 15 weeks by one instructor. Undergraduates needed junior standing; graduate students needed prior coursework in algorithms and machine learning, or instructor approval. All labs and assignments run on the free tier of Google Colab.

The design has three core elements. A fourth component, the [Pipeline Debugger](pipeline_debugger.md), was added during the semester and is presented as a proposed intervention.

## 1. Pipeline-centered sequencing

Each stage of the LLM pipeline builds the foundation for the next. Retrieval-augmented generation (RAG) and agents come last, so students place them inside the pipeline they have already built rather than treating them as product features.

| Stage | Weeks | Main topics | Aligned assessment |
|---|---|---|---|
| Orientation | 1 | Generative AI and LLM applications; course tooling | Orientation quiz; participation |
| Representation | 2–3 | Tokenization, token IDs, embeddings, positional information | Topic quiz; Homework 1 (tokenizer, embeddings) |
| Model internals | 4–7 | Attention, trainable query-key-value projections, causal masking, multi-head attention, layer normalization, feed-forward blocks, greedy generation | Topic quizzes; attention lab; mini-GPT build |
| Training & evaluation | 8–9 | Next-token datasets, cross-entropy, loss and perplexity, decoding, qualitative sample assessment | Topic quiz; Homework 2 (mini-GPT pretraining) |
| Adaptation | 10–13 | Classification fine-tuning, instruction tuning, LoRA and other parameter-efficient fine-tuning (PEFT) methods | Topic quiz; Homework 3 (LoRA, retrieval, agents) |
| System integration | 14–15 | RAG, agents, and tool use | Project milestones; final exam |

## 2. Assessment aligned with the pipeline

- **Homework** is cumulative: tokenization and embeddings (HW1); assembling and pretraining a small GPT-style model while tracking loss, perplexity, and samples (HW2); LoRA adaptation, RAG, and agents (HW3).
- **Live coding labs** (short Jupyter notebooks) connect lectures to assignments: attention scores and context vectors, scaled dot-product attention, causal masking, multi-head attention, next-token datasets, loss curves, instruction-tuning data, LoRA parameter counts, and RAG/agent workflows.
- **Topic quizzes**, a **three-milestone project**, and a **comprehensive final exam** complete the assessment.

## 3. Differentiation through epistemic demand

All students share lectures and the pipeline. Levels differ in the evidence students must produce, set out in separate syllabi, rubrics, and project briefs.

| Dimension | Undergraduate emphasis | Graduate emphasis |
|---|---|---|
| Shared course core | Common lectures and the same LLM pipeline | Common lectures and the same LLM pipeline |
| Primary emphasis | Applied technical competence and feasible working systems | Research- and systems-oriented depth |
| Evidence and justification | Baseline metrics and representative qualitative examples | Baselines plus reproducibility, ablations, comparison, and validity discussion |
| Project | Feasibility, implementation, and baseline evaluation | Literature grounding, reproducibility, ablations, and scholarly reporting |
| Scholarly framing | Limited and mainly supportive | Explicit engagement with related literature and conference-style reporting |
