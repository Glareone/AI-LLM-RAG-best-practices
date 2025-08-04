## Advanced AI LLM Topics.
### Document Retrieval Metrics
---
* NDCG@K (Normalized Discounted Cumulative Gain) - Ranking quality with relevance grades
> How good your ranking is, considering both relevance AND position.
> Perfect for RAG because users care more about top results.

---
* Mean Reciprocal Rank (MRR) - First relevant document positioning
> What it measures: How quickly users find their first relevant result. Critical for RAG user experience.

---
* Expected Reciprocal Rank (ERR) - User behavior modeling with graded relevance
> What it measures: Advanced metric that models user behavior - probability that user stops at each result based on satisfaction.  
> Key Concept: Users examine results sequentially and stop when satisfied. More realistic than MRR.  

---
* Rank-Biased Precision (RBP) - Early result weighting strategies
> What it measures: Precision with exponential decay - heavily weights top results. Great for RAG where first few results matter most.

---
* Embedding Quality Metrics - Intra-cluster vs inter-cluster distance analysis
> What it measures: Quality of your vector space - are similar documents close together?


### Business Scenarios.
### Multiple data sources.

Data Quality and Retrieval Metrics. Primary Metrics:
* NDCG@5 - Overall ranking quality for top (5) results
* MRR - Time to first relevant result (user experience)

Analytics. Secondary Metrics:
* RBP with p=0.8 - Precision with realistic user behavior
* Embedding Quality - Monitor your vector space health
