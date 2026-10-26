
def calculate_score(questions, answers):
    """Returns (correct, total) for index-based multiple-choice answers."""
    correct = sum(
        answer == question.correct_index
        for question, answer in zip(questions, answers)
    )
    return correct, len(questions)


def option_from_speech(text: str):
    """Accept short answers like 'B', 'option B', or 'answer B'."""
    import re
    match = re.fullmatch(
        r"\s*(?:(?:the\s+)?(?:answer|option|letter)\s+(?:is\s+)?)?([ABCD])\s*[.!]?\s*",
        text.upper(),
    )
    return "ABCD".index(match.group(1)) if match else None
