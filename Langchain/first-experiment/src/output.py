from typing import Optional, List

from pydantic import BaseModel, Field


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
    confidence_score: float = Field(description="Confidence in recommendation (0-1)", ge=0, le=1)


class SimpleExplanation(BaseModel):
    """PYDANTIC: A simple explanation model for pydantic output"""
    topic: str = Field(description="The topic being explained")
    explanation: str = Field(description="Simple explanation of the topic")
    key_points: List[str] = Field(description="3-5 key points about the topic")
    difficulty_level: str = Field(description="Difficulty level: beginner, intermediate, or advanced")
    confidence_score: float = Field(description="Confidence in explanation (0-1)", ge=0, le=1)
