from pyreindexer.query import CondType
from tests.helpers.query_helper import call
from tests.test_data.constants import JOIN_METHOD


def apply_op(q, op):
    op = op.upper()
    if op == "AND":
        return call(q, "op_and") if hasattr(q, "op_and") else q
    if op == "OR":
        return call(q, "op_or")
    if op == "NOT":
        return call(q, "op_not")
    raise ValueError(op)


def add_nested(q, join_type, op, subq, right_field):
    op = op.upper()

    if op == "NOT":
        q = call(call(q, "op_not"), "open_bracket")
        getattr(q, JOIN_METHOD[join_type])(subq, "joined").on("location_id", CondType.CondEq, right_field)
        return call(q, "close_bracket")

    q = apply_op(q, op)
    getattr(q, JOIN_METHOD[join_type])(subq, "joined").on("location_id", CondType.CondEq, right_field)
    return q
