# RAG System assessment and quality control
### Framework Comparison Table
| Framework | Open Source | Key Metrics | Best For | Ease of Use | LLM-as-Judge | 
| --------- | ----------- | ----------- | -------- | ----------- | ------------ |
| DeepEval | ✅ | 14+ metrics including all basic and some advanced (Faithfulness, relevancy, contextual metrics, hallucination) | Comprehensive testing | Very Easy (5 lines) | ✅ | 
| RAGAS    | ✅ | Faithfulness, Relevancy, Context recall/precision, answer relevancy, answer correctness | Quick assessments | Easy | ✅ | 
| Arize Phoenix | ✅ | Custom evaluators, latency tracking | Performance monitoring | Medium | ✅ | 
| TruLens | ✅ | Custom feedback, app comparison (Context relevance, groundedness, answer relevance) |Development iteration | Medium | ✅ | 
| RAGChecker | ✅ | Diagnostic metrics, fine-grained analysis | Deep diagnosis | Medium | ✅ | 
| Quotient AI | ❌ | Faithfulness, relevancy benchmarks | Enterprise teams | Easy | ✅ | 
| LangWatch | ✅ [Yes (MIT)](https://github.com/langwatch/langwatch) | Real-time monitoring | Production monitoring | Easy | ✅ | Easy | ✅ |
| LangFuse  | ✅ [Yes](https://github.com/langfuse/langfuse) | Traces, costs, latency, custom scores | Open-source first teams, self-hosting priority | Simple integration | ✅ Yes (via integrations) |
| Galileo | ❌ | Advanced insights, transparency (Hallucination detection, context adherence, chunk attribution) | Large-scale deployments | Easy | ✅ |
| AI Foundry | ❌ No (Microsoft) | Groundedness, relevance, context precision/recall/relevancy, response completeness, NDCG/XDCG/MRR, safety metrics | Azure ecosystem teams, comprehensive evaluation needs, enterprise compliance | High - Portal UI + SDK, integrated Azure tooling | ✅ Yes (OpenAI models, o3-mini reasoning models) |

---

### Framework Comparison in terms of Capabilities vs Price

| Framework | Language Support | Key Capabilities | Pricing |
| --------- | ---------------  | ---------------- | ------- |
| Azure AI Foundry | ✅ Python ✅ C# ✅ JavaScript/TypeScript ✅ Java | Full RAG pipeline evaluation (retrieval + generation). Golden IR metrics (NDCG, XDCG, MRR). Groundedness, relevance, context precision/recall/relevancy. Agent evaluators (intent, tool accuracy, task adherence). Parameter sweep with visual comparison. Synthetic data simulators. Safety & risk metrics. Visual UI for non-technical users. | Usage: Pay-as-you-go. Compute: ~$0.40/hour (VM). Storage: $0.02-$0.03/GB/month. Model tokens: Varies by model. Free tier: $200 credit (30 days). Note: Complex multi-service costs |
| LangWatch | ✅ Python. ⚠️ Limited multi-language | RAG evaluations via LangEvals. Integrates Ragas + custom evaluators. Retrieval-focused evaluation (fast, cheap). Real-time guardrails & blocking. Agent simulations (Scenario). Custom dashboards & analytics. Model-agnostic. User/product analytics | Free: Developer plan Paid: From €59/month. Self-hosted: Free (no restrictions). Enterprise: Custom pricing (SSO, dedicated support). Expensive in AWS (from 50k annually) |
| LangFuse | ✅ Python. ✅ JavaScript/TypeScript | Tracing & observability. Cost & latency tracking. Custom scores & annotations. LLM-as-judge (via integrations). Dataset management. Prompt management. | Free: Self-hosted (unlimited). Cloud Free: Generous tier. Cloud Pro: From $59/month. Enterprise: Custom pricing. Note: Excellent free self-hosting |
| Ragas | ✅ Python only | Context recall & precision. Faithfulness. Answer relevancy & correctness. Answer similarity. Context entity recall. Aspect critique. RAG-specific metrics. LLM-as-judge evaluation. Synthetic test data generation | Free & Open Source. MIT License. No usage fees. No hosting costs. Cost: Only LLM API calls for evaluation (e.g., OpenAI, Anthropic pricing) |

---

### Quick Decision Guide

Here's the enhanced decision guide with AWS/Azure and perimeter considerations:  
➡️ Quick Decision Guide  

➡️ 1️⃣ **For Multi-Language Projects (C#, Java):**   
✅ Azure AI Foundry - Best multi-language support  
⚠️ LangWatch/LangFuse/Ragas - Python-focused  
  
➡️ 2️⃣ **For Budget-Conscious Projects:**    
✅ Ragas - Completely free (library only)  
✅ LangFuse - Best free self-hosting + cloud free tier  
✅ LangWatch - Good free tier, affordable paid ($65/mo)  
⚠️ Azure AI Foundry - Variable costs, can get expensive  

➡️ 3️⃣ **For Comprehensive RAG Evaluation:**   
✅ Azure AI Foundry - Most complete (IR metrics + RAG + agents + safety)  
✅ LangWatch - Strong RAG focus via LangEvals + Ragas integration  
✅ Ragas - Deep RAG-specific metrics (library)  
⚠️ LangFuse - More observability-focused than RAG evaluation  

➡️ 4️⃣ **For Azure Ecosystem:**  
✅ Azure AI Foundry - Native integration, optimized for Azure  
✅ Ragas - Works anywhere (library)  
✅ LangFuse - Self-host in Azure VMs/AKS  
✅ LangWatch - Self-host in Azure VMs/AKS  
⚠️ LangFuse/LangWatch cloud - External to Azure  

➡️ 5️⃣ **For AWS Ecosystem:**  
✅ Ragas - Works anywhere (library)  
✅ LangFuse - Self-host in EC2/ECS/EKS  
✅ LangWatch - Self-host in EC2/ECS/EKS, AWS Marketplace available  
❌ Azure AI Foundry - Azure-only, not designed for AWS  

➡️ 6️⃣ **For Isolated/Private Perimeters (VPC, On-Premises, Air-Gapped):**  
✅ Ragas - Perfect (library only, no external calls except LLM APIs)  
✅ LangFuse - Free self-hosting, full control  
✅ LangWatch - Free self-hosting, full control  
✅ Azure AI Foundry - Possible in Azure private networks/VNets  
⚠️ Azure AI Foundry - Requires Azure infrastructure (can't run fully air-gapped)  

➡️ 7️⃣ **For Public/Internet-Accessible Perimeters:**  
✅ All frameworks - All support public cloud deployments  
✅ Azure AI Foundry - Managed Azure service  
✅ LangWatch Cloud - Managed SaaS option  
✅ LangFuse Cloud - Managed SaaS option  
✅ Ragas - Deploy anywhere with internet access  

➡️ 8️⃣ **For Maximum Deployment Flexibility:**  
✅ Ragas - Runs anywhere Python runs (AWS, Azure, GCP, on-prem, edge)  
✅ LangFuse - Self-host anywhere (Docker/Kubernetes)  
✅ LangWatch - Self-host anywhere (Docker/Kubernetes)  
❌ Azure AI Foundry - Azure-locked  

➡️ 9️⃣ **For Hybrid/Multi-Cloud Strategy:**  
✅ Ragas - Cloud-agnostic library  
✅ LangFuse - Self-host in any cloud  
✅ LangWatch - Self-host in any cloud  
❌ Azure AI Foundry - Azure-only, creates vendor lock-in  

➡️ 1️⃣0️⃣ **For Data Sovereignty & Compliance:**  
✅ Ragas - Data never leaves your infrastructure  
✅ LangFuse - Self-hosted = complete control  
✅ LangWatch - Self-hosted = complete control  
⚠️ Azure AI Foundry - Data stays in Azure (need to trust Microsoft)  
❌ LangWatch/LangFuse Cloud - Data on vendor infrastructure  

➡️ 1️⃣1️⃣ **For Open Source & Flexibility:**   
✅ Ragas - Pure library, most flexible  
✅ LangFuse - Full platform, free self-hosting  
✅ LangWatch - Platform + free self-hosting  
❌ Azure AI Foundry - Proprietary  

---

### Deployment Summary
| Framework | Azure Deployment | AWS Deployment | Isolated/Air-Gap | Public Cloud | Self-Hosted | 
| --------- | ---------------  | -------------  | ---------------- | ------------ | ----------- |
| Azure AI Foundry | ✅ Native | ❌ No | ⚠️ Azure VNet only | ✅ Yes | ❌ No |
| LangWatch | ✅ Self-hosted | ✅ Self-host/Marketplace | ✅ Yes | ✅ Cloud or self-host | ✅ Free | 
| LangFuse | ✅ Self-host | ✅ Self-host | ✅ Yes | ✅ Cloud or self-host | ✅ Free | 
| Ragas | ✅ Library | ✅ Library | ✅ Yes* | ✅ Yes | ✅ N/A (library) |
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

---
### Azure AI Foundry
Azure AI Foundry is Microsoft's unified platform for developing, evaluating, and deploying generative AI applications, with comprehensive RAG evaluation capabilities built directly into the platform.  

#### RAG Evaluation Features
1️⃣ [RetrievalEvaluator](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators): Measures textual quality of retrieval results using LLMs without requiring ground truth.  
2️⃣ [DocumentRetrievalEvaluator](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/the-future-of-ai-evaluating-and-optimizing-custom-rag-agents-using-azure-ai-foun/4455215): Provides classical information retrieval metrics including NDCG, XDCG, and max relevance, requiring ground truth for precise measurement.   
3️⃣ Context Precision: Evaluates if retrieved contexts are relevant and properly ranked.  
4️⃣ Context Recall: Measures alignment with expected responses.  
5️⃣ Context Relevancy: Assesses what proportion of retrieved content is actually relevant.  

#### Generation Quality Metrics:
  
1️⃣ Groundedness: Measures consistency of generated responses with grounding documents, complemented by Response Completeness for recall aspects.  
2️⃣ Answer Relevancy: Evaluates how relevant the answer is to the query.  
3️⃣ Response Completeness: Captures recall aspect of response alignment.  

#### Advanced Features
  
1️⃣ Parameter Sweep: Enables systematic optimization of search parameters (search algorithms, top_k, chunk sizes, re-ranker thresholds) by comparing evaluation results across configurations.  
2️⃣ Simulators: Generate synthetic test data when evaluation datasets are unavailable, including adversarial queries for safety testing and context-appropriate queries for quality assessment.  
3️⃣ Agent Evaluators: New metrics for agentic applications including intent resolution, tool call accuracy, task adherence, and response completeness.  
4️⃣ Integrated Observability: Seamless integration with Azure Monitor Application Insights for production monitoring.  

#### PROS AND CONS


---
