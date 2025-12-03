## Advanced AI LLM Topics.
### Document Retrieval Metrics
---
### NDCG@K. Normalized Discounted Cumulative Gain
**➡️ NDCG@K (Normalized Discounted Cumulative Gain)** - Ranking quality with relevance grades  

**➡️ When to use: When ranking order matters significantly.**  
> How good your ranking is, considering both relevance AND position.
> Perfect for RAG because users care more about top results.
> Simple explanation: Measures not just if relevant docs are retrieved, but whether the most relevant ones appear first.

```python
Formula: NDCG@k = DCG@k / IDCG@k

DCG = Discounted Cumulative Gain
IDCG = Ideal DCG (best possible ranking)

Query: "Find me AI tutorials"
Retrieved ranking: [Python_Advanced ✓✓✓, AI ✓✓✓✓, Java_Guide ✗]
Relevance scores:   [3,                4,                   0]

DCG@3 = 3/log₂(2) + 4/log₂(3) + 0/log₂(4) = 3 + 2.52 + 0 = 5.52
IDCG@3 = 4/log₂(2) + 3/log₂(3) + 0/log₂(4) = 4 + 1.89 + 0 = 5.89
NDCG@3 = 5.52/5.89 = 0.94
```
---
### MRR. Mean Reciprocal Rank.
**➡️ Mean Reciprocal Rank (MRR) - First relevant document positioning.**  
**➡️ When to use: When users typically only care about the first good result.**  
> What it measures: How quickly users find their first relevant result. Critical for RAG user experience.  


```python
Formula: MRR = Average of (1 / rank of first relevant result)
Example:
Query 1: First relevant at position 2 → 1/2 = 0.5
Query 2: First relevant at position 1 → 1/1 = 1.0
Query 3: First relevant at position 4 → 1/4 = 0.25
MRR = (0.5 + 1.0 + 0.25) / 3 = 0.58
```

---
### Contextual Relevancy.
**➡️ Simple explanation: How relevant is the retrieved context to the user's question?**  
**➡️ When to use: To ensure your retrieval system finds contextually appropriate information.**  

Calculation: Usually measured using LLM-as-a-judge that scores 0-1.  

```
Example:
Question: "How do I reset my password?"
Retrieved context: "To reset your password, go to settings..." → Score: 0.95
Retrieved context: "Our company was founded in 1995..." → Score: 0.1
```


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
### Multiple data sources. Recommendations.
<img width="2535" height="1577" alt="image" src="https://github.com/user-attachments/assets/06c84394-d578-4db7-8dda-4960a668b327" />

Data Quality and Retrieval Metrics. Primary Metrics:
* NDCG@5 - Overall ranking quality for top (5) results
* MRR - Time to first relevant result (user experience)

Analytics. Secondary Metrics:
* RBP with p=0.8 - Precision with realistic user behavior
* Embedding Quality - Monitor your vector space health

**Step 1: Create Your Evaluation Dataset**
```python
evaluation_queries = [
    # Financial queries (SQL + S3 strong)
    "Q3 revenue by business unit",
    "Budget variance analysis 2024", 
    "Cost center performance metrics",
    
    # Operational queries (DynamoDB + SharePoint strong)  
    "Customer support ticket trends",
    "User engagement analytics",
    "System performance metrics",
    
    # Strategic queries (SharePoint + S3 strong)
    "Product roadmap decisions",
    "Competitive analysis findings", 
    "Market research insights",
    
    # Mixed queries (all sources potentially relevant)
    "Project X status and financial impact",
    "Customer feedback and revenue correlation"
]
```
**Step 2. Relevance Grading Guidelines for Your Sources**

| Grade | SQL Database | DynamoDB | S3 Bucket | SharePoint | 
| --    | --           | --       | --        | --         |
| 3     | Exact data match (revenue=X) | Real-time metrics for query | Current, comprehensive report | Recent strategy doc/decision | 
| 2     | Related data (customer data for revenue query) | Historical relevant metrics | Relevant but partial report | Meeting notes with context | 
| 1     | Tangentially related (employee data) | Loosely related analytics | Old or partial doc | Outdated or tangential notes | 
| 0     | Unrelated data | Wrong metrics/timeframe | Wrong topic/very old | Irrelevant content |

**Step 3: Monitor Source Balance**
```
# Watch for these patterns in your source contribution analysis:
# 
# GOOD SIGNS:
# - Multiple sources contributing to top-5
# - High relevance rates (>70%) for sources that appear
# - Balanced distribution based on query types
#
# RED FLAGS:  
# - One source dominating all queries (fusion algorithm issue)
# - Low relevance rates (<50%) for frequently appearing sources
# - Sources never appearing in top-5 (retrieval issue)
```
