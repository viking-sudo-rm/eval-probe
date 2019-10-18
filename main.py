from typing import List

import nltk
from nltk.grammar import FeatureGrammar
from nltk.sem import interpret_sents
from nltk.sem.logic import Expression
from nltk.sem.logic import ApplicationExpression, ConstantExpression
from nltk.parse.generate import generate

from eval_probe.model import model_dict


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
    grammar = nltk.data.load("grammars/basic_sents.fcfg", "fcfg")
    sentences = list(generate(grammar))
    expressions = semantic_parse(sentences, grammar)
    for expression in expressions:
        value = evaluate(expression, model_dict)
        print(str(expression), ":", value)


if __name__ == "__main__":
    main()
