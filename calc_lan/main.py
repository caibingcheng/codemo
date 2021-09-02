# encode=utf-8

from operator import mul
from functools import reduce


class Exp():
    """
    表达式抽象， 操作符和操作数
    通过cal_apply调用， cal_apply(operator, operands)
    """

    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

    def __str__(self):
        operand_strs = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operand_strs)


def cal_apply(op, args):
    """
    正式计算, 但是没有递归， 所以需要有别的模块解决递归计算问题
    cal_apply(operator, operands)
    """
    if op in ("add", "+"):
        return sum(args)
    if op in ("sub", "-"):
        if len(args) == 0:
            raise TypeError("{} require 1 argument at least".format(op))
        elif len(args) == 1:
            return -args[0]
        else:
            return sum(args[:1] + [-arg for arg in args[1:]])
    if op in ("mul", "*"):
        return reduce(mul, args, 1)
    if op in ("div", "/"):
        if len(args) != 2:
            raise TypeError("{} require 2 argument".format(op))
        else:
            return args[0] / args[1]


def calc_parse(line):
    """
    解析表达式， 返回值是Exp
    先将表达式的各个元素拆开， 再组合为Exp格式
    """
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree


def tokenize(line):
    """
    拆分表示各个元素
    """
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.split()


known_operators = ['add', 'sub', 'mul', 'div', '+', '-', '*', '/']


def analyze(tokens):
    """
    表达式元素组合，形成操作树
    """
    assert_non_empty(tokens)
    # 数字或者操作符
    token = analyze_token(tokens.pop(0))
    # 如果是数字，直接放回就好了，继续求下一个，因为数字是自求解的，本身就是解
    if type(token) in (int, float):
        return token
    # 如果是操作符，则需要组合为Exp表达式
    if token in known_operators:
        # 当前是操作符， 则需要检查后面有没有操作数
        # 计算器的操作符后面是有操作数的
        # 操作数递归组合即可
        if len(tokens) == 0 or tokens.pop(0) != '(':
            raise SyntaxError('expected ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)


def analyze_operands(tokens):
    """
    生成操作数
    """
    assert_non_empty(tokens)
    operands = []
    # 直到闭括号
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_empty(tokens)
    tokens.pop(0)  # 移除闭括号‘）’
    return operands


def assert_non_empty(tokens):
    """Raise an exception if tokens is empty."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected end of line')


def analyze_token(token):
    """Return the value of token if it can be analyzed as a number, or token."""
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            # 如果不是数字， 则可能是表达式， 先直接返回
            return token


def calc_eval(expression):
    """
    表达式递归求解， 从里到外依次求解
    """
    expression.operands = [calc_eval(operand) if type(operand) == type(
        expression) else operand for operand in expression.operands]
    cal_apply_result = cal_apply(expression.operator, expression.operands)
    return cal_apply_result


def read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):
            print('Calculation completed.')
            return


if __name__ == '__main__':
    read_eval_print_loop()
