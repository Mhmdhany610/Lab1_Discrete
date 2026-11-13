# ======================================================================
# Part 1: Logical Expressions Solver
# ======================================================================
class Expression:
    def __init__(self, representation: str = ""):
        pass  # TODO

    def get_representation(self) -> str:
        raise NotImplementedError  # TODO

    def set_representation(self, representation: str) -> None:
        raise NotImplementedError  # TODO


class LogicalExpressionSolver:
    # values: e.g. {"P": True, "Q": False, "R": True}
    # raises ValueError for a wrong expression
    def evaluate_expression(self, expression: Expression, values: dict) -> bool:
        raise NotImplementedError  # TODO


# ======================================================================
# Part 2: Inference Engine
# ======================================================================
class InferenceRule:
    def matches(self, exp1: Expression, exp2: Expression) -> bool:
        raise NotImplementedError

    def apply(self, exp1: Expression, exp2: Expression) -> Expression:
        raise NotImplementedError


class ModusPonens(InferenceRule):
    pass  # TODO


class ModusTollens(InferenceRule):
    pass  # TODO


class HypotheticalSyllogism(InferenceRule):
    pass  # TODO


class DisjunctiveSyllogism(InferenceRule):
    pass  # TODO


class Resolution(InferenceRule):
    pass  # TODO


class InferenceEngine:
    def __init__(self):
        pass  # TODO

    def add_rule(self, rule: InferenceRule) -> None:
        raise NotImplementedError  # TODO

    def add_expression(self, exp: Expression) -> None:
        raise NotImplementedError  # TODO

    def apply_rules(self) -> Expression:
        # None if it cannot be inferred
        raise NotImplementedError  # TODO


# returns the program output, e.g. "Y v Z (Resolution)"
def infer(expr1: str, expr2: str) -> str:
    raise NotImplementedError  # TODO


def main():
    pass  # TODO: your program (input / output)


if __name__ == "__main__":
    main()