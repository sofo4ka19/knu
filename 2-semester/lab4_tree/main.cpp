//Block 1: 2, 3
//Block 2: 7, 11
//Block 3: 13, 14, 15
//Block 4: 18
//Block 5: 21?
//Block 6: 22

#include <iostream>
#include <vector>
#include <iomanip>

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
void interactive(){
    std::cout << "enter the value for the root" << std::endl;
    int value, choose;
    std::cin >> value;
    if(std::cin.fail()) return;
    TreeNode* root = new TreeNode(value);
    while(true) {
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
        TreeNode* deleted;
        switch (choose) {
            case 1:
                std::cout << "enter value of the element" << std::endl;
                std::cin >> value;
                if (std::cin.fail()) return;
                way= findTheWay(value, root);
                if(way.empty() && value!=root->value){
                    std::cout << "there is no such element" << std::endl;
                }
                else{
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
                if(findTheElement(way, root)!= nullptr) std::cout << findTheElement(way, root)->value << std::endl;
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
                if(deleted != nullptr){
                    print(deleted);
                    std::cout << std::endl;
                } else{
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
                deleted = deleteByWay(way, root);
                if(deleted != nullptr){
                    print(deleted);
                } else{
                    std::cout << "there is no such element" << std::endl;
                }
                break;
            default:
                return;
        }
    }
}
int main() {
    interactive();
    return 0;
}
