## Response Quality Metrics. The Second Set
1️⃣ BLEURT - BERT-based learned evaluation metric  
2️⃣ SacreBLEU - Standardized BLEU with proper tokenization  
3️⃣ METEOR - Synonym and paraphrase consideration  
4️⃣ CIDEr - Consensus-based evaluation  
5️⃣ CHRF - Character-level F-score for multilingual evaluation
---
### Basics

| Metric | Evolution From | Key Innovation | Best For | Platform Support | 
| ------ | ------------- | -------------- | -------- | ---------------- |
| BLEURT | BERTScore + Human Training | Learned from human judgments | General text quality | Custom Implementation | 
| SacreBLEU | BLEU | Standardized tokenization | Reproducible translation eval | Widely Supported | 
| METEOR | BLEU | Synonyms + stemming + order | Enhanced machine translation | Standard Libraries | 
| CIDEr | BLEU/ROUGE | Consensus across references | Image captioning, multiple refs | Custom Implementation | 
| CHRF | Character-level | Multilingual robustness | Cross-language evaluation | Standard Libraries |
---
### METEOR vs BLEU vs ROUGE: Core Differences

| 💡 Aspect | BLEU | ROUGE | METEOR |
|   ------ | ---- | ----- | ------ |
| Focus | Precision (exact matches) | Recall (coverage) | Balanced P+R with semantics |
| Matching | Exact n-grams only | Exact n-grams + LCS | Exact + Stem + Synonym |
| Word Order | Indirectly via n-grams | Minimal consideration | Explicit penalty | 
| Correlation with Humans | 0.817 (corpus-level) | Good for summaries | 0.964 (corpus), 0.403 (sentence) |
| Recall Weight | Equal to precision | Higher than precision | Much higher (α=0.9) |
| Best For | MT when precision matters | Summarization | General text quality | 

---
### BLEURT - BERT-based learned evaluation metric  

BLEURT is the "trained cousin" of BERTScore - it takes BERT's semantic understanding and trains it specifically on human evaluation data to predict quality scores.  
The New Revolutionary Approach  
BERTScore: Uses pre-trained BERT embeddings directly  
BLEURT: Fine-tunes BERT on human quality ratings  

**Training Process:**
1. Start with pre-trained BERT
2. Add human evaluation datasets (WMT, etc.)
3. Train to predict human quality scores
4. Result: Better correlation with human judgment

➡️ How BLEURT Works
```python
# Conceptual BLEURT process
def bleurt_score(candidate, reference):
    # Step 1: Encode both texts with fine-tuned BERT
    encoded = bleurt_model.encode(candidate, reference)
    
    # Step 2: Pass through learned scoring head
    quality_score = scoring_head(encoded)
    
    # Step 3: Return single quality score (0-1)
    return quality_score  # e.g., 0.73
```
➡️ BLEURT vs BERTScore
Same Example:
Reference: "The scientist discovered a new species"  
Candidate: "A researcher found a previously unknown organism"  

BERTScore: 
- Calculates semantic similarity using cosine similarity
- Returns: Precision=0.85, Recall=0.82, F1=0.83

BLEURT:
- Uses human-trained model to predict quality
- Returns: Single score=0.89 (closer to human judgment)

#### BLEURT. When to Use
Good At:  
✅ General text quality evaluation - Best overall correlation with humans  
✅ When you have computational resources - Slower than traditional metrics  
✅ Academic benchmarking - Gold standard for research  
✅ High-stakes evaluation - When accuracy is more important than speed  
Limitations:  
🔴 Computationally expensive - Requires GPU for reasonable speed  
🔴 Black box nature - Less interpretable than P/R/F1 breakdowns  
🔴 Model dependency - Requires specific BLEURT model weights  
---
### METEOR  Synonym and paraphrase consideration  
METEOR (Metric for Evaluation of Translation with Explicit ORdering) was created at Carnegie Mellon University in 2005 to solve BLEU's major weaknesses.  
While BLEU focuses heavily on precision, METEOR balances precision and recall and understands that "cat" and "feline" convey similar meaning.  

#### Why METEOR Was Needed
> Problem with BLEU:  
Reference:  "The cat is sleeping on the couch"  
Candidate:  "A feline is resting on the sofa"  
BLEU Score: Very LOW (no exact word matches!)  
Human Judge: "This is actually a good translation!"  

> How METEOR Works: 4-Stage Process
➡️1️⃣: Multi-Level Word Alignment
METEOR matches words through sequential modules (each stage only adds new matches).
Module 1 - Exact Match
```txt
Reference:  "The cat sat on the mat"
Candidate:  "The cat sits on a mat"
Matches:    [The, cat, on, mat]  ← Exact word matches
```
Module 2 - Stem Match (Porter Stemmer)
```txt
Remaining:  "sat" vs "sits"
Matches:    [sit-stem]  ← Both stem to "sit"
```
Module 3 - Synonym Match (WordNet)
```txt
Reference:  "The automobile is fast"
Candidate:  "The car is quick"
Matches:    [automobile≈car, fast≈quick]  ← Synonyms from WordNet
```  
➡️2️⃣: Calculate Precision & Recall  
```python
# After alignment
matched_unigrams = 4
candidate_length = 6
reference_length = 5

Precision = matched_unigrams / candidate_length = 4/6 = 0.67
Recall = matched_unigrams / reference_length = 4/5 = 0.80

# Weighted harmonic mean (recall weighted 9x more)
Fmean = (Precision * Recall) / (α * Precision + (1-α) * Recall)
Fmean = (0.67 * 0.80) / (0.1 * 0.67 + 0.9 * 0.80) = 0.79
```

➡️3️⃣: Fragmentation Penalty
METEOR penalizes translations where matched words are scattered (poor ordering):  
```
Reference:  "The quick brown fox jumped"
Candidate:  "jumped fox brown quick The"

All words match, but ordering is terrible!

Chunks = number of contiguous matched sequences
Penalty = 0.5 * (chunks / matches)³

Example:
- Good order (1 chunk):   Penalty = 0.5 * (1/5)³ = 0.001
- Bad order (5 chunks):   Penalty = 0.5 * (5/5)³ = 0.500
```
Chunk Definition: Contiguous sequence of matched words:  
```
Candidate: "The cat [gap] on mat [gap] sat"
           └─chunk1─┘  └chunk2┘  └chunk3┘
Chunks = 3 (matches are fragmented)
```
➡️4️⃣: Final METEOR Score
```python
METEOR = Fmean * (1 - Penalty)
Example:
Fmean = 0.79
Penalty = 0.15
METEOR = 0.79 * (1 - 0.15) = 0.67
Score Range: 0.0 (worst) to 1.0 (perfect)
```

#### Real Example. Calculation
```python
Reference: "The cat plays outside"
Candidate: "A cat plays outside"

Step 1: Alignment
- Exact matches: [cat, plays, outside] = 3 matches
- "The" vs "A" = no match

Step 2: Metrics
- Precision = 3/4 = 0.75
- Recall = 3/4 = 0.75
- Fmean = (0.75 * 0.75) / (0.1*0.75 + 0.9*0.75) = 0.75

Step 3: Chunks
- Matched words form 1 contiguous chunk: "cat plays outside"
- Penalty = 0.5 * (1/3)³ = 0.019

Step 4: Final
- METEOR = 0.75 * (1 - 0.019) = 0.74
```
