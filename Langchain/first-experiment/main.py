import os
import asyncio
from typing import List, Optional, Any
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

# Step 3: Define Pydantic models for structured output
class PersonAnalysis(BaseModel):
    """PYDANTIC: Analysis of a person's characteristics for pydantic output"""
    name: str = Field(description="Person's name")
    age_estimate: Optional[int] = Field(description="Estimated age range", ge=0, le=120)
    profession: Optional[str] = Field(description="Likely profession or role")
    personality_traits: List[str] = Field(description="Key personality traits identified")
    confidence_score: float = Field(description="Confidence in analysis (0-1)", ge=0, le=1)

class ProductRecommendation(BaseModel):
    """PYDANTIC: Product recommendation based on user preferences for pydantic output"""
    product_name: str = Field(description="Name of the recommended product")
    category: str = Field(description="Product category")
    price_range: str = Field(description="Expected price range")
    reason: str = Field(description="Why this product is recommended")
    alternatives: List[str] = Field(description="Alternative product suggestions")

class SimpleExplanation(BaseModel):
    """PYDANTIC: A simple explanation model for pydantic output"""
    topic: str = Field(description="The topic being explained")
    explanation: str = Field(description="Simple explanation of the topic")
    key_points: List[str] = Field(description="3-5 key points about the topic")
    difficulty_level: str = Field(description="Difficulty level: beginner, intermediate, or advanced")

def create_person_analysis_pipeline():
    """Creates a pipeline for analyzing person descriptions"""

    # Step 1: Create prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert human behavior analyst. 
        Analyze the given person description and provide insights about their characteristics.

        Context: {context}
        Analysis Focus: {focus_area}

        {format_instructions}"""),
        ("human", "Please analyze this person: {person_description}")
    ])

    # Step 2: Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Step 3: Create output parser
    output_parser = PydanticOutputParser(pydantic_object=PersonAnalysis)

    # Create the chain
    chain = prompt_template | llm | output_parser

    return chain, output_parser


def create_product_recommendation_pipeline():
    """Creates a pipeline for product recommendations"""

    # Step 1: Create prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are a product recommendation expert.
        Based on the user's preferences and requirements, suggest the best product.

        Budget Range: {budget}
        User Type: {user_type}
        Special Requirements: {requirements}

        {format_instructions}"""),
        ("human", "I'm looking for: {product_query}")
    ])

    # Step 2: Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Step 3: Create output parser
    output_parser = PydanticOutputParser(pydantic_object=ProductRecommendation)

    # Create the chain
    chain = prompt_template | llm | output_parser

    return chain, output_parser


async def run_person_analysis_example():
    """Example of running the person analysis pipeline"""
    print("=== CASE 1. Person Analysis Pipeline ===")

    chain, parser = create_person_analysis_pipeline()

    try:
        result = await chain.ainvoke({
            "person_description": "John is a 35-year-old software engineer who loves hiking, reads technical blogs daily, and prefers working in small teams. He's very detail-oriented and often stays late to perfect his code.",
            "context": "Professional environment assessment",
            "focus_area": "Work style and team compatibility",
            "format_instructions": parser.get_format_instructions()
        })

        print(f"Analysis Result:")
        print(f"Name: {result.name}")
        print(f"Age Estimate: {result.age_estimate}")
        print(f"Profession: {result.profession}")
        print(f"Personality Traits: {', '.join(result.personality_traits)}")
        print(f"Confidence Score: {result.confidence_score}")

    except Exception as e:
        print(f"❌ Execution Failed. Error in person analysis: {e}")

# ✅ CORRECT: Annotate the actual return value, not the coroutine wrapper
# ❌ WRONG: Don't include Coroutine/Awaitable in the annotation
async def run_product_recommendation_example() -> Optional[AIMessage]:
    """Example of running the product recommendation pipeline"""
    print("\n=== CASE 2. Product Recommendation Pipeline ===")

    chain, parser = create_product_recommendation_pipeline()

    try:
        result = await chain.ainvoke({
            "product_query": "A laptop for software development and occasional gaming",
            "budget": "$1000-2000",
            "user_type": "Software Developer",
            "requirements": "Good keyboard, multiple monitors support, long battery life",
            "format_instructions": parser.get_format_instructions()
        })

        print(f"Recommendation Result:")
        print(f"Product: {result.product_name}")
        print(f"Category: {result.category}")
        print(f"Price Range: {result.price_range}")
        print(f"Reason: {result.reason}")
        print(f"Alternatives: {', '.join(result.alternatives)}")

        # Return result only for demonstration purposes
        return result

    except Exception as e:
        print(f"❌ Execution Failed. Error in product recommendation: {e}")
        # Return result only for demonstration purposes
        return None

def sync_execute_chain_without_result_formatting() -> None:
    """Synchronous example for simpler use cases"""
    print("\n=== CASE 3. Synchronous Simple Example ===")

    # Simple prompt template
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that provides concise answers."),
        ("human", "Explain {topic} in simple terms.")
    ])

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Simple chain without structured output
    chain = prompt | llm

    try:
        result = chain.invoke({"topic": "machine learning"})
        print(f"Simple Response: {result.content}")

    except Exception as e:
        print(f"❌ Execution Failed. Error in sync example: {e}")

def sync_execute_chain_with_pydantic_format() -> Optional[AIMessage]:
    """Sync example with Pydantic output parser"""
    # Simple prompt template
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that provides concise answers."),
        ("human", "Explain {topic} in simple terms.")
    ])

    # Create the output parser
    output_parser = PydanticOutputParser(pydantic_object=SimpleExplanation)

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Chain: prompt -> llm -> parser
    chain = prompt | llm | output_parser

    try:
        # Execute the chain
        result = chain.invoke({
            "topic": "generative AI",
            "format_instructions": output_parser.get_format_instructions()
        })

        print(f"Parsed result type: {type(result)}")
        print(f"Topic: {result.topic}")
        print(f"Explanation: {result.explanation}")
        print(f"Key Points: {result.key_points}")
        print(f"Difficulty: {result.difficulty_level}")
        # Return result only for demonstration purposes, to specify the return type in the function signature
        return result

    except OutputParserException as e:
        print(f"❌ Execution Failed. Parser failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Execution Failed. Another error: {e}")
        return None

async def main():
    """Main function to run all examples"""
    print("LangChain Pipeline Examples")
    print("Make sure to set OPENAI_API_KEY in your .env file")

    # Run examples
    sync_execute_chain_without_result_formatting()
    sync_execute_chain_with_pydantic_format()
    await run_person_analysis_example()
    await run_product_recommendation_example()

if __name__ == "__main__":
    asyncio.run(main())