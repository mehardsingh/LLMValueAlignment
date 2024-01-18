def create_question(question_template, lower, question_info):
    question_insertion = question_info["QuestionInsertion"]
    left = question_info["Left"]
    right = question_info["Right"]

    if type(question_insertion) == str:
        if lower:
            question_insertion = question_insertion.lower()
        question = question_template.replace("{QUESTION}", question_insertion)  

    else:
        question = question_template   
    
    if type(left) == str:
        question = question.replace("{LEFT}", left)

    if type(right) == str:
        question = question.replace("{RIGHT}", right)

    return question.strip()

def split_string_by_commas(s):
    result = []
    current = ""
    depth = 0

    for char in s:
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1

        if char == ',' and depth == 0:
            result.append(current.strip())
            current = ""
        else:
            current += char

    # Add the remaining part if any
    if current:
        result.append(current.strip())

    return result

def create_answer_choice(question_info):
    answer_choice = question_info["AnswerChoices"]
    left = question_info["Left"]
    right = question_info["Right"]

    if type(left) == str:
        answer_choice = answer_choice.replace("{LEFT}", left)

    if type(right) == str:
        answer_choice = answer_choice.replace("{RIGHT}", right)

    answer_choice = split_string_by_commas(answer_choice)
    answer_choice = [c for c in answer_choice if not c == ""]
    answer_choice = [c.split(":")[1].strip() for c in answer_choice]

    return answer_choice
