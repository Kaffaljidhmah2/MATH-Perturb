# MATH Evaluation Code


The code is modified from [DeepSeek-Math/evaluation](https://github.com/deepseek-ai/DeepSeek-Math/tree/main/evaluation), with the following key modifications:

1. Changed the absolute tolerance `abs_tol` from `1e-3` to `1e-7`. This reduces false positives, e.g., the original verifier may cliam 1/5120 to be the same as 1/28800. 

2. Added post-processing codes for handling unicodes. OpenAI o1 and o3-mini tend to output a lot of unicodes.

3. Used `lark` as SymPy latex backend.

4. Fixed other latex parsing bugs.