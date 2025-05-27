import re
import regex

def _fix_fracs(string):
    substrs = string.split("\\frac")
    new_str = substrs[0]
    if len(substrs) > 1:
        substrs = substrs[1:]
        for substr in substrs:
            new_str += "\\frac"
            if len(substr) > 0 and substr[0] == "{":
                new_str += substr
            else:
                try:
                    assert len(substr) >= 2
                except:
                    return string
                a = substr[0]
                b = substr[1]
                if b != "{":
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}{" + b + "}" + post_substr
                    else:
                        new_str += "{" + a + "}{" + b + "}"
                else:
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}" + b + post_substr
                    else:
                        new_str += "{" + a + "}" + b
    string = new_str
    return string


def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        if "sqrt" not in a:
            a = int(a)
        if "sqrt" not in b:
            b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string


def _fix_sqrt(string):
    _string = re.sub(r"\\sqrt(-?[0-9.a-zA-Z]+)", r"\\sqrt{\1}", string)
    _string = re.sub(r"\\sqrt\s+(\w+)$", r"\\sqrt{\1}", _string)
    return _string


def _fix_tan(string):
    _string = re.sub(r"\\tan(-?[0-9.a-zA-Z]+)", r"\\tan{\1}", string)
    _string = re.sub(r"\\tan\s+(\w+)$", r"\\tan{\1}", _string)
    return _string

def _fix_unicode(string):
    # for debugging.
    before = string

    # square root 
    pattern = re.compile(r'√(\([^()]*\)|[A-Za-z0-9]+)')
    string = pattern.sub(lambda m: r'\sqrt{' + m.group(1) + '}', string)

    # cube root
    pattern = re.compile(r'∛(\([^()]*\)|[A-Za-z0-9]+)')
    string = pattern.sub(lambda m: r'\sqrt[3]{' + m.group(1) + '}', string)

    # other fonts of digits
    math_sans_bold_digits = {
        '𝟬': '0', '𝟭': '1', '𝟮': '2', '𝟯': '3', '𝟰': '4',
        '𝟱': '5', '𝟲': '6', '𝟳': '7', '𝟴': '8', '𝟵': '9',

        '𝟢': '0', '𝟣': '1', '𝟤': '2', '𝟥': '3', '𝟦': '4',
        '𝟧': '5', '𝟨': '6', '𝟩': '7', '𝟪': '8', '𝟫': '9',
    }
    for unicode_digit, ascii_digit in math_sans_bold_digits.items():
        string = string.replace(unicode_digit, ascii_digit)

    subscript_map = {
        '₀': '0', '₁': '1', '₂': '2', '₃': '3',
        '₄': '4', '₅': '5', '₆': '6', '₇': '7',
        '₈': '8', '₉': '9', 'ₙ': 'n'
    }
    for subchar, digit in subscript_map.items():
        string = string.replace(subchar, f"_{{{digit}}}")

    # other replacements
    replacements = {
        '²': '^{2}',
        '³': '^{3}',
        'ⁿ': '^{n}',
        'π': '\\pi ',
        '∞': '\\infty ',
        '⎣': '\\lfloor ',
        '⎦': '\\rfloor ',
        '–': '-', ## (en dash) U+2013 to (hyphen) U+002D
        '−': '-', ## (minus) U+2212 to (hyphen) U+002D
        '∪': '\\cup ',
        '∩': '\\cap ',
        '·': '\\cdot ',
        '×': '\\times ',
        ' ': ' ',
        '⁄': '/',
        '\xa0': ' ',
        '½': '\\frac{1}{2}',
        '∏': '\\prod ',
        '∑': '\\sum ',
    }
    
    for unicode_char, latex_equiv in replacements.items():
        string = string.replace(unicode_char, latex_equiv)

    if before != string:
        print(f"DEBUG: Unicode conversion: {before} -> {string}", flush=True)
    return string


def strip_string(string):
    string = str(string).strip()
    # linebreaks
    string = string.replace("\n", "")

    # right "."
    string = string.rstrip(".")

    # remove inverse spaces
    string = string.replace("\\!", "")
    string = re.sub(r'(?<!\\)\\ ', '', string) # remove "\\ " but not "\\\\ ".
    string = string.replace("\\,", "")
    string = string.replace("\\:", "")
    string = string.replace("\\;", "")
    string = string.replace("\\quad", "")

    # replace \\ with \
    # string = string.replace("\\\\", "\\")
    # string = string.replace("\\\\", "\\")

    if string.startswith("\\text{") and string.endswith("}"):
        string = string.split("{", 1)[1][:-1]

    # replace tfrac and dfrac with frac
    string = string.replace("tfrac", "frac")
    string = string.replace("dfrac", "frac")
    string = string.replace("cfrac", "frac")

    # remove \left and \right
    string = string.replace("\\left", "")
    string = string.replace("\\right", "")

    # Remove unit: miles, dollars if after is not none
    _string = re.sub(r"\\text{.*?}$", "", string).strip()
    if _string != "" and _string != string:
        # print("Warning: unit not removed: '{}' -> '{}'".format(string, _string))
        string = _string

    # Remove circ (degrees)
    string = string.replace("^{\\circ}", "").strip()
    string = string.replace("^\\circ", "").strip()

    string = regex.sub(r"\{(c|m)?m\}(\^(2|3))?", "", string).strip()
    string = regex.sub(r"p\.m\.$", "", string).strip()
    string = regex.sub(r"(\d)\s*t$", r"\1", string).strip()

    ## fix for o1 and o3-mini: these models may use unicode characters for some operators.
    string = _fix_unicode(string)


    # remove dollar signs
    string = string.replace("\\$", "")
    string = string.replace("$", "")

    # string = string.replace("\\text", "")
    string = string.replace("x\\in", "")

    # remove percentage
    string = string.replace("\\%", "%")
    string = string.replace("\%", "%")
    # string = string.replace("%", "")

    # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively, add "0" if "." is the start of the string
    string = string.replace(" .", " 0.")
    string = string.replace("{.", "{0.")

    # cdot
    # string = string.replace("\\cdot", "")

    # inf
    string = string.replace("infinity", "\\infty")
    if "\\infty" not in string:
        string = string.replace("inf", "\\infty")
    string = string.replace("+\\inity", "\\infty")

    # and 
    # string = string.replace("and", "")
    string = string.replace("\\mathbf", "")
    string = string.replace("\\mathrm", "")

    # use regex to remove \mbox{...}
    string = re.sub(r"\\mbox{.*?}", "", string)

    # quote
    string.replace("'", "")
    string.replace("\"", "")
    
    # i, j
    if "j" in string and "i" not in string:
        string = string.replace("j", "i")

    # replace a.000b where b is not number or b is end, with ab, use regex
    string = re.sub(r"(\d+)\.0+([^\d])", r"\1\2", string)
    string = re.sub(r"(\d+)\.0+$", r"\1", string)

    # if empty, return empty string
    if len(string) == 0:
        return string
    if string[0] == ".":
        string = "0" + string

    # to consider: get rid of e.g. "k = " or "q = " at beginning
    # if len(string.split("=")) == 2:
    #     if len(string.split("=")[0]) <= 2:
    #         string = string.split("=")[1]

    string = _fix_sqrt(string)
    string = _fix_tan(string)
    #string = string.replace(" ", "")

    # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
    string = _fix_fracs(string)

    # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix in case the model output is X/Y
    string = _fix_a_slash_b(string)

    string = regex.sub(r"(\\|,|\.)+$", "", string)

    return string

def extract_boxed_answers(text):

    ### sometimes extra spaces are added between `boxed`` and the brackets `{}`.
    text = re.sub(r"boxed\s+\{", "boxed{", text)
    text = re.sub(r"boxed\s+\[", "boxed[", text)
    text = re.sub(r"boxed\s+\(", "boxed(", text)

    answers = []
    for piece in text.split('boxed{')[1:]:
        n = 0
        for i in range(len(piece)):
            if piece[i] == '{':
                n += 1
            elif piece[i] == '}':
                n -= 1
                if n < 0:
                    if i + 1 < len(piece) and piece[i + 1] == '%':
                        answers.append(piece[: i + 1])
                    else:
                        answers.append(piece[:i])
                    break

    ### o3-mini may output boxed(), boxed[] instead of boxed{}. This is a hack to fix it.
    left_brackets = ['(', '[', '{']
    right_brackets = [')', ']', '}']
    if len(answers) == 0:
        for piece in text.split('boxed(')[1:]:
            n = 0
            for i in range(len(piece)):
                if piece[i] in left_brackets:
                    n += 1
                elif piece[i] in right_brackets:
                    n -= 1
                    if n < 0:
                        if i + 1 < len(piece) and piece[i + 1] == '%':
                            answers.append(piece[: i + 1])
                        else:
                            answers.append(piece[:i])
                        break
        for piece in text.split('boxed[')[1:]:
            n = 0
            for i in range(len(piece)):
                if piece[i] in left_brackets:
                    n += 1
                elif piece[i] in right_brackets:
                    n -= 1
                    if n < 0:
                        if i + 1 < len(piece) and piece[i + 1] == '%':
                            answers.append(piece[: i + 1])
                        else:
                            answers.append(piece[:i])
                        break
    return answers

def extract_program_output(pred_str):
    """
    extract output between the last ```output\n...\n```
    """
    if "```output" not in pred_str:
        return ""
    if '```output' in pred_str:
        pred_str = pred_str.split('```output')[-1]
    if '```' in pred_str:
        pred_str = pred_str.split('```')[0]
    output = pred_str.strip()
    return output

def extract_answer(pred_str, exhaust=False):
    pred = []
    if 'final answer is $' in pred_str and '$. I hope' in pred_str:
        tmp = pred_str.split('final answer is $', 1)[1]
        pred = [tmp.split('$. I hope', 1)[0].strip()]
    elif 'boxed' in pred_str:
        pred = extract_boxed_answers(pred_str)
    elif ('he answer is' in pred_str):
        pred = [pred_str.split('he answer is')[-1].strip()]
    else:
        program_output = extract_program_output(pred_str)
        if program_output != "":
            # fall back to program
            pred.append(program_output)
        else: # use the last number
            #print("warning: fall back to the last number", flush=True)
            #print([pred_str], flush=True)
            pattern = '-?\d*\.?\d+'
            ans = re.findall(pattern, pred_str.replace(",", ""))
            if(len(ans) >= 1):
                ans = ans[-1]
            else:
                ans = ''
            if ans:
                pred.append(ans)
                #print(ans, flush=True)

    # multiple line
    _pred = []
    for ans in pred:
        ans = ans.strip().split("\n")[0]
        ans = ans.lstrip(":")
        ans = ans.rstrip(".")
        ans = ans.rstrip("/")
        ans = strip_string(ans)
        _pred.append(ans)
    if exhaust:
        return _pred
    else:
        return _pred[-1] if _pred else ""

def extract_math_answer(question, reasoning, task):
    answer = []
    for ans in extract_answer(reasoning, exhaust=True):
        if 'separated by commas' in question and all(ch not in ans for ch in '()[]'):
            answer.extend([a.strip() for a in ans.split(",")])
        elif regex.search(r"\\text\{\s*and\s*\}", ans):
            answer.extend([a.strip() for a in regex.sub(r"\\text\{\s*and\s*\}", "[SEP]", ans).split("[SEP]")])
        elif regex.search(r"\\text\{\s*or\s*\}", ans):
            answer.extend([a.strip() for a in regex.sub(r"\\text\{\s*or\s*\}", "[SEP]", ans).split("[SEP]")])
        elif regex.search(r"\s+and\s+", ans):
            answer.extend([a.strip() for a in regex.sub(r"\s+and\s+", "[SEP]", ans).split("[SEP]")])
        elif regex.search(r"\s+or\s+", ans):
            answer.extend([a.strip() for a in regex.sub(r"\s+or\s+", "[SEP]", ans).split("[SEP]")])
        else:
            answer.append(ans.strip())
    return answer

def extract_math_perturb_ground_truth_answer(question, reasoning, task):
    """ 
        Hack for the labels with multiple answers separated by ' or '
    """
    answer = []
    for ans in extract_answer(reasoning, exhaust=True):
        if 'separated by commas' in question and all(ch not in ans for ch in '()[]'):
            answer.extend([a.strip() for a in ans.split(",")])
        elif regex.search(r"\\text\{\s*and\s*\}", ans):
            answer.extend([a.strip() for a in regex.sub(r"\\text\{\s*and\s*\}", "[SEP]", ans).split("[SEP]")])
        elif regex.search(r" or ", ans):
            answer.extend([a.strip() for a in regex.sub(r" or ", "[SEP]", ans).split("[SEP]")])
        else:
            answer.append(ans.strip())
    return answer

def extract_math_few_shot_cot_answer(question, reasoning, task):
    if 'Problem:' in reasoning:
        reasoning = reasoning.split("Problem:", 1)[0]
    return extract_math_answer(question, reasoning, task)

def extract_last_single_answer(question, reasoning, task):
    return extract_answer(reasoning, exhaust=False)

def extract_gsm_few_shot_cot_answer(question, reasoning, task):
    if 'Q: ' in reasoning:
        reasoning = reasoning.split("Q: ", 1)[0]
    pred = [s for s in regex.findall(r'-?\d+\.?\d*', reasoning)]
    if pred:
        return pred[-1]
    else:
        return "[invalid]"

def extract_agieval_gaokao_mathcloze_few_shot_cot_test(question, reasoning, task):
    if '问题 ' in reasoning:
        reasoning = reasoning.split("问题 ", 1)[0]
    if '答案是' in reasoning:
        ans = reasoning.split('答案是', 1)[1].strip()
        ans = ans.split("\n")[0].strip()
        ans = [ans.strip("$")]
    else:
        ans = ['placeholder']
    return ans

def extract_agieval_gaokao_mathqa_few_shot_cot_test(question, reasoning, task):
    if '问题 ' in reasoning:
        reasoning = reasoning.split("问题 ", 1)[0]
    if '答案是' in reasoning:
        ans = reasoning.split('答案是', 1)[1].strip()
        ans = ans.split("\n")[0].strip()
    else:
        ans = 'placeholder'
    return ans

def extract_sat_few_shot_answer(question, reasoning, task):
    if 'Problem:' in reasoning:
        reasoning = reasoning.split("Problem:", 1)[0]
    patt = regex.search(r"the final answer is \(?(?P<ans>[abcd])\)?", reasoning.lower())
    if patt is not None:
        return patt.group('ans').upper()
    return 'placeholder'

def extract_ocwcourses_few_shot_answer(question, reasoning, task):
    if 'Problem:' in reasoning:
        reasoning = reasoning.split("Problem:", 1)[0]
    patt = regex.search(r"final answer is (?P<ans>.*)\. I hope it is correct.", reasoning)
    if patt is None:
        pred = "[invalid]"
        print(f"DEBUG >>>\n{reasoning}", flush=True)
    else:
        pred = patt.group('ans')
    return pred

def extract_mmlu_stem(question, reasoning, task):
    if 'Problem:' in reasoning:
        reasoning = reasoning.split("Problem:", 1)[0]
    return extract_sat_few_shot_answer(question, reasoning, task)

def extract_minif2f_isabelle(question, reasoning, task):
    if 'Informal:' in reasoning:
        reasoning = reasoning.split("Informal:", 1)[0]
    return reasoning.strip()

def extract_cmath_few_shot_test(question, reasoning, task):
    if '问题：' in reasoning:
        reasoning = reasoning.split("问题：", 1)[0]
    if '答案是' in reasoning:
        ans = reasoning.split('答案是', 1)[1].strip()
        ans = ans.split("\n")[0]
        ans = ans.strip("：")
        ans = ans.strip("。")
        try:
            ans = [s for s in regex.findall(r'-?\d+\.?\d*', ans)][-1]
        except:
            print(f"DEBUG CMATH: {reasoning}", flush=True)
            ans = "[invalid]"
    else:
        ans = extract_last_single_answer(question, reasoning, task)
    return ans
