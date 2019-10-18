from typing import List
from tqdm import tqdm

from nltk.grammar import FeatureGrammar
from nltk.sem import interpret_sents
from nltk.sem.logic import Expression
from nltk.sem.logic import ApplicationExpression, ConstantExpression
from nltk.parse.generate import generate

from eval_probe.model import model_dict


def load_grammar(grammar_file: str,
                 lexicon_file: str ="grammars/lexicon.fcfg") -> FeatureGrammar:
    with open(grammar_file) as g_file:
        grammar_text = g_file.read()
        grammar_text += "\n\n"
    with open(lexicon_file) as l_file:
        grammar_text += l_file.read()

    return FeatureGrammar.fromstring(grammar_text)


def semantic_parse(sentences: List[List[str]],
                   grammar: FeatureGrammar) -> List[Expression]:
    sentences = [" ".join(sent) for sent in sentences]
    results = interpret_sents(sentences, grammar)
    return [res[0][1] for res in results]


def evaluate(expression: Expression, model_dict):
    if isinstance(expression, ConstantExpression):
        return model_dict[str(expression)]
    if isinstance(expression, ApplicationExpression):
        pred = evaluate(expression.pred, model_dict)
        args = [evaluate(arg, model_dict) for arg in expression.args]
        return pred(*args)
    else:
        raise NotImplementedError("Trying to evaluate: %s." % expression)


def main():
    """Skeleton towards a data generation process.

    An actual data generation pipeline would:
      1. Generate all basic sentences and throw them in train.
      2. Generate all complex sentences, and divide between train/test.
    """

    print("Basic grammar...")
    basic_grammar = load_grammar("grammars/basic_sents.fcfg")
    sentences = tqdm(generate(basic_grammar))
    expressions = semantic_parse(sentences, basic_grammar)
    for expression in expressions:
        value = evaluate(expression, model_dict)
        print(str(expression), ":", value)

    print("Complex grammar...")
    complex_grammar = load_grammar("grammars/complex_sents.fcfg")
    sentences = tqdm(generate(complex_grammar, n=200, depth=5))
    expressions = semantic_parse(sentences, complex_grammar)
    for expression in expressions:
        value = evaluate(expression, model_dict)
        if value is not None:
            print(str(expression), ":", value)


if __name__ == "__main__":
    main()
