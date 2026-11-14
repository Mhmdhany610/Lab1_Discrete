# =====================================================================
# Lab 1 - Part 1: Logical Expressions Solver (الكود كامل)
# =====================================================================
#
# ------------- قاموس المتغيرات (إيه كل اسم معناه) -------------------
# text        : النص نفسه، مثلاً "(P ^ Q) v ~R"
# tokens      : النص بعد ما اتقطّع لقائمة، مثلاً ['(', 'P', '^', 'Q', ')', 'EOF']
# pos         : "الصباع": رقم المكان اللي واقفين عليه في tokens
# values      : القاموس اللي فيه قيم المتغيرات، مثلاً {"P": True, "Q": False}
# left        : النتيجة اللي اتحسبت لحد دلوقتي (الحتة الشمال)
# right       : الحتة اللي بعد العملية (الحتة اليمين)
# op          : العملية الحالية (^ أو v)
# first_op    : أول عملية اتشافت في orand (عشان نكتشف خلط ^ و v)
# value       : القيمة اللي atom بترجّعها
# result      : النتيجة النهائية في evaluate_expression
#
# ------------- السلسلة (مين بينادي مين) ------------------------------
# evaluate_expression → expr (>) → orand (^ v) → unary (~) → atom (متغير أو قوس)
# =====================================================================


# ---------------------------------------------------------------------
# 1) tokenize_logic: يقطّع النص لقائمة (كل حرف token)
# ---------------------------------------------------------------------
def tokenize_logic(text):                          # بتاخد النص
    result = []                                    # القائمة النهائية (فاضية في الأول)
    for ch in text:                                # نمشي على النص حرف حرف
        if ch == " ":                              # لو مسافة
            continue                               # تجاهلها وروح للحرف اللي بعده
        if ch.isalpha():                           # لو حرف (متغير زي P أو عملية v)
            result.append(ch)                      # ضيفه
        elif ch in ["(", ")", "~", "^", ">"]:      # لو قوس أو عملية
            result.append(ch)                      # ضيفه
        else:                                      # أي حاجة تانية (زي @ أو 5)
            raise ValueError("Wrong expression")   # غلط
    return result                                  # رجّع القائمة


# ---------------------------------------------------------------------
# 2) Expression: علبة بتخزّن النص بس
# ---------------------------------------------------------------------
class Expression:
    def __init__(self, representation: str = ""):          # بيشتغل لما نعمل Expression("...")
        self.representation = representation               # خزّن النص جوه العلبة

    def get_representation(self) -> str:                   # افتح العلبة
        return self.representation                         # رجّع النص

    def set_representation(self, representation: str) -> None:   # غيّر النص
        self.representation = representation               # خزّن النص الجديد


# ---------------------------------------------------------------------
# 3) LogicalExpressionSolver: الـ parser جوه صندوق (كلاس)
# ---------------------------------------------------------------------
class LogicalExpressionSolver:

    def __init__(self):                    # بيشتغل مرة واحدة لما نعمل Solver()
        self.tokens = []                   # القائمة (فاضية دلوقتي)
        self.pos = 0                       # الصباع على أول مكان
        self.values = {}                   # قاموس القيم (فاضي دلوقتي)

    def peek(self):                        # بصّ على العنصر الحالي
        return self.tokens[self.pos]       # من غير ما تحرّك الصباع

    def advance(self):                     # حرّك الصباع خطوة لقدام
        self.pos = self.pos + 1            # زوّد pos بواحد

    # ----- atom: أقوى مستوى: متغير أو قوس -----
    def atom(self):
        if self.peek() == '(':                         # لو الحالي قوس فتح
            self.advance()                             # عدّي على '('
            value = self.expr()                        # احسب اللي جوه القوس من الأول (recursion)
            if self.peek() != ')':                     # لازم نلاقي ')' بعد اللي جوه القوس
                raise ValueError("Wrong expression")   # لو لأ: القوس ما اتقفلش
            self.advance()                             # عدّي على ')'
            return value                               # رجّع نتيجة اللي جوه القوس
        if self.peek() in self.values:                 # لو الحالي اسم متغير موجود في القاموس
            value = self.values[self.peek()]           # هات قيمته (True أو False)
            self.advance()                             # عدّي عليه
            return value                               # رجّع القيمة
        raise ValueError("Wrong expression")           # أي حاجة تانية في مكان متغير = غلط

    # ----- unary: الـ ~ -----
    def unary(self):
        if self.peek() == '~':                         # لو الحالي ~
            self.advance()                             # عدّي عليه
            return not self.unary()                    # نادي نفسها (عشان ~~P) واقلب النتيجة
        return self.atom()                             # لو مش ~ يبقى متغير أو قوس

    # ----- orand: ^ و v (نفس المستوى) -----
    def orand(self):
        left = self.unary()                            # خد أول حتة (متغير أو ~ أو قوس)
        first_op = None                                # لسه ما شفناش أي عملية
        while self.peek() == '^' or self.peek() == 'v':    # طول ما قدامي ^ أو v
            op = self.peek()                           # احفظ العملية
            if first_op is None:                       # لو دي أول عملية
                first_op = op                          # افتكرها
            elif first_op != op:                       # لو مختلفة عن أول واحدة (خلط ^ و v)
                raise ValueError("Wrong expression")   # غلط: لازم أقواس
            self.advance()                             # عدّي على العملية
            right = self.unary()                       # خد الحتة اللي بعدها
            if op == '^':                              # لو and
                left = left and right                  # احسبها
            else:                                      # غير كده يبقى or
                left = left or right                   # احسبها
        return left                                    # رجّع النتيجة

    # ----- expr: الـ > (أضعف مستوى) -----
    def expr(self):
        left = self.orand()                            # خد أول حتة جاهزة (^ و v اتحسبوا)
        while self.peek() == '>':                      # طول ما قدامي >
            self.advance()                             # عدّي عليها
            right = self.orand()                       # خد الحتة اللي بعدها جاهزة
            left = (not left) or right                 # P > Q  =  (not P) or Q
        return left                                    # رجّع النتيجة

    # ----- evaluate_expression: الباب الرئيسي اللي الـ tests بتنادي عليه -----
    def evaluate_expression(self, expression: Expression, values: dict) -> bool:
        text = expression.get_representation()         # افتح العلبة وهات النص
        self.tokens = tokenize_logic(text) + ['EOF']   # قطّعه وضيف علامة النهاية
        self.pos = 0                                   # صفّر الصباع (عشان نقدر نستخدم نفس الـ Solver تاني)
        self.values = values                           # خزّن القاموس عشان atom تشوفه
        result = self.expr()                           # ابدأ من أضعف مستوى
        if self.peek() != 'EOF':                       # لو فاضل كلام ما اتقراش (زي "P Q" أو "P )")
            raise ValueError("Wrong expression")       # غلط
        return result                                  # رجّع True أو False



# ======================================================================
# Part 2: Inference Engine
# ======================================================================
def split_expr(text):
    parts = text.split()
    if len(parts) == 1:
        return parts[0], None, None
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    raise ValueError("Wrong expression")


def negate(text):
    if text.startswith("~"):
        return text[1:]
    return "~" + text
class InferenceRule:
    name = ""
    def matches(self, exp1: Expression, exp2: Expression) -> bool:
        raise NotImplementedError
    
    def apply(self, exp1: Expression, exp2: Expression) -> Expression:
        raise NotImplementedError


class ModusPonens(InferenceRule):
    name = "Modus Ponens" 
    def matches(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        return op1 == ">" and left1 == exp2.get_representation()
    
    def apply(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        return Expression(right1)


class ModusTollens(InferenceRule):
    name = "Modus Tollens"
    def matches(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        return op1 == ">" and exp2.get_representation() == negate(right1)
    
    def apply(self, exp1, exp2):
            left1, op1, right1 = split_expr(exp1.get_representation())
            return Expression(negate(left1))
    
class HypotheticalSyllogism(InferenceRule):
    name = "Hypothetical Syllogism"
    def matches(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        left2, op2, right2 = split_expr(exp2.get_representation())
        return op1 == ">" and op2 == ">" and  left2 == right1
        
    def apply(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        left2, op2, right2 = split_expr(exp2.get_representation())
        return Expression(f"{left1} > {right2}")

class DisjunctiveSyllogism(InferenceRule):
    name = "Disjunctive Syllogism"
    def matches(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        return op1 == "v" and negate(exp2.get_representation()) == left1
                   
    def apply(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        return Expression(right1)

class Resolution(InferenceRule):
    name = "Resolution"
    def matches(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        left2, op2, right2 = split_expr(exp2.get_representation())
        return op1 == "v" and op2 == "v" and left1 == negate(left2)
            
    def apply(self, exp1, exp2):
        left1, op1, right1 = split_expr(exp1.get_representation())
        left2, op2, right2 = split_expr(exp2.get_representation())
        return Expression(f"{right1} v {right2}")
    
class InferenceEngine:
    def __init__(self):
        self.rules = []
        self.expressions = []
        self.last_rule = None

    def add_rule(self, rule: InferenceRule) -> None:
        self.rules.append(rule)

    def add_expression(self, exp: Expression) -> None:
        self.expressions.append(exp)
        

    def apply_rules(self) -> Expression:
        e1 = self.expressions[0]
        e2 = self.expressions[1]
        for rule in self.rules:
            for a,b in [(e1,e2), (e2,e1)]:
                if rule.matches( a , b ):
                    self.last_rule = rule
                    return rule.apply(a,b)
        return None
def infer(expr1: str, expr2: str) -> str:
    engine=InferenceEngine()
    engine.add_rule(ModusPonens())
    engine.add_rule(ModusTollens())
    engine.add_rule(HypotheticalSyllogism())
    engine.add_rule(DisjunctiveSyllogism())
    engine.add_rule(Resolution())
    engine.add_expression(Expression(expr1))
    engine.add_expression(Expression(expr2))
    result = engine.apply_rules()
    if result is None :
        return "The input expression can not be inferred"
    return f"{result.get_representation()} ({engine.last_rule.name}) "


# def main():
#     pass  # TODO: your program (input / output)


# if __name__ == "__main__":
#     main()


