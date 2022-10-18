class MentalMathsTrainer:
    def __init__(self):
        self.question_amount = 10
        self.question_types = {
            "addition": {
                "shorthand": "a",
                "symbol": "+",
                "min_nums": 2
            },
            "subtraction": {
                "shorthand": "s",
                "symbol": "-",
                "min_nums": 2
            },
            "multiplication": {
                "shorthand": "m",
                "symbol": "×",
                "min_nums": 2
            },
            "division": {
                "shorthand": "d",
                "symbol": "÷",
                "min_nums": 2
            },
            "base": {
                "shorthand": "b",
                "min_nums": 1
            }
        }
        self.question_type = "random"
        self.base_bits = 4
        self.history_file_name = "history.json"
        self.history = None

    def load_json(self, file_name: str = None) -> dict:
        # Import json for loading the json file
        import json

        # Set the file name if not chosen
        file_name = file_name or self.history_file_name

        # Load the json file
        with open(file_name, "r") as file:
            json_file = json.load(file)
            self.history = json_file
            return json_file

    def save_json(self, file_data: dict = None, file_name: str = None) -> None:
        # Import json for saving the json file
        import json

        # Set the file name if not chosen
        file_name = file_name or self.history_file_name

        # Set the file data if not chosen
        file_data = file_data or self.history

        # Save the json file
        with open(file_name, "w") as file:
            json.dump(file_data, file, indent=2)

    @staticmethod
    def generate_nums(question_type: str, nums_amount: int) -> list[int]:
        # Import randint for random integer generation
        from random import randint

        # Initialise numbers for storing
        nums = [0, 0]

        match question_type:
            case "addition":
                # Generate random numbers between 10 and 99
                nums = [randint(10, 99) for _ in range(nums_amount)]

            case "subtraction":
                # Generate random numbers between 10 and 99
                nums = [randint(10, 99) for _ in range(nums_amount)]

            case "multiplication":
                # Generate random numbers between 2 and 12
                nums = [randint(2, 12) for _ in range(nums_amount)]

            case "division":
                # Import reduce for calculating if the division is within 1 <= answer <= 12
                from functools import reduce

                # Only finish once the answer is an integer
                answer = 0.1
                while not answer.is_integer() or len(set(nums)) == 1:
                    # Generate random numbers between 2 and 12
                    nums = [randint(2, 24) for _ in range(nums_amount)]

                    # Work out the answer
                    answer = reduce((lambda x, y: x / y), nums)

        return nums

    @staticmethod
    def calc_answer(question_type: str, nums: list) -> int:
        match question_type:
            case "addition":
                return sum(nums)

            case "subtraction":
                from functools import reduce
                return reduce((lambda x, y: x - y), nums)

            case "multiplication":
                from functools import reduce
                return reduce((lambda x, y: x * y), nums)

            case "division":
                from functools import reduce
                return reduce((lambda x, y: x / y), nums)

    def store_incorrect(self, incorrect: list):
        # Load the history file
        history = self.load_json()

        for i, incorrect_question in enumerate(history["incorrect"]):
            if incorrect_question["question_type"] == incorrect[0] and \
                    incorrect_question["nums"] == incorrect[1] and \
                    incorrect_question["user_answer"] == incorrect[2] and \
                    incorrect_question["real_answer"] == incorrect[3]:

                # The question is already in the history, so we need to increment the amount of times it's been wrong
                history["incorrect"][i]["occurrences"] += 1

            else:
                # The question isn't in the history, so we need to add it
                history["incorrect"].append({
                    "question_type": incorrect[0],
                    "nums": incorrect[1],
                    "user_answer": incorrect[2],
                    "real_answer": incorrect[3],
                    "occurrences": 1
                })
                break

        # Store the history
        self.save_json(history)

    def check_answer(self, question_type: str, nums: list, user_answer: int,
                     add_to_history: bool = True) -> tuple[bool, int]:
        # Get the real answer for the question
        real_answer = self.calc_answer(question_type, nums)

        # Check against the user's answer
        if user_answer == real_answer:
            # User got it correct
            return True, real_answer

        else:
            # If add_to_history is true, we want to store the incorrect into history
            if add_to_history:
                self.store_incorrect([question_type, nums, user_answer, real_answer])

            # User didn't get it correct
            return False, real_answer

    def generate_test(self, question_type: str = None, nums_amount: int = None) -> list[int] | int:
        # Import randint for random integer generation
        from random import randint

        # Use default question type values if they haven't been specified
        question_type = question_type or self.question_type
        nums_amount = nums_amount or self.question_types[self.question_types[question_type]["min_nums"]]

        # Random question type if it hasn't been specified
        question_type = list(self.question_types)[randint(0, len(self.question_types) - 1)] \
            if question_type == "random" else question_type

        # Generate the numbers for the test
        nums = self.generate_nums(question_type, nums_amount)

        # Test has been generated, return nums
        return nums

    def get_min_nums(self, question_type: str) -> int:
        return self.question_types[question_type]["min_nums"]
