
# All the required imports for the solution
from datetime import datetime
import re
import calendar


class HistoryQuiz:
    def create_history_question(self, topic):
        """Return a short question that expects a specific date as an answer."""
        topic_str = str(topic).strip()
        if topic_str.lower() in ("world war 2", "world war ii", "ww2", "wwii"):
            return "On what date did World War 2 (the Second World War) end?"
        return f"On what date did {topic_str} occur or end?"

    def get_AI_answer(self, question):
        """Return a deterministic datetime for a known question.

        This function does not call external services; it uses a small lookup and
        simple heuristics to return a datetime object.
        """
        q = (question or "").lower()
        if any(k in q for k in ("world war 2", "world war ii", "ww2", "wwii")):
            return datetime(1945, 9, 2)

        # Try to extract a 4-digit year if present and return Jan 1 of that year
        m = re.search(r"(19|20)\d{2}", question)
        if m:
            year = int(m.group(0))
            return datetime(year, 1, 1)

        # Fallback to today
        return datetime.now()

    def get_user_answer(self, question):
        """Prompt the user for Year, Month and Day and return a datetime."""
        print("Question:\n", question)
        print("Please enter the date you think is correct.")

        def ask_int(prompt, min_val, max_val):
            while True:
                try:
                    val = input(prompt).strip()
                    v = int(val)
                    if v < min_val or v > max_val:
                        raise ValueError()
                    return v
                except Exception:
                    print(f"Please enter an integer between {min_val} and {max_val}.")

        year = ask_int("Year (e.g. 1945): ", 1, 9999)
        month = ask_int("Month (1-12): ", 1, 12)
        max_day = calendar.monthrange(year, month)[1]
        day = ask_int(f"Day (1-{max_day}): ", 1, max_day)
        return datetime(year, month, day)

    def check_user_answer(self, user_answer, ai_answer):
        """Compare two datetimes and print/return a (days, seconds) difference."""
        if not isinstance(user_answer, datetime) or not isinstance(ai_answer, datetime):
            raise TypeError("Both answers must be datetime objects")

        delta = user_answer - ai_answer
        days = abs(delta.days)
        seconds = abs(delta.seconds)
        print(f"AI answer: {ai_answer.date()}")
        print(f"Your answer: {user_answer.date()}")
        print(f"Difference: {days} day(s) and {seconds} second(s)")
        return days, seconds


if __name__ == "__main__":
    quiz_bot = HistoryQuiz()
    question = quiz_bot.create_history_question(topic='World War 2')
    ai_answer = quiz_bot.get_AI_answer(question)
    user_answer = quiz_bot.get_user_answer(question)
    result = quiz_bot.check_user_answer(user_answer, ai_answer)
    print('\nResult (days, seconds):', result)