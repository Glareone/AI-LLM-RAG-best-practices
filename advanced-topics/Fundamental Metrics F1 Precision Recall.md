## Fundamental Metrics of Response.

1️⃣ Precision: "Of what I found, how much was actually good?"
2️⃣ Recall: "Of all the good stuff that exists, how much did I find?"
3️⃣ F1: "What's the balanced score between precision and recall?"

---
#### The Crime Scene Analogy
Imagine you're a detective looking for evidence at a crime scene:

> Total Evidence Available: 10 pieces of real evidence exist  
> Evidence You Collected: You collect 8 pieces, but 2 are false leads  

1️⃣ Precision = "Of the 8 pieces I collected, how many were real evidence?"

> Real evidence found: 6 pieces  
> Precision = 6/8 = 0.75 (75%)  
> "I was right 75% of the time when I thought I found evidence"  

2️⃣ Recall = "Of the 10 real pieces of evidence, how many did I find?"

> Real evidence available: 10 pieces  
> Real evidence found: 6 pieces  
> Recall = 6/10 = 0.60 (60%)  
> "I found 60% of all the evidence that existed"  

3️⃣ F1 = "What's my balanced detective performance?"

> F1 = 2 × (Precision × Recall) / (Precision + Recall)  
> F1 = 2 × (0.75 × 0.60) / (0.75 + 0.60) = 0.67  
> "My overall balanced performance is 67%"  

---
