from typing import List

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
    grammar = load_grammar("grammars/basic_sents.fcfg")
    sentences = list(generate(grammar))
    expressions = semantic_parse(sentences, grammar)
    for expression in expressions:
        value = evaluate(expression, model_dict)
        print(str(expression), ":", value)

    complex_grammar = load_grammar("grammars/complex_sents.fcfg")
    for sentence in generate(complex_grammar):
        print(sentence)
        # This grammar has infinite capacity.
        break


if __name__ == "__main__":
    main()
