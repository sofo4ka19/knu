//
// Created by User on 09.06.2024.
//
#include <iostream>
#include <stack>
#include <cassert>

namespace var_48{
    //2------------------------------------------------------------------------------------------------------------
    bool is_digit(char current) {
        return current <= '9' && current >= '0';
    }

    bool is_operator(char current) {
        if (current == '-' || current == '/') { return true;}
        return false;
    }

    bool less_precedence(char operator1, char operator2) {
        if (operator1 == '-' && operator2 == '/') {return true;}
        return false;
    }

    void pop_stack_to_result(char from_stack, std::stack<char> &operator_stack,
                             std::string &result) {
        // greater precedence, or same precedence and left associative
        operator_stack.pop();
        result += from_stack;
        result += ' ';
    }

    std::string infix_to_postfix(std::string expression) {
        std::string result;
        std::stack<char> operator_stack;
        bool is_number = false;

        for (char current: expression) {
            if (is_digit(current)) {
                result += current;
                is_number = true;
            } else { // not digit
                if (is_number) {
                    result += ' ';
                    is_number = false;
                }
                if (is_operator(current)) {
                    while (!operator_stack.empty()) {
                        char from_stack = operator_stack.top();
                        if (is_operator(from_stack)) {
                            if (less_precedence(from_stack, current)) {
                                break; //less precedence
                            } else { // greater precedence, or same precedence and left associative
                                pop_stack_to_result(from_stack, operator_stack, result);
                            }
                        } else if (from_stack == '(') {
                            break; // no more operators for result
                        }
                    } // while there are suitable operators on stack
                    operator_stack.push(current);
                } else if (current == '(') {
                    operator_stack.push(current);
                } else if (current == ')') {
                    while (!operator_stack.empty()) {
                        char from_stack = operator_stack.top();
                        if (from_stack != '(') {
                            pop_stack_to_result(from_stack, operator_stack, result);
                        } else {
                            break;
                        }
                    } // while operator on stack is not (
                    if (operator_stack.empty()) {
                        return "error: ')' without '('";
                    }
                    assert(operator_stack.top() == '(');
                    operator_stack.pop(); // discard matching (
                } // if current
            } // if current is digit

        } // for current: input
        if (is_number) {
            result += ' ';
        }
        while(!operator_stack.empty()) {
            char from_stack = operator_stack.top();
            if (from_stack == '(') {
                return "error: '(' without ')'";
            }
            pop_stack_to_result(from_stack, operator_stack, result);
        }

        return result;
    }

    void check_expression(std::string expression) {
        std::cout<<expression<<" => "<< infix_to_postfix(expression)<<std::endl;
    }
    struct Node{
        int index;
        int value;
        Node* next;
    };
    struct RowNode{
        int index;
        Node* element;
        RowNode* next;
    };
    Node* row[4];
    int main(){
        return 0;
    }
}