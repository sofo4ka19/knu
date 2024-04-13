//Block 1: 2, 3
//Block 2: 7, 11
//Block 3: 13, 14, 15
//Block 4: 18
//Block 5: 21?
//Block 6: 22

#include <iostream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <map>
#include <cassert>

//Block 0
struct TreeNode{
    int value;
    std::vector<TreeNode*> children;

    TreeNode(int value): value{value}, children{} {}
};
//Block 1
std::vector<int> findTheWay(int element, TreeNode* root, std::vector<int> way = {}){
    if(element == root->value){
        return way;
    }
    for (int i = 0; i < root->children.size(); ++i) {
        if (i!=0) way.pop_back();
        way.push_back(i);
        if(!findTheWay(element, root->children[i], way).empty()) return findTheWay(element, root->children[i], way);
    }
    return {};
}
TreeNode* findTheElement(const std::vector<int>& way, TreeNode* root){
    for (int i = 0; i < way.size(); ++i) {
        if(root->children.size()<=way[i]){
            std::cout << "there is not such way in this tree" << std::endl;
            return nullptr;
        }
        root=root->children[way[i]];
    }
    return root;
}
void addTheElement(TreeNode* root, int value, const std::vector<int>& way){
    root = findTheElement(way, root);
    if(root == nullptr) return;
    root->children.push_back(new TreeNode(value));
    std::cout << "your element was added" << std::endl;
}
//Block 2
void print(TreeNode*& root){
    std::cout<<root->value;
    if (root->children.empty()) {return;}
    std::cout<<"(";
    for(int i=0; i<root->children.size(); i++) {
        print(root->children[i]);
        if(i!=root->children.size()-1)std::cout<<",";
    }
    std::cout<<")";
}

void printWay(std::vector<int> way){
    std::cout << "(";
    for (int i = 0; i < way.size(); ++i) {
        std::cout << std::setw(3) << way[i];
        if(i!=way.size()-1) std::cout<< ",";
    }
    std::cout << ") - ";
}
void printWithWay(TreeNode*& current, std::vector<int> way={}){
    printWay(way);
    std::cout << std::setw(3) << current->value << std::endl;
    if (current->children.empty()) {return;}
    for (int i = 0; i < current->children.size(); ++i) {
        if(i!=0) way.pop_back();
        way.push_back(i);
        printWithWay(current->children[i], way);
    }
}

//Block 3
TreeNode* deleteByWay(std::vector<int> way, TreeNode* root){
    int position = way[way.size()-1];
    way.pop_back();
    TreeNode* element = findTheElement(way, root);
    if (element == nullptr || root->children.size()<=position) return nullptr;
    TreeNode* parent = element->children[position];
    element->children.erase(element->children.begin()+position);
    return parent;
}
TreeNode* deleteAndPrintByElement(int value, TreeNode* root){
    if(root->value==value) return root;
    if(root->children.empty()) return nullptr;
    for (int i = 0; i < root->children.size(); ++i) {
        TreeNode* element = deleteAndPrintByElement(value, root->children[i]);
        if(element!= nullptr){
            root->children.erase(root->children.begin()+i);
            return element;
        }
    }
    return nullptr;
}
void deleteTree(TreeNode* root){
    for(TreeNode*& child: root->children) {
        deleteTree(child);
    }
    delete root;
}
void deleteByElement(int value, TreeNode* root){
    if (root->value == value) {
        deleteTree(root);
        std::cout << "subtree was deleted" << std::endl;
        return;
    }
    for (auto it = root->children.begin(); it != root->children.end();) {
        if ((*it)->value == value) {
            deleteTree(*it);
            it = root->children.erase(it);
        } else {
            deleteByElement(value, *it);
            ++it;
        }
    }
}
//Block 4
struct BinaryTree{
    int value;
    BinaryTree* left;
    BinaryTree* right;

    BinaryTree(int value): value{value}, left{nullptr}, right{nullptr} {}
};
void addToBinary(int value, BinaryTree* root = nullptr){
    assert(root!=nullptr);
    if(value < root->value){
        if (root->left == nullptr){
            root->left = new BinaryTree(value);
            return;
        }
        else{
            addToBinary(value, root->left);
        }
    }
    else{
        if(root->right== nullptr){
            root->right = new BinaryTree(value);
            return;
        }
        else{
            addToBinary(value, root->right);
        }
    }
}
void print(BinaryTree*& root){
    if(root== nullptr) return;
    std::cout<<root->value;
    if(root->left!= nullptr || root->right!= nullptr){
        std::cout<<"(";
        print(root->left);
        std::cout<<",";
        print(root->right);
        std::cout<<")";
    }

}
void printWithWay(BinaryTree*& current, std::vector<int> way={}){
    if(current== nullptr){
        std::cout << "there is no elements in your tree" << std::endl;
        return;
    }
    printWay(way);
    std::cout << std::setw(3) << current->value << std::endl;
    if(current->left!= nullptr) {
        std::vector<int> left = way;
        left.push_back(0);
        printWithWay(current->left, left);
    }
    if(current->right!= nullptr){
        std::vector<int> right = way;
        right.push_back(1);
        printWithWay(current->right, right);
    }
}
//Block 5 ?
void printStraightOrder(BinaryTree* root){
    if (root== nullptr) return;
    std::cout << root->value << " ";
    printStraightOrder(root->left);
    printStraightOrder(root->right);
}
//Block 6
enum NodeType {
    Constant,
    Variable,
    Operation
};

NodeType get_type_from_string(std::string value) {
    if(value[0]=='-' || (value[0]<='9' && value[0]>='0')){
        for(int i=1; i<value.size(); i++){
            assert((value[i]<='9' && value[i]>='0') || value[i]=='.');
        }
        return Constant;
    }
    if(value=="+" || value=="-" || value=="*" || value=="/" || value=="^") {
        return Operation;
    }
    if(isalpha(value[0])) return Variable;
    assert(false);
}

struct ExpressionTree {
    std::string value;
    NodeType type;
    ExpressionTree* left;
    ExpressionTree* right;

    ExpressionTree(std::string value):
            value{value}, type{get_type_from_string(value)}, left{nullptr}, right{nullptr} {}
};
double calculate(std::string operation, double num1, double num2){
    if (operation=="+") return (num1+num2);
    if (operation=="-") return (num1-num2);
    if (operation=="*") return (num1*num2);
    if (operation=="/") {
        assert(num2!=0);
        return (num1/num2);
    }
    if (operation=="^"){
        if(num2==0) return 1;
        //program can't calculate irrational
        assert(num2==round(num2));
        if (num1==0) {
            assert(num2>0);
            return 0;
        }
        double result=1;
        if (num2<0){
            for (int i = 0; i < num2; ++i) {
                result/=num1;
            }
            return (result);
        }
        if (num2>0){
            for (int i = 0; i < num2; ++i) {
                result*=num1;
            }
            return (result);
        }
    }
}
std::string createExpression(ExpressionTree* root){
    assert(root!= nullptr);
    if (root->type == Operation) {
        std::string left = createExpression(root->left);
        std::string right = createExpression(root->right);
        if(get_type_from_string(left)==Constant && get_type_from_string(right)==Constant){
            return std::to_string(calculate(root->value, std::stod(left), std::stod(right)));
        }
        std::string result = left + root->value + right ;
        if(root->value=="^") return "(" + result + ")";
        return result;
    }
    else {
        return root->value;
    }
}
double calculateValue(ExpressionTree* root, std::map<std::string, int> variable_values){
    assert(root!= nullptr);
    if (root->type == Operation) {
        double left_value = calculateValue(root->left, variable_values);
        double right_value = calculateValue(root->right, variable_values);
        calculate(root->value, left_value, right_value);
    }
    if (root->type == Constant) {
        return std::stod(root->value); // converts string to double
    }
    if (root->type == Variable) {
        return variable_values[root->value];
    }
}
void createExpressionTree(ExpressionTree* root){
    std::string value;
    if (root== nullptr) {
        std::cout << "Enter the operation for the root" << std::endl;
        std::cin >> value;
        assert(get_type_from_string(value) == Operation);
    }
    else{
        std::cout << "Enter the element for node" << std::endl;
        std::cin >> value;
    }
    root = new ExpressionTree(value);
    if(get_type_from_string(value) == Operation){
        createExpressionTree(root->left);
        createExpressionTree(root->right);
    }
}

void print(ExpressionTree*& root){
    if(root== nullptr) return;
    std::cout<<root->value;
    if(root->left!= nullptr || root->right!= nullptr){
        std::cout<<"(";
        print(root->left);
        std::cout<<",";
        print(root->right);
        std::cout<<")";
    }

}

void interactive(){
    int value, choose;
    std::cout << "choose with which tree you want to work: 1 - n-ary, 2 - binary, 3 - expression" << std::endl;
    std::cin >> choose;
    if(std::cin.fail()) return;
    if (choose==1) {
        std::cout << "enter the value for the root" << std::endl;
        std::cin >> value;
        if (std::cin.fail()) return;
        TreeNode *root = new TreeNode(value);
        while (true) {
            std::cout << "choose what to do:\n"
                         "1. Find the way of the element\n"
                         "2. Find the element by the way\n"
                         "3. Add an element\n"
                         "4. Print the tree with ()\n"
                         "5. Print tree with way for each element\n"
                         "6. Delete an element and return subtree\n"
                         "7. Delete an element and free memory\n"
                         "8. Delete by the way"
                      << std::endl;
            std::cin >> choose;
            if (std::cin.fail()) return;
            std::vector<int> way = {};
            TreeNode *deleted;
            switch (choose) {
                case 1:
                    std::cout << "enter value of the element" << std::endl;
                    std::cin >> value;
                    if (std::cin.fail()) return;
                    way = findTheWay(value, root);
                    if (way.empty() && value != root->value) {
                        std::cout << "there is no such element" << std::endl;
                    } else {
                        printWay(way);
                    }

                    break;
                case 2:
                    int size;
                    std::cout << "how long is your way?" << std::endl;
                    std::cin >> size;
                    if (std::cin.fail() || size < 0) return;
                    for (int i = 0; i < size; ++i) {
                        std::cout << "enter value for the way" << std::endl;
                        std::cin >> value;
                        if (std::cin.fail()) return;
                        way.push_back(value);
                    }
                    if (findTheElement(way, root) != nullptr)
                        std::cout << findTheElement(way, root)->value << std::endl;
                    break;
                case 3:
                    std::cout << "how long is your way to the parent of the element" << std::endl;
                    std::cin >> size;
                    if (std::cin.fail() || size < 0) return;
                    for (int i = 0; i < size; i++) {
                        std::cout << "enter value for the way" << std::endl;
                        std::cin >> value;
                        if (std::cin.fail()) return;
                        way.push_back(value);
                    }
                    std::cout << "enter value for the element" << std::endl;
                    std::cin >> value;
                    if (std::cin.fail()) return;
                    addTheElement(root, value, way);
                    break;
                case 4:
                    print(root);
                    std::cout << std::endl;
                    break;
                case 5:
                    printWithWay(root);
                    break;
                case 6:
                    std::cout << "enter value for the element" << std::endl;
                    std::cin >> value;
                    if (std::cin.fail()) return;
                    deleted = deleteAndPrintByElement(value, root);
                    if (deleted != nullptr) {
                        print(deleted);
                        std::cout << std::endl;
                    } else {
                        std::cout << "there is no such element" << std::endl;
                    }
                    break;
                case 7:
                    std::cout << "enter value for the element" << std::endl;
                    std::cin >> value;
                    if (std::cin.fail()) return;
                    deleteByElement(value, root);
                    break;
                case 8:
                    std::cout << "how long is your way to the parent of the element" << std::endl;
                    std::cin >> size;
                    if (std::cin.fail() || size < 0) return;
                    for (int i = 0; i < size; ++i) {
                        std::cout << "enter value for the way" << std::endl;
                        std::cin >> value;
                        if (std::cin.fail()) return;
                        way.push_back(value);
                    }
                    if(way.empty()){
                        print(root);
                        std::cout << std::endl;
                        deleteTree(root);
                        std::cout << "you have just deleted the whole tree" << std::endl;
                        return;
                    }
                    deleted = deleteByWay(way, root);
                    if (deleted != nullptr) {
                        print(deleted);
                    } else {
                        std::cout << "there is no such element" << std::endl;
                    }
                    break;
                default:
                    return;
            }
        }
    }
    else if(choose==2) {
        std::cout << "enter the value for the root" << std::endl;
        std::cin >> value;
        if (std::cin.fail()) return;
        BinaryTree *root = new BinaryTree(value);
        while (true) {
            std::cout << "choose what to do:\n"
                         "1. Add an element\n"
                         "2. Print the tree with ()\n"
                         "3. Print the tree with way for each element\n"
                         "4. Print the tree with straight order"
                      << std::endl;
            std::cin >> choose;
            if (std::cin.fail()) return;
            std::vector<int> way = {};
            switch (choose) {
                case 1:
                    std::cout << "enter value of the element" << std::endl;
                    std::cin >> value;
                    if (std::cin.fail()) return;
                    addToBinary(value, root);

                    break;
                case 2:
                    print(root);
                    std::cout << std::endl;
                    break;
                case 3:
                    printWithWay(root);
                    std::cout << std::endl;
                    break;
                case 4:
                    printStraightOrder(root);
                    std::cout << std::endl;
                    break;
                default:
                    return;
            }
        }
    }
     else if(choose==3) {
    }
     else{
            return;
    }

}
int main() {
    interactive();
    return 0;
}
