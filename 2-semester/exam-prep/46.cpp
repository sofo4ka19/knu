//
// Created by User on 09.06.2024.
//
#include <iostream>
#include <stack>

namespace var_46{
    //2----------------------------------------------------------------------------------------------------------
    int poliz(char* exp, int size){
        std::stack<int> stack;
        for (int i = 0; i<size; i++) {

            if (exp[i] != ' ') {
                if (exp[i]>='0' and exp[i]<='9') {
                    int num = 0;
                    while (exp[i]>='0' and exp[i]<='9') {
                        num = num*10+exp[i] - '0';
                        i++;
                    }


                    stack.push(num);
                }
                else {
                    int result;
                    if (exp[i] == '+'){

                        result = stack.top();
                        stack.pop();
                        result += stack.top();
                        stack.pop();

                        stack.push(result);
                    }else if (exp[i] == '*'){
                        result = stack.top();
                        stack.pop();
                        result *= stack.top();
                        stack.pop();

                        stack.push(result);
                    }


                }
            }
        }
        return stack.top();
    }
    int main(){
        return 0;
    }
}