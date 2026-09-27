# Pipeline Debugger activity template

A misconception-repair activity for the model-internals unit. It is presented in the paper as a **proposed intervention**: it was run once and was not evaluated as a controlled intervention. The template is Appendix A of the paper.

## How it runs

1. **Group diagnosis.** Small groups receive deliberately flawed explanations of the LLM pipeline and label each statement *wrong*, *partly wrong*, or *misleading*.
2. **Correction.** Groups rewrite each statement in one accurate sentence.
3. **Consequence.** Groups state what would break in the model if the error remained. This step asks students to reason about how components interact, not only to recall definitions.
4. **Consolidation.** Groups compare their repairs in a guided whole-class discussion.
5. **Synthesis.** Each student writes a short explanation of how the corrected concepts fit together in the pipeline.

## Student response template

| Prompt element | Student response |
|---|---|
| Buggy statement | Provided by the instructor; contains one misconception |
| Verdict | Wrong, partly wrong, or misleading |
| Correction | One accurate sentence that repairs the concept |
| Consequence | What would break in the model if the error remained |
| Synthesis | A short explanation of how the corrected concept fits the pipeline |

## Sample misconception prompts

| Misconception prompt | Intended correction focus |
|---|---|
| Token IDs already encode the meanings of words. | Token IDs are discrete lookup indices; their meaning is learned in the embedding layer. |
| Self-attention already knows the order of the words. | Self-attention is permutation-invariant without positional information; positional encodings are required to represent word order. |
| The causal mask only optimizes the speed. | Decoder-only models use causal masking so that positions cannot attend to future tokens during training. |
| Logits are probabilities, so decoding can read them directly. | Logits are unnormalized scores; a softmax is required to obtain probabilities. |
| LoRA fine-tuning retrains the entire model. | LoRA freezes the base model and trains small low-rank adapters. |
