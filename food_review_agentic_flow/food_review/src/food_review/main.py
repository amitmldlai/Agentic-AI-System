from crewai.flow.flow import Flow, listen, start, router, and_
from food_review.src.food_review.crews.good_review.good_crew import GoodFeedBackCrew
from food_review.src.food_review.crews.bad_review.bad_crew import BadFeedBackCrew
from food_review.src.food_review.crews.neutral_review.neutral_crew import NeutralFeedbackCrew
from litellm import completion
from models import FoodReviewState
from dotenv import load_dotenv

load_dotenv()


class FoodReviewFlow(Flow[FoodReviewState]):
    model = "gpt-4o"

    @start()
    def take_review_input(self):
        self.state.review = input("""
            Thank You for ordering the food, We are eager to hear the review of the food you just tasted?, 
            Please comment along with restaurant name :) """)
        return self.state.review

    @listen(take_review_input)
    def categorize_review(self):
        # print("Categorising the Review into good, bad & neutral")

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Here is the review user has provided: {self.state.review}. Please categorize it into one of the following: Good, Neutral, or Bad. "
                               f"Respond with only one of those choices, do not add any extra text"
                },
            ],
        )
        print(response["choices"][0]["message"]["content"])
        self.state.review_category = response["choices"][0]["message"]["content"]

    @listen(take_review_input)
    def fetch_restaurant_name(self):

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Please extract the restaurant name from the review provided: {self.state.review}. "
                               f"Do not add any extra text if restaurant name is available, "
                               f"respond with the name; otherwise, return an empty string (''). ",
                },
            ],
        )

        self.state.restaurant_name = response["choices"][0]["message"]["content"]

    @router(and_(fetch_restaurant_name, categorize_review))
    def second_method(self):
        if self.state.review_category == 'Good':
            return "Good"
        elif self.state.review_category == 'Neutral':
            return "Neutral"
        else:
            return "Bad"

    @listen("Good")
    def good_feedback_method(self):
        result = GoodFeedBackCrew().crew().kickoff()
        print(result.raw)

    @listen("Bad")
    def bad_feedback_method(self):
        result = BadFeedBackCrew().crew().kickoff(
            inputs={"review": self.state.review, "restaurant_name": self.state.restaurant_name})
        print(result.raw)

    @listen("Neutral")
    def neutral_feedback_method(self):
        result = NeutralFeedbackCrew().crew().kickoff()
        print(result.raw)


def kickoff():
    poem_flow = FoodReviewFlow()
    poem_flow.kickoff()


if __name__ == "__main__":
    kickoff()
