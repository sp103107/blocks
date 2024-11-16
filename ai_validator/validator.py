import random

class AIValidator:
    def __init__(self, ethical_score_threshold=0.7):
        self.ethical_score_threshold = ethical_score_threshold

    def validate_transactions(self, transactions):
        # Mock validation logic
        validation_scores = [random.uniform(0.5, 1.0) for _ in transactions]
        avg_score = sum(validation_scores) / len(validation_scores) if transactions else 1.0
        return avg_score >= self.ethical_score_threshold, avg_score