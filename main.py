import mmtrain
import colour as c
from random import randint
from os import system
from time import sleep, perf_counter


def print_error(message: str):
    print(f"{c.red}Error: {message}.{c.end}")


def ask_question_type(question_types: dict) -> str | None:
    while True:
        # Ask the user what question type they want
        inp_question_type = input(f"{c.blue}Question type?{c.end} "
                                  f"{c.cyan}{list(question_types)}{c.end} "
                                  f"{c.blue}or{c.end} {c.cyan}random{c.end}{c.blue}:{c.end} ")

        for question_type in question_types:
            # Check for shorthand e.g. user typed in "s" for "subtraction"
            if inp_question_type == question_types[question_type]["shorthand"]:
                inp_question_type = question_type

        # If no question type or random has been chosen
        if inp_question_type in ("random", "r") or not inp_question_type:
            # Randomly generate the question_type
            rnd_question_type = list(question_types)[randint(0, len(question_types) - 1)]
            print(f"{c.green}Randomly selected '{rnd_question_type}.'{c.end}")

            # Return the randomly selected question type
            return rnd_question_type

        # If the question type is valid
        elif inp_question_type in question_types:
            # Return the inputted question type
            return inp_question_type


def generate_question_text(question_types: dict, question_type: str, nums: list[int] | int) -> str:
    # Get the symbol from the dictionary
    symbol = question_types[question_type]["symbol"]

    # Put the question text together from the list of nums and symbol
    ask_question = f"{c.cyan}{nums[0]}{c.end}"
    for num in nums[1:]:
        ask_question += f" {c.blue}{symbol}{c.end} {c.cyan}{num}{c.end}"

    return ask_question


def get_timed_answer(question_types: dict, question_type: str, nums: list[int] | int) -> tuple[int, float]:
    # Get the current time
    start_time = perf_counter()

    while True:
        try:
            answer = int(input(f"{generate_question_text(question_types, question_type, nums)}\n"  # Question
                               f"{c.magenta}=> {c.end}"))  # Prompt
            break

        except ValueError:
            print_error("Not an integer")

    # Get the time after the question has been answered
    end_time = perf_counter()

    # Calculate the time taken for the user to answer to 2 d.p.
    final_time = round(end_time - start_time, 2)

    return answer, final_time


def ask_amount(default_amount: int, thing: str) -> int:
    while True:
        # Ask for the amount of numbers
        amount = input(f"{c.blue}Amount of {thing}?{c.end} "
                       f"{c.cyan}(default: {default_amount}){c.end}{c.cyan}:{c.end} ")

        # Use default_amount if no answer is given
        if not amount:
            return default_amount

        # Has to be a positive integer
        elif not amount.isnumeric():
            print_error(f"Invalid number - must be an integer greater than {default_amount}")

        # Has to be greater than the minimum amount of numbers (which is also the default)
        elif int(amount) < default_amount:
            print_error(f"Invalid number - integer must be greater than {default_amount}")

        # Must be a correct
        else:
            return int(amount)


def train(trainer: mmtrain.MentalMathsTrainer, question_types: dict, question_type: str, question_amount: int,
          question_num: int, nums_amount: int, game_stats: dict):
    # Print question title
    print(f"{c.magenta}Question {question_num + 1} / {question_amount}")

    # Generate the test numbers
    nums = trainer.generate_test(question_type, nums_amount)

    # Check user answer
    user_answer, final_time = get_timed_answer(question_types, question_type, nums)
    correct, real_answer = trainer.check_answer(question_type, nums, user_answer)
    game_stats[final_time] = correct, nums, user_answer, real_answer

    # If the answer is correct, tell them
    if correct:
        print(f"{c.green}✔️  Correct!{c.end} {c.blue}(took {final_time}s){c.end}")

    # Otherwise it must be false
    else:
        print(f"{c.red}❌ Incorrect.{c.end} {c.blue}(took {final_time}s){c.end}")


def game(trainer: mmtrain.MentalMathsTrainer, question_type: str, question_amount: int, nums_amount: int):
    # Initialise game_stats
    game_stats = {}

    for question_num in range(question_amount):
        # Clear the screen
        system("clear")

        # Begin training
        train(trainer, trainer.question_types, question_type, question_amount, question_num, nums_amount, game_stats)

        # Wait half a second so user can see if they got the question right or not
        sleep(0.5)

    # Calculate the average time and round to 2d.p.
    average_time = round(sum(game_stats) / len(game_stats), 2)

    # Calculate percentage correct
    percent = round((sum(stat[0] for stat in list(game_stats.values())) / question_amount) * 100)

    # Show the user their stats
    print(f"\n{c.magenta}-- Stats --{c.end}\n"
          f"On average it took you {c.blue}{average_time}s{c.end} to answer\n"
          f"You got "
          f"{c.blue}{percent}%{c.end}"
          f" correct.")

    # Show the user what questions they got wrong and the correct answer
    if percent < 100:
        incorrect = [stat for stat in list(game_stats.values()) if not stat[0]]
        print(f"\n{c.red}-- Corrections --{c.end}")
        for list_num, question_data in enumerate(incorrect):
            question_asked = generate_question_text(trainer.question_types, question_type, question_data[1])

            print(f"{c.magenta}{list_num + 1}.{c.end} {c.blue}{question_asked}{c.end} = "
                  f"{c.green}{question_data[3]}{c.end} != {c.red}{question_data[2]}{c.end}")

    else:
        print(f"\n{c.green}Well done! You got everything correct.{c.end}")


def main():
    # Initialise the MentalMathsTrainer
    trainer = mmtrain.MentalMathsTrainer()

    # Print a title
    print(f"{c.magenta}-- Mental Maths Trainer --")

    # Ask for a question type
    question_type = ask_question_type(trainer.question_types)

    # Ask for the amount of questions
    question_amount = ask_amount(trainer.question_amount, "questions")

    # Ask for the amount of numbers
    nums_amount = ask_amount(trainer.get_min_nums(question_type), "numbers")

    # Confirm before beginning
    inp = input(f"{c.blue}Begin? {c.cyan}(Y/n):{c.end} ").upper()

    if inp == "N" or inp == "NO":
        # Quit the game if the user doesn't want to begin
        print(f"{c.blue}Goodbye!{c.end}")

    else:
        # Start the game
        game(trainer, question_type, question_amount, nums_amount)


if __name__ == "__main__":
    main()
