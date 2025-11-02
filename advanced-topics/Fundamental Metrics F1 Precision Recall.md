## Fundamental Metrics of Response.

1️⃣ Precision: "Of what I found, how much was actually good?"  
2️⃣ Recall: "Of all the good stuff that exists, how much did I find?"  
3️⃣ F1: "What's the balanced score between precision and recall?".    
  - Harmonic F1

4️⃣ [Precision vs Recall Trade-off](#precision-vs-recall-trade-off)  
  - [Imbalance Confusion](#imbalance-confusion)

5️⃣ F-beta score. Difference between F-beta and F1.
---

### Basic metrics understanding

|              |             |             |             |
|  ----------- | ----------- | ----------- | ----------- |
|              |             |             |   ACTUAL    |
|  PREDICTED   | Positive    | TP          |   FP        |
|              | Negative    | FN          |   TN        |

- TP (True Positives): Correctly identified positive cases
- FP (False Positives): Incorrectly identified as positive (Type I Error)
- FN (False Negatives): Missed positive cases (Type II Error)
- TN (True Negatives): Correctly identified negative cases

**Precision Formula:**
```
Precision = TP / (TP + FP)
         = True Positives Found / Total Positives
         = "Of what I predicted as positive, how much was actually positive?"
```
**Recall Formula:**
```
Recall = TP / (TP + FN)
       = True Positives / Total Actual Positives  
       = "Of all actual positives, how many did I find?"
```
**F1 Score Formula:**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
   = 2PR / (P + R)
   = Harmonic Mean of Precision and Recall
```
---
### Q&A Section

**Q1: Are P/R/F1 everywhere? Are they universal?**   
A1: Yes, they are absolutely universal! These three metrics appear in:  

1️⃣ Google Search (how good are search results?)  
2️⃣ Medical diagnosis (cancer detection accuracy)  
3️⃣ Email spam filtering (catch spam without blocking good emails)  
4️⃣ Netflix recommendations (suggest movies you'll actually like)  
5️⃣ AI model evaluation (assess language model performance)  

**Q2: What the difference between precision and Recall? Their formulas look similar.**  
A2: Both are indeed "success rate" calculations, but they're measuring success against different denominators:  
- Precision: Correct Predictions / Total Predictions Made. Precision: `"Of My Predictions, How Many Were Right?"`  
- Recall: Correct Detections / Total Things That Actually Exist. `"Of All Real Cases, How Many Did I Find?"`  


---
#### Example 1
1️⃣ Precision
```
Example: Email Spam Detection
- You flagged 100 emails as spam
- 85 were actually spam, 15 were legitimate emails

Precision = 85 / (85 TP + 15 FP) = 85/100 = 0.85 (85%)

Interpretation: "When I flag something as spam, I'm right 85% of the time"
```
2️⃣ Recall
```
Example: Security Threat Detection  
- There were 120 actual threats in the system
- Your system detected 90 of them, missed 30

Recall = 90 / (90 TP + 30 FN) = 90/120 = 0.75 (75%)

Interpretation: "I caught 75% of all real threats"
```

3️⃣ F1: Ariphmetic Mean
```
(Precision + Recall) / 2
```
3️⃣ F1: Harmonic Mean
- Example 1: Balanced Performance
```

Precision = 0.8, Recall = 0.8
Arithmetic Mean = (0.8 + 0.8) / 2 = 0.8
Harmonic Mean (F1) = 2 × (0.8 × 0.8) / (0.8 + 0.8) = 1.28/1.6 = 0.8
Same result ✅
```
- Example 2: Unbalanced Performance  
```

Precision = 0.9, Recall = 0.1
Arithmetic Mean = (0.9 + 0.1) / 2 = 0.5
Harmonic Mean (F1) = 2 × (0.9 × 0.1) / (0.9 + 0.1) = 0.18/1.0 = 0.18
F1 punishes the low recall! ✅
```
---
#### Precision vs Recall Trade-off
```python
# High Precision, Low Recall (CONSERVATIVE)
# "Only include generated facts I'm very confident about"
Precision: 0.95 (95% of included facts are correct)
Recall: 0.60 (only caught 60% of all correct facts)

Result: 
✅ Very few wrong facts make it through
❌ Miss many correct facts
➡️ Good for: Risk assessment, compliance, medical diagnosis

# Low Precision, High Recall (AGGRESSIVE)
# "Include anything that might be correct"
Precision: 0.60 (60% of included facts are correct, 40% are wrong!)
Recall: 0.95 (caught 95% of all correct facts)

Result:
❌ Many wrong facts get through
✅ Don't miss many correct facts
➡️ Good for: Initial screening, search, brainstorming
```

### Imbalance Confusion
For different AI Systems and even for different parts of your AI system you may need different focus, sometimes Recall matters, sometimes Precision, but usually the balance between two.
```
Scenario 3: Class Imbalance Confusion
python# Maybe they have:
# - 1000 correct facts in data (positive class)
# - 100 wrong facts generated (negative class)

# If validator accepts everything:
# Recall = 1000/1000 = 1.0 (perfect!)
# But Precision = 1000/(1000 + 100) = 0.91

# They see: "We captured all correct facts!" (high recall)
# They miss: "But we also included 100 wrong facts!" (lower precision)
```
---
### Example 2
Medical Cancer Screening  
Scenario: Testing 1000 patients for cancer  

- 100 patients actually have cancer
- Your test flags 120 patients as having cancer
- Of those 120 flagged, 80 actually have cancer
  
**Step 1: Build the Confusion Matrix**  
                    ACTUAL
                 Cancer  No Cancer
PREDICTED Cancer   80      40      (TP=80, FP=40)
       No Cancer   20     860      (FN=20, TN=860)
  
**Step 2: Calculate Each Metric**  
1️⃣ Precision = TP / (TP + FP) = 80 / (80 + 40) = 80/120 = 0.667 (66.7%)  
"Of patients I flagged as having cancer, 66.7% actually have it"  

2️⃣ Recall = TP / (TP + FN) = 80 / (80 + 20) = 80/100 = 0.80 (80%)  
"I detected 80% of all actual cancer cases"  

3️⃣ F1 = 2 × (0.667 × 0.80) / (0.667 + 0.80) = 2 × 0.534 / 1.467 = 0.727 (72.7%)  
"My balanced diagnostic performance is 72.7%"  

---

#### F1/P/R for BERTScore
1️⃣ F1 Score - Your primary metric (balanced view)  
- 0.85: Excellent quality  
- 0.70-0.84: Good quality  
- < 0.70: Needs improvement
  
2️⃣ Precision - Focus when false positives are expensive  
- "Only flag as good if you're confident"  
- Medical diagnosis, fraud detection
  
3️⃣ Recall - Focus when missing things is expensive  
- "Better safe than sorry"  
- Security monitoring, medical screening  

---
#### F-β beta score
- F-β = 1**: F(1.0) Precision and recall equally important. Equal to F1.
  * β = 1.0: "...give me equal parts of both". [Precision: █████] [Recall: █████]
- F-β > 1**: F(2.0) Recall is MORE important than precision.
  * β = 2.0: "...give me mostly recall with a side of precision". [Precision: ██] [Recall: ████████]
- F-β < 1**: F(0.5) Precision is MORE important than recall
  * β = 0.5: "...give me mostly precision with a side of recall". [Precision: ████████] [Recall: ██]

```python
β = 0.5  (F0.5)
├─ Precision weight: 4x
├─ Recall weight: 1x
└─ "I care 4x more about precision than recall"

β = 1.0  (F1)
├─ Precision weight: 1x
├─ Recall weight: 1x
└─ "I care equally about both"

β = 2.0  (F2)
├─ Precision weight: 1x
├─ Recall weight: 4x
└─ "I care 4x more about recall than precision"
```

#### F-beta score in examples
```python
# Scenario 1: Very strict validator
Precision = 0.95  # 95% of accepted facts are correct ✓
Recall = 0.50     # Only caught 50% of all correct facts ✗

# Scenario 2: Very lenient validator  
Precision = 0.60  # Only 60% of accepted facts are correct ✗
Recall = 0.95     # Caught 95% of all correct facts ✓
```
```python
# Question: which metric, F1 or F-beta, is the "better"?
# Answer: Depends on your use case!
- F1 score says: "They're equally important"
F1 = 2 × (Precision × Recall) / (Precision + Recall)

# It's the harmonic mean - balances both equallyBut what if they're NOT equally important for your use case? That's where F-beta comes in!F-beta Score FormulapythonF_β = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```
F-beta is how much MORE you care about recall than precision
```python
F_β = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```

#### Understanding where to use which F-beta score
💡 **β = 0.5 - Precision Matters More**  
1️⃣ Medical diagnosis (cancer screening)  
  - FP: Tell healthy person they have cancer → unnecessary treatment, stress  
  - FN: Miss cancer → delayed treatment  
  - But you can retest, so FP is worse in initial screening  

2️⃣ Spam detection (aggressive)  
  - FP: Important email goes to spam → miss critical information  
  - FN: Spam gets through → minor annoyance  

3️⃣ KYC/AML compliance  
  - FP: Accept high-risk customer as low-risk → regulatory violation, fraud  
  - FN: Reject valid customer → manual review, slower process  

4️⃣ Fraud detection (when you'll investigate anyway)  
  - FP: Flag legitimate transaction → customer inconvenience  
  - FN: Miss fraud → gets caught later in review

💡 **β = 1.0 (F1) - Equal Importance**  
1️⃣ General classification tasks  
2️⃣ Search engines (balanced relevance)  
3️⃣ When you're unsure of the cost ratio  
4️⃣ Academic benchmarks (default choice)  

💡 **β = 2.0 (F2) - Recall Matters More**  
1️⃣ Cancer screening (when affordable to retest)  
   - FP: Retest will catch error → minor inconvenience  
   - FN: Miss cancer → potentially fatal  
   
2️⃣ Security threat detection  
   - FP: Investigate false alarm → wasted time  
   - FN: Miss actual threat → security breach  
   
3️⃣ Search/Retrieval systems  
   - FP: Show irrelevant results → user ignores them  
   - FN: Miss relevant results → user never sees what they need  
   
4️⃣ Initial fact extraction (before validation)  
   - FP: Extract noise → filter it out later  
   - FN: Miss facts → lost forever  
