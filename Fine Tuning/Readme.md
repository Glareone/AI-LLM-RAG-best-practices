## Table of Contents

1. [What is Fine-Tuning and When Do You Need It?](#fine-tuning)  
2. [Understanding LoRA (Low-Rank Adaptation)](#lora-understanding-of-lora)  
3. [Core. Parameter-Efficient Fine-tuning)](#parameter-efficient-fine-tuning) 
    - [Rank Parameter (r)](#a-rank-parameter-r---8-64-range-efficiency-vs-capacity-trade-off)  
    - Alpha Scaling Factor  
    - Target Module Selection
4. Advanced LoRA Variants  
    - AdaLoRA  
    - QLoRA  


When to Use LoRA Fine-Tuning
Coming Up Next

### Fine tuning

Fine-tuning is the process of taking a pre-trained language model and further training it on your specific task or domain data. 

When Fine-Tuning Makes Sense:  
✅ Domain-Specific Language: Medical, legal, or technical domains with specialized terminology.  
✅ Consistent Style/Tone: Brand voice, formal reports, creative writing patterns.  
✅ Task-Specific Behavior: Classification, extraction, structured output generation.  
✅ Private/Proprietary Knowledge: Internal documentation, company-specific processes.  
✅ Performance Optimization: When prompt engineering alone doesn't achieve desired accuracy.  

When Fine-Tuning Might Be Overkill:  
❌ General Q&A that GPT-4 or similar models already handle well.  
❌ Tasks that can be solved with good prompt engineering and RAG (Retrieval-Augmented Generation).  
❌ Limited training data (<1000 quality examples).  
❌ Rapidly changing requirements (fine-tuned models are less flexible than prompted models).  

### LoRA. Understanding of LoRA
The Traditional Fine-tuning has a problem. Full fine-tuning of large language models (LLMs) requires a lot of resources:
* Updating billions of parameters
* Storing a complete copy of the model for each task
* Massive GPU memory (100GB+ for models like LLaMA-70B)
* Days or weeks of training time

**LoRA introduces a clever mathematical trick**: instead of modifying the original weights directly, it adds small "adapter" matrices that capture the changes needed for your task.  
**Mathematical Intuition (simplified):**
```
Original weight matrix: W (e.g., 4096 × 4096 = 16.7M parameters)
LoRA decomposition: W + ΔW = W + A × B

Where:
- A is 4096 × r (e.g., 4096 × 8 = 32K parameters)
- B is r × 4096 (e.g., 8 × 4096 = 32K parameters)
- Total trainable parameters: only 64K instead of 16.7M!
```

**Benefits:**
💾 Memory Efficient: Train with 10-100x less GPU memory  
⚡ Faster Training: Fewer parameters = faster iterations  
💰 Cost Effective: Can train on consumer GPUs (RTX 4090, RTX5080, RTX5090, etc.)  
🔄 Modular: Switch between different LoRA adapters without reloading the base model  

---

### Parameter-Efficient Fine-tuning  
Parameter-Efficient Fine-Tuning (PEFT) refers to techniques that adapt large pre-trained models to specific tasks while updating only a small fraction of the model's parameters.  
It means, that instead of retraining billions of weights, PEFT methods like LoRA train only millions (or even thousands) of additional parameters, achieving comparable results with dramatically reduced computational costs.  

**The key insight**: you don't need to change everything to teach the model something new. By carefully selecting which parameters to train and how to structure those trainable parameters, you can achieve 95-99% of full fine-tuning performance while training only 0.1-1% of the parameters.

**The following parameters control how LoRA implements this parameter-efficient approach:**

---
#### A. Rank Parameter (r) - 8-64 range, efficiency vs capacity trade-off  
> r

The "r" parameter determines the size of the adapter matrices and represents the rank of the low-rank decomposition.  
In other words, it is the level of detail in your modifications. Higher rank = more capacity to learn, but also more parameters to train.

**Typical Ranges:**  
1. r = 4-8: Lightweight, for simple tasks (sentiment classification, basic style adaptation)
2. r = 16-32: Moderate, for most fine-tuning tasks (instruction following, domain adaptation)
3. r = 64+: Heavy, for complex tasks requiring significant model changes (rare, approaching full fine-tuning costs)

| Task Complexity | Recommended r | Parameters Added (per layer) |
| --------------- | ------------- | ---------------------------- |
| Simple classification |     4-8 |              ~50K-100K |
| Style/tone adaptation |     8-16 |             ~100K-200K |
| Domain specialization |     16-32 |            ~200K-400K |
| Complex reasoning |         32-64 |            ~400K-800K |

**Real-world example**:
1. Fine-tuning LLaMA-7B with r=8 adds only ~4.2M trainable parameters (~0.06% of the model)
2. With r=32, adds ~16.8M parameters (~0.24% of the model)

---

#### B. Alpha Scaling Factor - Typically 16-32  
> alpha / r

A scaling factor that controls how much the LoRA updates influence the original model. Specifically, the LoRA contribution is scaled by (alpha / r).  
The volume knob for your fine-tuning. It determines how strongly your training data affects the model's behavior.  

**Typical Values**:
1. **alpha = 16**: Conservative, subtle changes
2. **alpha = 32**: Moderate, common default
3. **alpha = 64**: Aggressive, strong adaptation

The Relationship Between Alpha and Rank:
The effective learning rate of LoRA adapters is proportional to `alpha / r`:
| Configuration |    alpha/r |    Effect |
| -- | -- | -- |
| r=8,  alpha=16 |   2.0 |       Moderate influence |
| r=16, alpha=16 |   1.0 |       Gentle influence   |
| r=16, alpha=32 |   2.0 |       Moderate influence |
| r=32, alpha=32 |   1.0 |       Gentle influence   |
| r=8,  alpha=32 |   4.0 |       Strong influence   |

**Common Practices**:
1. Use alpha = 2 × r as a starting point Example: r=8 → alpha=16, or r=16 → alpha=32

Why It Matters:

Too low: Model doesn't learn enough from your data
Too high: Model forgets pre-trained knowledge (catastrophic forgetting)
The ratio helps balance new learning with preserving the base model's capabilities

Practical Tip: If your fine-tuned model produces outputs that are too similar to the base model (not learning enough), increase alpha. If it "forgets" general knowledge, decrease alpha or increase r.

#### C. Target Module Selection - Query, value, key, output projections  

#### D. AdaLoRA - Adaptive rank allocation   

#### E. QLoRA - 4-bit quantized LoRA for memory efficiency  

---

2. [Training Parameters](https://github.com/Glareone/AI-LLM-RAG-best-practices/blob/main/Fine%20Tuning/Training%20Parameters.md)
    a. Learning Rate Ranges - 1e-5 to 5e-4 for LLMs with warmup  
    b. Batch Size Optimization - 8-32 full fine-tuning, 64-128 LoRA  
    c. Sequence Length Limits - 512-4096 tokens task dependency  
    d. Weight Decay (L2 Regularization) - λ||w||² with λ = 1e-4 to 1e-2  
