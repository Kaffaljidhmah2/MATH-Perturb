from evaluation.answer_extraction import extract_math_answer, extract_math_perturb_ground_truth_answer,  strip_string
from evaluation.eval_script import eval_math
from evaluation.eval_utils import MAX_ABS_TOL

def extract_ground_truth_answer(problem, ground_truth, dataset_type):
    """
        Extracts the ground truth answer from the problem statement and ground_truth string.
        Args:
            problem (str): The problem statement.
            ground_truth (str): The ground truth answer string.
            dataset_type (str): The type of dataset, either 'perturb' or 'original'.
        Returns:
            ground_truth_answer_extracted (list): The extracted ground truth answer.
    """
    assert dataset_type in ['perturb', 'original'], "dataset_type must be either 'perturb' or 'original'"
    if dataset_type == 'perturb':
        ground_truth_answer = ground_truth
        if isinstance(ground_truth_answer, int) or isinstance(ground_truth_answer, float):
            ground_truth_answer = str(ground_truth_answer)

        ground_truth_answer_stripped = strip_string(ground_truth_answer)
        ground_truth_wrapped = "\\boxed{" + ground_truth_answer + "}"
        ground_truth_answer_extracted = extract_math_perturb_ground_truth_answer(problem, ground_truth_wrapped, task='')


        if ground_truth_answer_stripped != str(ground_truth_answer_extracted[0]):
            print("Multi-valued ground truth:" , ground_truth_answer_stripped, ground_truth_answer_extracted)
    elif dataset_type == 'original':
        ground_truth_answer_extracted = extract_math_answer(problem, ground_truth, task='')

    return ground_truth_answer_extracted

def extract_predicted_answer(problem, solution_str):
    """
        Extracts the predicted answer from the solution string.
        Args:
            problem (str): The problem statement.
            solution_str (str): The solution string containing the predicted answer.
        Returns:
            unique_prediction (list): The extracted predicted answer, with duplicates removed.
    """
    prediction = extract_math_answer(problem, solution_str, task='')

    unique_prediction = list(dict.fromkeys(prediction)) # remove duplicates but preserve order
    if len(unique_prediction) > 1:
        print("multi-valued prediction:", unique_prediction)

    return unique_prediction


def answer_check(problem, solution_str, ground_truth, dataset_type):
    """
        Checks if the predicted answer matches the ground truth answer.
        Args:
            problem (str): The problem statement.
            solution_str (str): The solution string containing the predicted answer.
            ground_truth (str): The ground truth answer string.
            dataset_type (str): The type of dataset, either 'perturb' or 'original'.
        Returns:
            is_correct (bool): True if the predicted answer matches the ground truth answer, False otherwise.
    """
    ground_truth_answer_extracted = extract_ground_truth_answer(problem, ground_truth, dataset_type)
    prediction_extracted = extract_predicted_answer(problem, solution_str)

    #print("Ground truth:", ground_truth_answer_extracted)
    #print("Prediction:", prediction_extracted)

    inp = {
        'answer': ground_truth_answer_extracted,
        'prediction': prediction_extracted
    }

    is_correct = eval_math(inp, prec=MAX_ABS_TOL)
    return is_correct


def test_parse_latex():
    # test if parse_latex is working:
    dataset_type = 'perturb'
    problem = "A fake problem statement."
    ground_truth = '1 - (x + 1)^{\\frac14}'
    solution_str = r"""
The answer is 
\[ \boxed{1 - \sqrt[4]{x + 1}} \]
"""
    
    assert answer_check(problem, solution_str, ground_truth, dataset_type), 'there may be error in sympy package!'

if __name__ == "__main__":
    test_parse_latex()
    print("All tests passed!")