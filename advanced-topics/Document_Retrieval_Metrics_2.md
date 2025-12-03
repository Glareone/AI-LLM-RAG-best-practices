Document Retrieval Metrics 2

## What are the Document Retrieval Metrics?

They include the following golden metrics in information retrieval to specifically target retrieval quality measurement in a RAG system:

| Metric | Higher is Better | Description |
|--------|------------------|-------------|
| Fidelity | Yes | Measures how well the top n retrieved chunks reflect the content for a given query; calculated as the number of good documents returned out of total known good documents in a dataset. |
| NDCG | Yes | Evaluates how close the ranking is to an ideal order where all relevant items appear at the top of the list. |
| XDCG | Yes | Assess the quality of results within the top-k documents, regardless of scoring of other index documents. |
| Max Relevance N | Yes | Captures the maximum relevance score in the top-K chunks. |
| Holes | No | Counts the number of documents missing query relevance judgments (ground truth). |

----
### Fidelity
Measures recall quality - what percentage of all relevant documents in your dataset were actually retrieved in the top-n results.  
Higher fidelity means you're not missing important relevant documents.

----
### XDCG
A ranking quality metric that focuses specifically on how well the top-k retrieved documents are ordered, ignoring the rest of your document collection.  
It's more targeted than NDCG for evaluating just your retrieved results.

----
#### XDCG vs NDCG

**NDCG**: Evaluates ranking quality across your entire document collection - wants all relevant docs at the very top.  
**XDCG**: Only cares about ranking quality within your retrieved top-k results - more practical for RAG systems where you only use a few chunks.  

----
### Max Relevance N
Simply captures the highest relevance score among your top-k retrieved chunks. Helps ensure at least one highly relevant document made it into your results.

----
### Holes
Counts missing ground truth data - documents that lack human relevance judgments for evaluation. Lower is better since holes make it harder to accurately measure your retrieval system's performance.
