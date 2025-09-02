## Advanced Evaluation Metrics & Methodologies
### Response Quality Metrics
* BLEU Score - N-gram overlap evaluation.  
`Traditional metric. BLEU - Still widely used, fast computation.`
* ROUGE (L/1/2) - Recall-oriented summarization metrics.  
`Traditional metric. ROUGE - Essential for summarization tasks.`
* BERTScore - Semantic similarity using contextualized embeddings  
`BERTScore - 0.93 Pearson correlation with human judgments, significantly outperforming BLEU (0.70) and ROUGE (0.78)`
* G-Eval
`G-Eval - LLM-as-judge approach, best for complex reasoning`
* BLEURT - BERT-based learned evaluation metric
* SacreBLEU - Standardized BLEU with proper tokenization
* METEOR - Synonym and paraphrase consideration
* CIDEr - Consensus-based evaluation
* CHRF - Character-level F-score for multilingual evaluation

| Metric | Best For | Limitations | Correlation with Humans |
| -----  | -------  | ----------  | ----------------------- |
| BERTScore | Semantic evaluation, paraphrasing | Computationally heavier | 0.93 (Excellent) | 
| BLEUExact | matching, translation | No semantic understanding | 0.70 (Good) | 
| ROUGE | Summarization, content coverage | Surface-level matching | 0.78 (Good) | 
| G-Eval | Complex reasoning, creativity | Expensive, variable | 0.85+ (Excellent) |

### LangWatch. What's supported out of the box
LangWatch offers an extensive library of evaluators to help you evaluate the quality and guarantee the safety of your LLM apps, including:
* Built-in evaluators for RAG systems, guardrails, and safety  
* LLM-as-a-judge metrics (G-Eval style)  
* Custom evaluator framework - this is key for your BLEU/BERTScore needs  
* Real-time and offline evaluation pipelines

❗️ Important Finding: Traditional metrics like BLEU and BERTScore are not directly built-in to LangWatch, but you can easily implement them as custom evaluators.
