# MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations

Evaluation code and dataset for the ICML 2025 paper [MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations](https://arxiv.org/abs/2502.06453).

For more details and the leaderboard, please refer to the project page [here](https://math-perturb.github.io/).

## Dataset Usage


## Evaluation 

The evaluation script extracts the answers within `\boxed{}`, post-processes the potentially unformatted answer string, and then utlizes SymPy package to check the equivalence of two latex strings. Please read the [README](/evaluation/README.md) for details. The entry point is the `answer_check` method in `evaluate.py`. This can be adapted both in evaluation and in RL training.

``` python
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
```

## License


## Citation

