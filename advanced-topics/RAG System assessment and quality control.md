# RAG System assessment and quality control
a. LangWatch, LangFuse  
b. Galileo  
c. Ragas  
d. DeepEval   
e. TrueLens  

### Framework Comparison Table
| Framework | Open Source | Key Metrics | Best For | Ease of Use | LLM-as-Judge | 
| --------- | ----------- | ----------- | -------- | ----------- | ------------ |
| DeepEval | ✅ | 14+ metrics including all basic and some advanced | Comprehensive testing | Very Easy (5 lines) | ✅ | 
| RAGAS    | ✅ | Faithfulness, Relevancy, Context Precision/Recall | Quick assessments | Easy | ✅ | 
| Arize Phoenix | ✅ | Custom evaluators, latency tracking | Performance monitoring | Medium | ✅ | 
| TruLens | ✅ | Custom feedback, app comparison |Development iteration | Medium | ✅ | 
| RAGChecker | ✅ | Diagnostic metrics, fine-grained analysis | Deep diagnosis | Medium | ✅ | 
| Quotient AI | ❌ | Faithfulness, relevancy benchmarks | Enterprise teams | Easy | ✅ | 
| LangWatch | ❌ | Real-time monitoring | Production monitoring | Easy | ✅ | 
| Galileo | ❌ | Advanced insights, transparency | Large-scale deployments | Easy | ✅ |
---
### Why to use such frameworks
➡️ Faithfulness - to catch hallucinations  
➡️ Answer Relevancy - to ensure responses stay on topic  
➡️ Context Precision - to optimize your retrieval ranking  

---
### Ragas
Ragas (RAG Assessment) is an evaluation framework specifically designed to assess Retrieval Augmented Generation (RAG) pipelines.  
It provides metrics to evaluate both the retrieval quality and generation quality of your RAG system.  
The framework operates on four key components:  
> 1. Question - The user's query  
> 2. Answer - Generated response from your RAG system  
> 3. Contexts - Retrieved document chunks used to generate the answer  
> 4. Ground Truth (optional) - Reference answer for comparison

#### Ragas Key Features
1️⃣ Automated Synthetic Test Data Generation: Can generate test questions from your documents    
2️⃣ Component-Level Evaluation: Separate metrics for retrieval vs generation    
3️⃣ Model Agnostic: Works with any LLM provider  
4️⃣ Integration Friendly: Works with LangChain, LlamaIndex, and could be integrated with experiment tracking tools  

#### Ragas usage
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

# Your evaluation dataset
dataset = {
    'question': [...],
    'answer': [...],
    'contexts': [...],
    'ground_truth': [...]  # optional
}

# Evaluate
result = evaluate(
    dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ],
)
```

#### Ragas Retrieval Metrics:
1️⃣ Context Recall:  
  * Measures if all relevant information from ground truth is present in retrieved contexts
  * Requires ground truth answers
  * Formula: Ratio of ground truth statements found in contexts

```txt
Context Recall = (Number of statements attributable to contexts) / (Total statements in ground truth)
```
```txt
Example:
Ground Truth: "Paris is the capital of France and has a population of over 2 million people."
Retrieved Contexts: ["Paris is the capital city of France."]

Statement 1: "Paris is the capital of France" ✓ (found in context)
Statement 2: "Paris has a population of over 2 million" ✗ (not in context)

Context Recall = 1/2 = 0.5
```

2️⃣ Context Precision:  
  * Measures if retrieved contexts are relevant to the question  
  * Evaluates ranking quality - are relevant chunks ranked higher?  
  * No ground truth needed  
3️⃣ Context Relevancy  
  * Measures what proportion of retrieved context is actually relevant   
  * Helps identify noise in retrieval  
#### Generation Metrics:
1️⃣ Faithfulness (Answer Faithfulness)  
  * Checks if the answer is factually consistent with the retrieved contexts  
  * Detects hallucinations    
  * Critical for ensuring grounded responses  
2️⃣ Answer Relevancy:  
  * Measures how relevant the answer is to the question  
  * Penalizes incomplete or redundant answers  
  * No ground truth needed  
3️⃣ Answer Correctness (requires ground truth):  
  * Compares generated answer against ground truth  
  * Uses both factual similarity and semantic similarity  
4️⃣ Answer Similarity (requires ground truth):
  * Semantic similarity between generated and ground truth answers  
