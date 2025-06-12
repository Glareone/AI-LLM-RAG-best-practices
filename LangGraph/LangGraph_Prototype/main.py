import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Any, TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
# Define state schema for better type safety
from typing import NotRequired

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Define state schema for better type safety
class DocumentState(TypedDict):
    content: NotRequired[str] # Made optional to avoid type errors
    chunks: NotRequired[List[str]]
    candidate_rules: NotRequired[List[Dict[str, Any]]]
    validated_rules: NotRequired[List[Dict[str, Any]]]
    confidence_score: NotRequired[float]
    iteration_count: NotRequired[int]
    processed: NotRequired[bool]

# Sample rules (in production, load from your rule database)
SAMPLE_RULES = [
    {
        "id": "R001",
        "description": "Document must contain customer identification information",
        "keywords": ["customer", "identification", "ID", "identity"],
        "category": "compliance"
    },
    {
        "id": "R002", 
        "description": "Financial amounts must be clearly stated with currency",
        "keywords": ["amount", "currency", "$", "USD", "EUR"],
        "category": "financial"
    },
    {
        "id": "R003",
        "description": "Risk assessment documentation required",
        "keywords": ["risk", "assessment", "evaluation", "analysis"],
        "category": "risk_management"
    }
]

def read_file(file_path: str) -> str:
    """Read content from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def chunk_document(state: DocumentState) -> DocumentState:
    """Split document into manageable chunks."""
    content = state["content"]
    
    # Simple chunking by paragraphs (enhance with semantic chunking later)
    chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
    
    print(f"Document split into {len(chunks)} chunks")
    
    return {
        **state,
        "chunks": chunks,
        "iteration_count": state.get("iteration_count", 0)
    }

def extract_candidate_rules(state: DocumentState) -> DocumentState:
    """Extract potentially applicable rules using keyword matching and basic NLP."""
    chunks = state["chunks"]
    candidate_rules = []
    
    for chunk in chunks:
        chunk_lower = chunk.lower()
        
        for rule in SAMPLE_RULES:
            # Simple keyword matching (replace with vector similarity later)
            keyword_matches = sum(1 for keyword in rule["keywords"] 
                                if keyword.lower() in chunk_lower)
            
            if keyword_matches > 0:
                candidate_rules.append({
                    "rule_id": rule["id"],
                    "rule_description": rule["description"],
                    "chunk": chunk,
                    "keyword_matches": keyword_matches,
                    "confidence": keyword_matches / len(rule["keywords"])
                })
    
    # Remove duplicates and sort by confidence
    unique_candidates = []
    seen = set()
    for candidate in sorted(candidate_rules, key=lambda x: x["confidence"], reverse=True):
        key = (candidate["rule_id"], candidate["chunk"][:50])  # First 50 chars as identifier
        if key not in seen:
            unique_candidates.append(candidate)
            seen.add(key)
    
    print(f"Found {len(unique_candidates)} candidate rule applications")
    
    return {
        **state,
        "candidate_rules": unique_candidates
    }

def react_rule_validation(state: DocumentState) -> DocumentState:
    """Use ReAct pattern to validate rule applicability."""
    candidate_rules = state["candidate_rules"]
    validated_rules = []
    
    for candidate in candidate_rules:
        # ReAct prompt for rule validation
        prompt = f"""
        You are a financial document compliance expert. Analyze if the following rule applies to the given text chunk.

        RULE: {candidate['rule_description']}
        
        TEXT CHUNK: {candidate['chunk']}
        
        Think step by step:
        1. THOUGHT: What does this rule require?
        2. OBSERVATION: What do I see in the text?
        3. ACTION: Does the rule apply? (YES/NO)
        4. CONFIDENCE: Rate your confidence (0.0-1.0)
        
        Respond in this exact format:
        THOUGHT: [your reasoning]
        OBSERVATION: [what you observe]
        ACTION: [YES or NO]
        CONFIDENCE: [0.0-1.0]
        """
        
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            response_text = response.content
            
            # Parse ReAct response (simplified parsing)
            lines = response_text.strip().split('\n')
            action_line = next((line for line in lines if line.startswith('ACTION:')), 'ACTION: NO')
            confidence_line = next((line for line in lines if line.startswith('CONFIDENCE:')), 'CONFIDENCE: 0.0')
            
            action = action_line.split(':', 1)[1].strip().upper()
            confidence = float(confidence_line.split(':', 1)[1].strip())
            
            if action == 'YES' and confidence > 0.5:  # Threshold for validation
                validated_rules.append({
                    **candidate,
                    "validation_confidence": confidence,
                    "llm_reasoning": response_text
                })
                
        except Exception as e:
            print(f"Error in ReAct validation: {e}")
            continue
    
    print(f"Validated {len(validated_rules)} rules")
    
    return {
        **state,
        "validated_rules": validated_rules,
        "iteration_count": state["iteration_count"] + 1
    }

def assess_confidence(state: DocumentState) -> DocumentState:
    """Assess overall confidence in rule extraction."""
    validated_rules = state["validated_rules"]
    
    if not validated_rules:
        confidence_score = 0.0
    else:
        avg_confidence = sum(rule["validation_confidence"] for rule in validated_rules) / len(validated_rules)
        # Factor in number of rules found vs expected
        coverage_factor = min(len(validated_rules) / 3, 1.0)  # Assuming we expect ~3 rules per document
        confidence_score = avg_confidence * coverage_factor
    
    print(f"Overall confidence score: {confidence_score:.2f}")
    
    return {
        **state,
        "confidence_score": confidence_score
    }

def should_continue_processing(state: DocumentState) -> str:
    """Determine next step based on confidence and iteration count."""
    confidence = state["confidence_score"]
    iterations = state["iteration_count"]
    
    # Continue if confidence is low and we haven't exceeded max iterations
    if confidence < 0.7 and iterations < 3:
        print("Confidence low, continuing processing...")
        return "continue"
    else:
        print("Processing complete!")
        return "finish"

def enrich_rules(state: DocumentState) -> DocumentState:
    """Attempt to find additional applicable rules (enrichment step)."""
    print("Attempting rule enrichment...")
    
    # Simple enrichment: look for rules we might have missed
    chunks = state["chunks"]
    current_rule_ids = {rule["rule_id"] for rule in state["validated_rules"]}
    
    # Check if we missed any obvious rules
    for rule in SAMPLE_RULES:
        if rule["id"] not in current_rule_ids:
            # More aggressive matching for enrichment
            for chunk in chunks:
                if any(keyword.lower() in chunk.lower() for keyword in rule["keywords"]):
                    # Add to validated rules with lower confidence
                    state["validated_rules"].append({
                        "rule_id": rule["id"],
                        "rule_description": rule["description"],
                        "chunk": chunk,
                        "keyword_matches": 1,
                        "confidence": 0.6,  # Lower confidence for enriched rules
                        "validation_confidence": 0.6,
                        "llm_reasoning": "Added during enrichment phase"
                    })
                    break
    
    return state

# Create the graph
workflow = StateGraph(DocumentState)

# Add nodes
workflow.add_node("chunk", chunk_document)
workflow.add_node("extract_candidates", extract_candidate_rules)
workflow.add_node("validate_rules", react_rule_validation)
workflow.add_node("assess_confidence", assess_confidence)
workflow.add_node("enrich", enrich_rules)

# Add edges
workflow.add_edge("chunk", "extract_candidates")
workflow.add_edge("extract_candidates", "validate_rules")
workflow.add_edge("validate_rules", "assess_confidence")

# Conditional routing based on confidence
workflow.add_conditional_edges(
    "assess_confidence",
    should_continue_processing,
    {
        "continue": "enrich",
        "finish": END
    }
)

# Enrichment loops back to validation
workflow.add_edge("enrich", "validate_rules")

# Set the entry point
workflow.set_entry_point("chunk")

# Compile the graph
app = workflow.compile()

def main():
    # Example file path
    file_path = Path("data/example.txt")
    content = read_file(str(file_path))
    
    # Initialize the state
    initial_state: DocumentState = {
        "content": content,
        "chunks": [],
        "candidate_rules": [],
        "validated_rules": [],
        "confidence_score": 0.0,
        "iteration_count": 0,
        "processed": False
    }
    
    # Run the workflow
    print("Starting document analysis workflow...")
    result = app.invoke(initial_state)
    
    print("\n" + "="*50)
    print("FINAL RESULTS")
    print("="*50)
    
    print(f"Total validated rules: {len(result['validated_rules'])}")
    print(f"Final confidence score: {result['confidence_score']:.2f}")
    print(f"Processing iterations: {result['iteration_count']}")
    
    print("\nValidated Rules:")
    for rule in result['validated_rules']:
        print(f"- {rule['rule_id']}: {rule['rule_description']}")
        print(f"  Confidence: {rule['validation_confidence']:.2f}")
        print(f"  Applied to: {rule['chunk'][:100]}...")
        print()

if __name__ == "__main__":
    main()