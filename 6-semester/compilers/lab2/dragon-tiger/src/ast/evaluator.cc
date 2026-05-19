#include "evaluator.hh"
#include "../utils/errors.hh"
#include <cstdint>

namespace ast {

int32_t ASTEvaluator::visit(const IntegerLiteral &literal) {
  return literal.value;
}

int32_t ASTEvaluator::visit(const StringLiteral &literal) {
  utils::error(literal.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const BinaryOperator &binop) {
  int32_t left = binop.get_left().accept(*this);
  int32_t right = binop.get_right().accept(*this);
  switch (binop.op) {
    case o_plus:
      return left + right; 
    case o_minus:
      return left - right; 
    case o_times:
      return left * right;
    case o_divide:
      if (right == 0)
        utils::error(binop.loc, "division by zero");  
      return left / right;
    case o_eq:
      return left == right;
    case o_neq:
      return left != right;
    case o_lt:
      return left < right;
    case o_le:
      return left <= right;
    case o_gt:
      return left > right;
    case o_ge:
      return left >= right;
    default:
      utils::error(binop.loc, "unknown binary operator");
  }
}

int32_t ASTEvaluator::visit(const Sequence &seqExpr) {
  if(seqExpr.get_exprs().empty())
    utils::error(seqExpr.loc, "empty sequence");
  int32_t result = 0;
  for (const auto &expr : seqExpr.get_exprs()) {
    result = expr->accept(*this);
  }
  return result;
}

int32_t ASTEvaluator::visit(const Let &let) {
  utils::error(let.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const Identifier &id) {
  utils::error(id.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const IfThenElse &ite) {
  if (ite.get_condition().accept(*this))
    return ite.get_then_part().accept(*this);
  else
    return ite.get_else_part().accept(*this);
}

int32_t ASTEvaluator::visit(const VarDecl &decl) {
  utils::error(decl.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const FunDecl &decl) {
  utils::error(decl.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const FunCall &call) {
  utils::error(call.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const WhileLoop &loop) {
  utils::error(loop.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const ForLoop &loop) {
  utils::error(loop.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const Break &breakStmt) {
  utils::error(breakStmt.loc, "cannot evaluate");
}

int32_t ASTEvaluator::visit(const Assign &assign) {
  utils::error(assign.loc, "cannot evaluate");
}
}
  