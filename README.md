# MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations

Evaluation code and dataset for the ICML 2025 paper [MATH-Perturb: Benchmarking LLMs' Math Reasoning Abilities against Hard Perturbations](https://arxiv.org/abs/2502.06453).

For more details and the leaderboard, please refer to the project page [here](https://math-perturb.github.io/).

## Dataset Usage

The MATH-P-Simple and MATH-P-Hard datasets are located in `math_perturb/`. Each testset is a `jsonl` file, where each line represents a test datapoint in `json` format. You can load the dataset with the following Python code:

```python
dataset = [json.loads(line) for line in open(filepath)]
``` 

### Keys:

- `problem_id`: A unique random problem id assigned to each of the *original* problem. The modified problems sharing the same `problem_id` are perturbed from the same original problem.
- `problem`: Problem statement.
- `answer`: Ground-truth answer to the problem.
- `level`: The difficulty level that originates from MATH dataset. The field will be `"Level 5"` for all the entries.
- `type`: Category of the math problem, e.g., Algebra, Calculus, etc. 
- `original_split`: The split (`train` v.s. `test`) where the original problem belongs.


**Note: Please do not use MATH-P-Simple or MATH-P-Hard as training data.**



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

## Legal Compliance


Intended Usage:

- The dataset is only for **academic research purposes**, and we do not seek to monetize or commercialize the problems & answers.
- The MATH-Perturb datasets (both MATH-P-Simple and MATH-P-Hard) are intended to be used as **test datasets** (benchmarks) to **evaluate** large language models. 
- The datasets should **not** be used for training the models under any circumstance.

Transformative differences from MATH dataset (Hendrycks et al., 2021):

- We have transformed the problems from the original MATH dataset by making edits directly to the problem statements. 
- For our two variants MATH-P-Simple and MATH-P-Hard, we have worked on the modified problems ourselves to get the correct answers. We only released the final answers without the intermediate steps.
- We have ensured that the answers to our perturbed problems are different from the answers to the corresponding original problems.  



## Citation

Please consider citing our paper if you find it useful.

```bibtex
@article{huang2025math,
        title={{MATH-Perturb}: Benchmarking {LLMs}' Math Reasoning Abilities against Hard Perturbations},
        author={Kaixuan Huang and Jiacheng Guo and Zihao Li and Xiang Ji and Jiawei Ge and Wenzhe Li and Yingqing Guo and Tianle Cai and Hui Yuan and Runzhe Wang and Yue Wu and Ming Yin and Shange Tang and Yangsibo Huang and Chi Jin and Xinyun Chen and Chiyuan Zhang and Mengdi Wang},
        journal={arXiv preprint arXiv:2502.06453},
        year={2025}
      }
```