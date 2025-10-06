### Parameter-Efficient Fine-tuning

1. LoRA (Low-Rank Adaptation)  
    a. Rank Parameter (r) - 8-64 range, efficiency vs capacity trade-off  
    b. Alpha Scaling Factor - Typically 16-32  
    c. Target Module Selection - Query, value, key, output projections  
    d. AdaLoRA - Adaptive rank allocation   
    e. QLoRA - 4-bit quantized LoRA for memory efficiency  

2. Training Parameters
    a. Learning Rate Ranges - 1e-5 to 5e-4 for LLMs with warmup  
    b. Batch Size Optimization - 8-32 full fine-tuning, 64-128 LoRA  
    c. Sequence Length Limits - 512-4096 tokens task dependency  
    d. Weight Decay (L2 Regularization) - λ||w||² with λ = 1e-4 to 1e-2  
