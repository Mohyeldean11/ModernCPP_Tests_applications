# Deep Dive: Core ML & RAG Concepts

## 📊 1. TOP-K: The "Best N Results" Selector

### **What is Top-K?**

Top-K means **"Keep only the K best results"** where K is a number you choose.

### **Visual Example:**

Imagine you're searching for "vacation policy" and get these similarity scores:

```
Document A: 0.92 ⭐⭐⭐⭐⭐
Document B: 0.87 ⭐⭐⭐⭐⭐
Document C: 0.76 ⭐⭐⭐⭐
Document D: 0.65 ⭐⭐⭐
Document E: 0.43 ⭐⭐
Document F: 0.21 ⭐
Document G: 0.15 ⭐
Document H: 0.08 
```

**With top_k = 3:**
You keep only A, B, C (the top 3)

**With top_k = 5:**
You keep A, B, C, D, E (the top 5)

### **Why Use Top-K?**

#### **Problem Without Top-K:**
```python
# Return ALL results
results = search_database(query)  
# Returns 1000 documents! 🤯
# LLM gets overwhelmed
# Answer becomes confused
```

#### **Solution With Top-K:**
```python
# Return only best 3
results = search_database(query, top_k=3)
# Returns 3 most relevant documents ✅
# LLM focuses on what matters
# Answer is precise
```

### **The Trade-off:**

```
┌─────────────────────────────────────┐
│         Top-K Values                │
├─────────────────────────────────────┤
│ K=1  → Fast, Precise, Might Miss    │
│ K=3  → Balanced ✅ (Most Common)    │
│ K=5  → More Context, Slower         │
│ K=10 → Comprehensive, Risk Noise    │
│ K=50 → Too Much, Confusing          │
└─────────────────────────────────────┘
```

### **Real Code Example:**

```python
def search_similar_chunks(self, query: str, top_k: int = 10):
    # Calculate similarity for ALL chunks
    all_scores = calculate_similarity(query, all_chunks)
    # Result: [0.92, 0.87, 0.76, 0.65, 0.43, ...]
    
    # Sort from highest to lowest
    sorted_scores = sort_descending(all_scores)
    
    # Keep only top K
    top_results = sorted_scores[:top_k]
    # If top_k=3: [0.92, 0.87, 0.76]
    
    return top_results
```

### **Why top_k=3 in Your Code?**

```python
rag_context = self.get_rag_context(corrected_query, top_k=3)
```

**Reasoning:**
- ✅ Enough context for the LLM (usually 1-3 paragraphs)
- ✅ Doesn't overload the prompt (cost/speed)
- ✅ Reduces noise (irrelevant info)
- ✅ Typical LLM context: ~2000-4000 tokens

**When to adjust:**
- **Increase to 5-7**: Complex questions needing multiple sources
- **Decrease to 1**: Simple factual lookup ("What's the CEO's name?")

---

## 🌡️ 2. TEMPERATURE: The Creativity Knob

### **What is Temperature?**

Temperature controls **how random/creative the LLM's output is**.

Think of it as a creativity slider:

```
0.0 ←────────────────────→ 2.0
Robotic              Creative/Chaotic
Deterministic        Unpredictable
Factual              Imaginative
```

### **How Temperature Works (Deep Dive):**

#### **Step 1: LLM Generates Probabilities**

When generating the next word, the LLM calculates probabilities:

```
Query: "The capital of France is ___"

Without temperature:
- "Paris"     → 95% probability ⭐⭐⭐⭐⭐
- "Lyon"      → 3%  probability ⭐
- "Marseille" → 1%  probability
- "Berlin"    → 0.5% probability
- "Pizza"     → 0.1% probability 🤪
```

#### **Step 2: Apply Temperature**

Temperature **reshapes** these probabilities:

**Temperature = 0.0 (Deterministic)**
```
Always pick the highest: "Paris" (100% of the time)
```

**Temperature = 0.3 (Low - Your Code Uses This)**
```
- "Paris"     → 92% probability ⭐⭐⭐⭐⭐
- "Lyon"      → 5%  probability ⭐
- "Marseille" → 2%  probability
- "Berlin"    → 0.8% probability
- "Pizza"     → 0.2% probability
```
Mostly picks "Paris", occasionally "Lyon"

**Temperature = 1.0 (Medium)**
```
- "Paris"     → 70% probability ⭐⭐⭐⭐
- "Lyon"      → 15% probability ⭐⭐
- "Marseille" → 10% probability ⭐
- "Berlin"    → 4%  probability
- "Pizza"     → 1%  probability
```
More variety, but still reasonable

**Temperature = 2.0 (High - Creative Mode)**
```
- "Paris"     → 40% probability ⭐⭐
- "Lyon"      → 25% probability ⭐⭐
- "Marseille" → 20% probability ⭐⭐
- "Berlin"    → 10% probability ⭐
- "Pizza"     → 5%  probability 🤪
```
High chance of weird answers!

### **The Math Behind Temperature:**

```python
# Simplified version of what happens internally:

def apply_temperature(logits, temperature):
    """
    logits: raw model scores [5.2, 1.3, 0.8, ...]
    temperature: your setting
    """
    # Divide logits by temperature
    scaled_logits = logits / temperature
    
    # Convert to probabilities (softmax)
    probabilities = softmax(scaled_logits)
    
    # Sample from these probabilities
    next_token = random_choice(probabilities)
    
    return next_token
```

**What happens mathematically:**

```
Temperature = 0.1: logits / 0.1 = logits * 10
→ Amplifies differences → More deterministic

Temperature = 1.0: logits / 1.0 = logits
→ No change → Balanced

Temperature = 2.0: logits / 2.0 = logits * 0.5
→ Flattens differences → More random
```

### **Real-World Examples:**

#### **Example 1: Query Preprocessing (Your Code)**

```python
preprocessing_prompt = "Fix typos: 'vacaton policy'"
temperature = 0.1  # Very low ✅
```

**With temp=0.1:**
```
Output: "vacation policy" ✅ (correct 99% of time)
```

**With temp=1.5:**
```
Output 1: "vacation policy" ✅
Output 2: "holiday policy" (synonym)
Output 3: "time-off guidelines" (creative)
Output 4: "vacationing rules" (weird)
```
❌ Inconsistent! We want CONSISTENT corrections.

#### **Example 2: Generating HR Answer (Your Code)**

```python
answer_prompt = "Explain vacation policy based on: [context]"
temperature = 0.3  # Low but not zero ✅
```

**Why 0.3?**
- ✅ Mostly consistent wording
- ✅ Slight variation (not robotic)
- ✅ Sticks to facts
- ❌ Won't hallucinate

**With temp=0.0:**
```
"The vacation policy states that employees with less than 5 years 
receive 21 days. Employees with 5 years receive 23 days."
```
Accurate but robotic, same every time.

**With temp=0.3:**
```
"According to the policy, your vacation days depend on tenure. 
If you've been here under 5 years, you get 21 days. After 5 
years, this increases to 23 days."
```
Natural, accurate, slightly varied phrasing.

**With temp=1.5:**
```
"Great question! Vacation time is super important for work-life 
balance! 😊 You'll get anywhere from 21-30 days depending on 
how long you've been with us. Make sure to plan ahead and enjoy 
your time off! The company really values rest and relaxation..."
```
❌ Too chatty, loses precision!

### **Temperature Selection Guide:**

```
┌──────────────┬────────────────┬──────────────────┐
│ Temperature  │ Use Case       │ Example          │
├──────────────┼────────────────┼──────────────────┤
│ 0.0 - 0.2    │ Factual Tasks  │ Data extraction  │
│              │ Consistency    │ Typo fixing      │
│              │ Math/Code      │ SQL queries      │
├──────────────┼────────────────┼──────────────────┤
│ 0.3 - 0.5    │ Balanced       │ HR answers       │
│              │ Professional   │ Documentation    │
│              │ Explanations   │ Tutorials        │
├──────────────┼────────────────┼──────────────────┤
│ 0.6 - 0.9    │ Conversational │ Chatbots         │
│              │ Varied Style   │ Product reviews  │
│              │ Marketing      │ Blog posts       │
├──────────────┼────────────────┼──────────────────┤
│ 1.0 - 1.5    │ Creative       │ Story writing    │
│              │ Brainstorming  │ Poetry           │
│              │ Humor          │ Slogans          │
├──────────────┼────────────────┼──────────────────┤
│ 1.5 - 2.0    │ Experimental   │ Art prompts      │
│              │ Wild Ideas     │ Surreal content  │
│              │ (Risky!)       │ Random chaos     │
└──────────────┴────────────────┴──────────────────┘
```

---

## 🧮 3. PYTORCH TENSORS: The Math Powerhouse

### **What Are Tensors?**

A **tensor** is a multi-dimensional array of numbers. Think of it as Excel on steroids.

### **Tensor Dimensions Explained:**

#### **0D Tensor (Scalar):**
```python
x = torch.tensor(5)
# Just a single number
# Shape: ()
```

#### **1D Tensor (Vector):**
```python
x = torch.tensor([1, 2, 3, 4, 5])
# A list of numbers (like a row in Excel)
# Shape: (5,)
# Use: Word embedding for a single word
```

#### **2D Tensor (Matrix):**
```python
x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
# A table of numbers (like a spreadsheet)
# Shape: (3, 3)
# Use: Embeddings for multiple words
```

#### **3D Tensor (Cube):**
```python
x = torch.tensor([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])
# Multiple matrices stacked
# Shape: (2, 2, 2)
# Use: Batch of embeddings
```

### **Why Your Code Uses Tensors:**

```python
# From your code:
self.embeddings = torch.cat(all_embeddings, dim=0)
# Shape: (35, 768)
# 35 chunks, each with 768 dimensions
```

**Visual Representation:**
```
        Dimension 1  Dimension 2  ...  Dimension 768
Chunk 1    0.23        -0.45      ...     0.12
Chunk 2    0.15        -0.32      ...     0.08
Chunk 3    0.87         0.12      ...    -0.45
...
Chunk 35   0.34        -0.21      ...     0.67

↑ 35 rows (chunks)
↑ 768 columns (embedding dimensions)
```

### **Why Use PyTorch Tensors Instead of Lists?**

#### **Option 1: Python Lists (Slow ❌)**

```python
# Calculate similarity between query and 35 chunks
embeddings = [[0.23, -0.45, ...], [0.15, -0.32, ...], ...]  # List of lists
query = [0.12, 0.34, ...]

similarities = []
for chunk_embedding in embeddings:
    # Calculate dot product manually
    similarity = 0
    for i in range(768):
        similarity += query[i] * chunk_embedding[i]
    similarities.append(similarity)

# Time: ~500ms for 35 chunks ❌
```

#### **Option 2: PyTorch Tensors (Fast ✅)**

```python
# Same calculation with tensors
embeddings = torch.tensor(embeddings)  # Shape: (35, 768)
query = torch.tensor(query)            # Shape: (768,)

similarities = torch.matmul(embeddings, query)
# Time: ~5ms for 35 chunks ✅ (100x faster!)
```

### **Key Tensor Operations in Your Code:**

#### **1. Creating Tensors from Text:**

```python
texts = ["vacation policy", "sick leave", "benefits"]
embeddings = model.encode(texts, convert_to_tensor=True)
# Result: torch.tensor with shape (3, 768)
```

#### **2. Concatenating Tensors:**

```python
batch1 = torch.tensor([[1, 2], [3, 4]])  # Shape: (2, 2)
batch2 = torch.tensor([[5, 6], [7, 8]])  # Shape: (2, 2)

combined = torch.cat([batch1, batch2], dim=0)
# Result shape: (4, 2)
# [[1, 2],
#  [3, 4],
#  [5, 6],
#  [7, 8]]
```

**In your code:**
```python
all_embeddings = []
for i in range(0, len(texts), 32):
    batch_embeddings = model.encode(batch, convert_to_tensor=True)
    all_embeddings.append(batch_embeddings)

self.embeddings = torch.cat(all_embeddings, dim=0)
```

This processes chunks in batches of 32, then stacks them vertically.

#### **3. Cosine Similarity:**

```python
query_embedding = torch.tensor([0.5, 0.3, 0.2])  # Shape: (3,)
chunk_embeddings = torch.tensor([
    [0.6, 0.4, 0.1],
    [0.1, 0.8, 0.3],
    [0.5, 0.3, 0.2]
])  # Shape: (3, 3)

similarities = util.pytorch_cos_sim(query_embedding, chunk_embeddings)
# Result: [0.95, 0.43, 1.00]
#         ↑     ↑     ↑
#      Similar  Not  Identical
```

**The formula:**
```
cosine_similarity = (A · B) / (||A|| × ||B||)

Where:
A · B = dot product
||A|| = length (magnitude) of vector A
||B|| = length (magnitude) of vector B
```

### **Why Tensors Are Faster:**

#### **1. Vectorization:**
```python
# Python loops (slow)
result = 0
for i in range(1000):
    result += a[i] * b[i]

# Tensor operation (fast)
result = torch.dot(a, b)
# No loops! All at once!
```

#### **2. GPU Acceleration:**
```python
# CPU: Process one at a time
for item in data:
    process(item)  # 1000 items = 1000 steps

# GPU: Process many simultaneously
gpu_data = data.to('cuda')
process(gpu_data)  # 1000 items = 10 steps (100 parallel cores)
```

#### **3. Memory Efficiency:**

```python
# Python list: Scattered memory
list_data = [1, 2, 3, 4, 5]
# Memory: [1]--[2]--[3]--[4]--[5] (slow to access)

# Tensor: Contiguous memory
tensor_data = torch.tensor([1, 2, 3, 4, 5])
# Memory: [1][2][3][4][5] (fast to access)
```

### **Real Performance Comparison:**

```python
import time
import numpy as np
import torch

# Test data: 10,000 vectors of 768 dimensions
n = 10000
dims = 768

# Python lists
list_data = [[random() for _ in range(dims)] for _ in range(n)]
start = time.time()
result = [[a * b for a, b in zip(row1, row2)] for row1, row2 in ...]
print(f"Lists: {time.time() - start:.2f}s")  # ~45 seconds

# NumPy arrays
np_data = np.random.rand(n, dims)
start = time.time()
result = np_data @ np_data.T
print(f"NumPy: {time.time() - start:.2f}s")  # ~2 seconds

# PyTorch tensors (CPU)
torch_data = torch.randn(n, dims)
start = time.time()
result = torch.mm(torch_data, torch_data.T)
print(f"PyTorch CPU: {time.time() - start:.2f}s")  # ~1 second

# PyTorch tensors (GPU)
torch_data = torch.randn(n, dims).cuda()
start = time.time()
result = torch.mm(torch_data, torch_data.T)
torch.cuda.synchronize()
print(f"PyTorch GPU: {time.time() - start:.2f}s")  # ~0.05 seconds!
```

**Result:**
```
Lists:       45.0s ❌
NumPy:        2.0s ⚠️
PyTorch CPU:  1.0s ✅
PyTorch GPU:  0.05s ⚡ (900x faster than lists!)
```

---

## 🔍 4. RAG (Retrieval-Augmented Generation): The Complete System

### **What is RAG?**

RAG = **Combining search with AI generation**

Traditional LLM vs. RAG:

```
┌─────────────────────────────────────────┐
│         TRADITIONAL LLM                 │
├─────────────────────────────────────────┤
│ User: "What's our vacation policy?"     │
│                                         │
│ LLM: "Based on my training data from   │
│      2023, typical companies offer...   │
│      [might hallucinate/be outdated]"   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         RAG SYSTEM                      │
├─────────────────────────────────────────┤
│ User: "What's our vacation policy?"     │
│                                         │
│ Step 1: RETRIEVE from documents         │
│ → Search finds: "Employees with <5      │
│   years get 21 days..."                 │
│                                         │
│ Step 2: AUGMENT the prompt              │
│ → "Based on this document: [policy],    │
│   answer the question"                  │
│                                         │
│ Step 3: GENERATE answer                 │
│ → LLM: "According to your company's     │
│   vacation policy document, you get     │
│   21 days if you've been here less      │
│   than 5 years..."                      │
└─────────────────────────────────────────┘
```

### **The RAG Pipeline (Step-by-Step):**

#### **PHASE 1: Indexing (One-Time Setup)**

```
┌──────────────┐
│ Raw Document │
│  "Vacation   │
│   Policy.pdf"│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ 1. LOAD DOCUMENT     │
│    Read PDF/Text     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 2. CHUNK TEXT        │
│    Split into pieces │
│    (500-1000 chars)  │
└──────┬───────────────┘
       │
       ▼ Example chunks:
       Chunk 1: "Employees with <5 years get 21 days..."
       Chunk 2: "Vacation requests must be submitted..."
       Chunk 3: "Emergency leave is limited to 6 days..."
       │
       ▼
┌──────────────────────┐
│ 3. CREATE EMBEDDINGS │
│    Convert to vectors│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 4. STORE IN DATABASE │
│    Vector DB         │
│    [0.23, -0.45,...] │
│    [0.15, -0.32,...] │
│    [0.87,  0.12,...] │
└──────────────────────┘
```

**In your code:**
```python
def initialize_hardcoded_database(self):
    # Pre-chunked data
    hardcoded_chunks = [
        {
            "text": "4. VACATION LEAVE POLICY...",
            "source": "Vacation Policy.pdf",
            "keywords": ["vacation", "leave", "annual"]
        },
        # ... more chunks
    ]
    self.vector_db = hardcoded_chunks
    self.create_embeddings()  # Convert all to vectors
```

#### **PHASE 2: Query Time (Every User Question)**

```
┌──────────────┐
│ User Query   │
│ "How many    │
│  vacation    │
│  days?"      │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ 1. PREPROCESS QUERY  │
│    Fix typos         │
│    "vacation days" ✓ │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 2. EMBED QUERY       │
│    [0.28, -0.41,...] │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 3. SIMILARITY SEARCH │
│    Compare query     │
│    embedding with    │
│    all chunk         │
│    embeddings        │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 4. RANK RESULTS      │
│    Chunk 1: 0.92 ⭐⭐⭐│
│    Chunk 5: 0.87 ⭐⭐⭐│
│    Chunk 3: 0.76 ⭐⭐⭐│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 5. GET TOP-K (3)     │
│    Take best 3 chunks│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 6. BUILD CONTEXT     │
│    "Context:         │
│    Chunk 1 text...   │
│    Chunk 5 text...   │
│    Chunk 3 text..."  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 7. CREATE PROMPT     │
│    "You are an HR    │
│    assistant. Based  │
│    on this context:  │
│    [context],        │
│    answer: [query]"  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 8. SEND TO LLM       │
│    Qwen2.5-coder     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 9. GENERATE ANSWER   │
│    "Based on your    │
│    company's policy, │
│    employees with    │
│    less than 5 years │
│    receive 21 days..." │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ 10. RETURN TO USER   │
└──────────────────────┘
```

### **Why RAG is Powerful:**

#### **Problem 1: LLMs Hallucinate**

**Without RAG:**
```
User: "What's our vacation policy?"
LLM: "Most companies offer 15-20 days of PTO..."
❌ Generic answer, not YOUR company
```

**With RAG:**
```
User: "What's our vacation policy?"
RAG: [Retrieves actual company document]
LLM: "According to your company policy document,
     employees with less than 5 years get 21 days..."
✅ Accurate, grounded in real docs
```

#### **Problem 2: LLMs Have Outdated Knowledge**

**Without RAG:**
```
User: "Who's the current CEO?"
LLM: "As of my training data in 2023, the CEO was John..."
❌ Might be outdated
```

**With RAG:**
```
User: "Who's the current CEO?"
RAG: [Retrieves latest company doc]
LLM: "According to the latest organizational chart,
     the current CEO is Jane Smith..."
✅ Always up-to-date
```

#### **Problem 3: LLMs Can't Access Private Data**

**Without RAG:**
```
User: "What's our internal hiring process?"
LLM: "I don't have access to your internal documents..."
❌ Can't help
```

**With RAG:**
```
User: "What's our internal hiring process?"
RAG: [Retrieves from internal HR database]
LLM: "According to your Internal Mobility Policy,
     employees must complete 6 months and have
     a 'B' performance rating..."
✅ Accesses private knowledge
```

### **RAG vs. Fine-Tuning:**

```
┌─────────────────────────────────────────┐
│           FINE-TUNING                   │
├─────────────────────────────────────────┤
│ Pros:                                   │
│ ✅ LLM learns your data deeply          │
│ ✅ No retrieval step (faster)           │
│                                         │
│ Cons:                                   │
│ ❌ Expensive (GPU hours)                │
│ ❌ Static (retrain for updates)         │
│ ❌ Risk of overfitting                  │
│ ❌ Can still hallucinate                │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│              RAG                        │
├─────────────────────────────────────────┤
│ Pros:                                   │
│ ✅ Cheap (just embed docs)              │
│ ✅ Dynamic (add docs anytime)           │
│ ✅ Transparent (see sources)            │
│ ✅ Grounded (less hallucination)        │
│                                         │
│ Cons:                                   │
│ ❌ Retrieval step (slightly slower)     │
│ ❌ Quality depends on search            │
└─────────────────────────────────────────┘
```

### **Advanced RAG Techniques (Beyond Your Code):**

#### **1. Hybrid Search (Your code uses this! ✅)**

```python
# Your code combines:
semantic_score = 0.92   # Meaning-based
keyword_score = 0.85    # Exact match
text_score = 0.73       # Simple overlap

combined = 0.6*semantic + 0.3*keyword + 0.1*text
```

#### **2. Re-ranking (Not in your code)**

```
Initial search → Top 100 results
↓
Re-rank with better model → Top 3 best results
↓
Send to LLM
```

#### **3. Query Expansion (Not in your code)**

```
User asks: "PTO"
↓
Expand to: "PTO OR vacation OR leave OR time-off"
↓
Better search results
```

#### **4. Metadata Filtering (Partially in your code)**

```python
# Your code tracks:
chunk['source'] = "Vacation Policy.pdf"
chunk['keywords'] = ["vacation", "annual", "leave"]

# Could add:
chunk['date'] = "2024-01-01"
chunk['department'] = "HR"
chunk['country'] = "Egypt"

# Then filter:
results = search(query, filters={"country": "Egypt"})
```

### **RAG Performance Metrics:**

```
┌────────────────────────────────────────┐
│         RETRIEVAL QUALITY              │
├────────────────────────────────────────┤
│ Precision: Relevant docs / Total docs  │
│ Example: 3 relevant / 3 returned = 100%│
│                                        │
│ Recall: Relevant found / All relevant  │
│ Example: 3 found / 5 exist = 60%      │
│                                        │
│ MRR (Mean Reciprocal Rank):           │
│ 1 / (position of first relevant)      │
│ Example: First result relevant = 1.0   │
└────────────────────────────────────────┘
```

### **Your RAG System's Strengths:**

```python
# 1. Query Preprocessing ✅
corrected_query = self.preprocess_query(query)
# Unique! Most RAG systems don't fix typos

# 2. Hybrid Search ✅
combined_score = 0.6*semantic + 0.3*keyword + 0.1*text
# Better than pure semantic search

# 3. Confidence Thresholding ✅
if similarity < 0.5:
    return "No information found"
# Prevents bad answers

# 4. Multi-Level Fallback ✅
try:
    llm_answer()
except