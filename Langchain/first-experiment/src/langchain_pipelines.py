import os

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.output import PersonAnalysis, ProductRecommendation


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
