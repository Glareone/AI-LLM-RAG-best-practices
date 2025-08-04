import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from src.langchain_pipelines import create_person_analysis_pipeline, create_product_recommendation_pipeline
from src.output import SimpleExplanation

load_dotenv()

async def run_person_analysis_example():
    """Example of running the person analysis pipeline"""
    print("=== CASE 1. Person Analysis Pipeline ===. Example of running the person analysis pipeline")

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

# Return result only for demonstration purposes to specify the return type in the function signature
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
        ("system", "You are a helpful assistant that provides concise answers. Respond with JSON: {format_instructions}"),
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
    """Main function to run all examples, sync and async"""
    print("LangChain Pipeline Examples")
    print("Make sure to set OPENAI_API_KEY in your .env file")

    # Run examples
    sync_execute_chain_without_result_formatting()
    sync_execute_chain_with_pydantic_format()
    await run_person_analysis_example()
    await run_product_recommendation_example()

if __name__ == "__main__":
    asyncio.run(main())