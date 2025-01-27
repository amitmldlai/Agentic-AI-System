from pydantic import BaseModel, Field


class FoodReviewState(BaseModel):
    review_category: str = Field(
        default="",
        description="Category of the review (e.g., Good, Neutral, Bad)."
    )
    review: str = Field(
        default="",
        description="The actual content of the review provided by the customer."
    )
    restaurant_name: str = Field(
        default="",
        description="The name of the restaurant that the review is about."
    )


class DatabaseLoggerToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    feedback_message: str = Field(..., description="Feedback provided by customer")
    restaurant_name: str = Field(..., description="Name of the Restaurant")

