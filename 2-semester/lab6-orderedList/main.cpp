//Текстові рядки, спершу за довжиною, за зростанням (“A”<”B”<”AA”<”AB”)
#include <iostream>
#include <random>

bool comparison(const std::string& v1, const std::string& v2){
    if(v1.size()==v2.size()){
        for (int i = 0; i < v1.size(); ++i) {
            if (v1[i]!=v2[i]) return v2[i]>v1[i];
        }
    }
    return v2.size()>v1.size();
}
bool check(std::string& data){
    for (int i = 0; i < data.size(); ++i) {
        if(data[i]<65 || data[i]>90){
            if (data[i]<97 || data[i]>122){
                return false;
            }
            data[i]-=32;
        }
    }
    return true;
}

struct Node{
    std::string value;
    Node* prev;
    Node* next;

    Node(std::string value, Node* prev = nullptr, Node* next = nullptr): value(value), prev(prev), next(next) { }

};
struct LinkedList {
    Node* start;
    Node* end;

    LinkedList(Node* start = nullptr, Node* end = nullptr): start(start), end(end) {}

    void addElement(const std::string& data) {
        Node* newNode = new Node(data);
        if (start == nullptr) {
            // for an empty list
            start = end = newNode;
        } else if (comparison(end->value, data)) {
            // add to the end
            newNode->prev = end;
            end->next = newNode;
            end = newNode;
        } else if (comparison(data, start->value)) {
            // add to the start
            newNode->next = start;
            start->prev = newNode;
            start = newNode;
        } else {
            Node* current = start;
            while (current != nullptr && comparison(current->value, data)) {
                current = current->next;
            }
            newNode->prev = current->prev;
            newNode->next = current;
            current->prev->next = newNode;
            current->prev = newNode;
        }
    }
    void deleteElement(std::string data){
        if (start == nullptr){
            std::cout << "Sorry, your list is empty" << std::endl;
            return;
        } else if(start->value == data){
            Node* newStart = start->next;
            delete start;
            start = newStart;
            start->prev= nullptr;
        } else if(end->value == data){
            Node* newEnd = end->prev;
            delete end;
            end = newEnd;
            end->next= nullptr;
        } else{
            Node* current = start;
            while (current!= nullptr && current->value!=data){
                current=current->next;
            }
            if (current== nullptr){
                std::cout << "there is no such element" << std::endl;
                return;
            }
            current->prev->next = current->next;
            current->next->prev = current->prev;
            delete current;
        }
    }
    int findNum(const std::string& data){
        Node* item = findElement(data);
        if (start== nullptr || item== nullptr){
            return 0;
        }
        Node* current = start;
        int n = 1;
        while (current!=item){
            current=current->next;
            n++;
        }
        return n;
    }
    Node* findElement(const std::string& data){
        if (start == nullptr){
            std::cout << "Sorry, your list is empty" << std::endl;
            return nullptr;
        } else if(start->value == data){
            return start;
        } else if(end->value == data){
            return end;
        } else{
            Node* current = start;
            while (current!= nullptr && current->value!=data){
                current=current->next;
            }
            if (current== nullptr){
                std::cout << "there is no such element" << std::endl;
                return nullptr;
            }
            else{
                return current;
            }
        }
    }
    LinkedList findInterval(std::string v1, std::string v2){
        if (start== nullptr){
            std::cout << "Sorry, your list is empty" << std::endl;
            return nullptr;
        }
        if (comparison(v2,v1) || comparison(v2, start->value) || comparison(end->value, v1)){
            std::cout << "Inappropriate values" << std::endl;
            return nullptr;
        }
        LinkedList result;
        if(findElement(v1)!= nullptr){
            result.start = findElement(v1);
        }
        else{
            Node* current = start;
            while(current!= nullptr && comparison(current->value, v1)){
                current=current->next;
            }
            result.start=current;
        }
        if (findElement(v2)!= nullptr){
            result.end = findElement(v2);
        } else{
            Node* current = end;
            while(current!= nullptr && comparison(v2, current->value)){
                current=current->prev;
            }
            result.end=current;
        }
        if (comparison(result.end->value, result.start->value)){
            std::cout << "There is no elements in such interval" << std::endl;
            return nullptr;
        }
        result.start->prev = nullptr;
        result.end->next = nullptr;
        return result;
    }
    void print(){
        if (start== nullptr){
            std::cout << "your list is empty" << std::endl;
            return;
        }
        else{
            Node* current = start;
            while (current!= nullptr){
                std::cout << current->value << " ";
                current=current->next;
            }
            std::cout << std::endl;
        }
    }
};

struct ArrayList{
    std::vector<std::string> list;

    void addElement(const std::string& data){
        for (int i = 0; i < list.size(); ++i) {
            if (comparison(data, list[i])){
                list.insert(list.begin()+i, data);
                return;
            }
        }
        list.push_back(data);
    }
    int findNum(const std::string& data){
        for (int i = 0; i < list.size(); ++i) {
            if (list[i]==data) return i+1;
        }
        std::cout << "there is no such element" << std::endl;
        return 0;
    }
    void deleteElement(const std::string& data){
        if (list.empty()){
            std::cout << "Sorry, your list is empty" << std::endl;
        }
        else if (findNum(data)!=0){
            list.erase(list.begin()+findNum(data)-1);
        }
    }
    ArrayList findInterval(std::string v1, std::string v2){
        if (list.empty()){
            std::cout << "Sorry, your list is empty" << std::endl;
            return {};
        }
        if (comparison(v2,v1) || comparison(v2, list[0]) || comparison(list[list.size()-1], v1)){
            std::cout << "Inappropriate values" << std::endl;
            return {};
        }
        ArrayList result;
        int v0,v;
        if(findNum(v1) != 0){
            v0 = findNum(v1)-1;
        }
        else{
            int i=0;
            while(i<list.size()-1 && comparison(list[i], v1)){
                i++;
            }
            v0=i;
        }
        if (findNum(v2)!= 0){
            v = findNum(v2)-1;
        } else{
            int i=list.size()-1;
            while(i>0 && comparison(v2, list[i])){
                i--;
            }
            v=i;
        }
        if (v0>v){
            std::cout << "There is no elements in such interval" << std::endl;
            return {};
        }
        result.list.assign(list.begin()+v0, list.begin()+v+1);
        return result;
    }
    void print(){
        if (list.empty()){
            std::cout << "Sorry, your list is empty" << std::endl;
            return;
        }
        for (const auto & i : list) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
};

struct BinaryTreeNode{
    std::string value;
    BinaryTreeNode* left;
    BinaryTreeNode* right;

    BinaryTreeNode(const std::string& value): value{value}, left{nullptr}, right{nullptr} {}

};
struct BinaryTree{
    BinaryTreeNode* root;

    BinaryTree() : root(nullptr) {}

    void addElement(const std::string& data){
        if(root== nullptr){
            root = new BinaryTreeNode(data);
        }
        else{
            addElement2(data, root);
        }
    }
    void addElement2(const std::string& data, BinaryTreeNode* node){
        if (comparison(node->value, data)){
            if (node->right== nullptr){
                node->right = new BinaryTreeNode(data);
            } else{
                addElement2(data, node->right);
            }
        } else{
            if (node->left== nullptr){
                node->left= new BinaryTreeNode(data);
            } else{
                addElement2(data, node->left);
            }
        }
    }

    BinaryTreeNode* findElement(const std::string& data) {
        return findElementHelper(root, data);
    }

    BinaryTreeNode* findElementHelper(BinaryTreeNode* node, const std::string& data) {
        if (node == nullptr || node->value == data) {
            return node;
        }
        if (comparison(node->value, data)) {
            return findElementHelper(node->right, data);
        }
        return findElementHelper(node->left, data);
    }

    int countNodes(BinaryTreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        return 1 + countNodes(node->left) + countNodes(node->right);
    }
    int findNum(const std::string& data) {
        if (findElement(data)!= nullptr){
            return countNodes(findElement(data)->left)+1;
        }
        std::cout << "there is no such element" << std::endl;
        return 0;
    }


    void deleteElement(const std::string& data) {
        root = deleteElementHelper(root, data);
    }

    BinaryTreeNode* findMin(BinaryTreeNode* node) {
        while (node->left != nullptr) {
            node = node->left;
        }
        return node;
    }

    BinaryTreeNode* deleteElementHelper(BinaryTreeNode* node, const std::string& data) {
        if (node == nullptr) {
            std::cout << "Element " << data << " not found" << std::endl;
            return node;
        }
        if(node->value==data){
            if (node->left == nullptr) {
                BinaryTreeNode* temp = node->right;
                delete node;
                return temp;
            } else if (node->right == nullptr) {
                BinaryTreeNode* temp = node->left;
                delete node;
                return temp;
            }
            BinaryTreeNode* temp = findMin(node->right);
            node->value = temp->value;
            node->right = deleteElementHelper(node->right, temp->value);
        } else if (comparison(node->value, data)) {
            node->right = deleteElementHelper(node->right, data);
        } else {
            node->left = deleteElementHelper(node->left, data);
         }
        return node;
    }
    BinaryTreeNode* findMax(BinaryTreeNode* node) {
        while (node->right != nullptr) {
            node = node->right;
        }
        return node;
    }
    BinaryTreeNode* findClosestElement(BinaryTreeNode* node, const std::string& value, bool isStart) {
        BinaryTreeNode* closest = nullptr;
        while (node != nullptr) {
            if (isStart) {
                if (node->value == value || comparison(value, node->value)) {
                    closest = node;
                    node = node->left;
                } else {
                    node = node->right;
                }
            } else {
                if (node->value == value || comparison(node->value, value)) {
                    closest = node;
                    node = node->right;
                } else {
                    node = node->left;
                }
            }
        }
        return closest;
    }
    BinaryTree findInterval(const std::string& v1, const std::string& v2) {
        BinaryTree result;
        if (root == nullptr) {
            std::cout << "Tree is empty" << std::endl;
            return result;
        }
        if (comparison(v2, v1) || comparison(v2, findMin(root)->value) || comparison(findMax(root)->value, v1)) {
            std::cout << "Invalid interval" << std::endl;
            return result;
        }
        BinaryTreeNode* start = findClosestElement(root, v1, true);
        BinaryTreeNode* end = findClosestElement(root, v2, false);
        if (start == nullptr || end == nullptr || start->value > end->value) {
            std::cout << "No elements in the given interval" << std::endl;
            return result;
        }
        copyInterval(root, start->value, end->value, result);
        return result;
    }
    void copyInterval(BinaryTreeNode* node, const std::string& v1, const std::string& v2, BinaryTree& result) {
        if (node == nullptr) {
            return;
        }
        if (comparison(v1, node->value)) {
            copyInterval(node->left, v1, v2, result);
        }
        if ((node->value == v1 || comparison(v1, node->value)) && (node->value == v2 || comparison(node->value, v2))) {
            result.addElement(node->value);
        }
        if (comparison(node->value, v2)) {
            copyInterval(node->right, v1, v2, result);
        }
    }
    void print() {
        if (root!= nullptr){
            printSubtree(root);
            std::cout << std::endl;
            return;
        }
        std::cout << "tree is empty" << std::endl;
        return;
    }

    void printSubtree(BinaryTreeNode* node) {
        if (node == nullptr) {
            return;
        }
        printSubtree(node->left);
        std::cout << node->value << " ";
        printSubtree(node->right);
    }
};
struct AVLTreeNode{
    std::string value;
    AVLTreeNode* left;
    AVLTreeNode* right;
    int height;

    AVLTreeNode(const std::string& value)
            : value(value), left(nullptr), right(nullptr), height(1) {}

};
struct AVLTree{
    AVLTreeNode* root;

    AVLTree(): root(nullptr) {}

    int height(AVLTreeNode* node) {
        return node!= nullptr ? node->height : 0;
    }

    int getBalance(AVLTreeNode* node) {
        return node!= nullptr ? height(node->left) - height(node->right) : 0;
    }

    AVLTreeNode* rightRotate(AVLTreeNode* y) {
        AVLTreeNode* x = y->left;
        AVLTreeNode* T2 = x->right;
        x->right = y;
        y->left = T2;
        y->height = std::max(height(y->left), height(y->right)) + 1;
        x->height = std::max(height(x->left), height(x->right)) + 1;
        return x;
    }

    AVLTreeNode* leftRotate(AVLTreeNode* x) {
        AVLTreeNode* y = x->right;
        AVLTreeNode* T2 = y->left;
        y->left = x;
        x->right = T2;
        x->height = std::max(height(x->left), height(x->right)) + 1;
        y->height = std::max(height(y->left), height(y->right)) + 1;
        return y;
    }

    void addElement(const std::string& value){
        root = addElement2(value, root);
    }
    AVLTreeNode* addElement2(const std::string& value, AVLTreeNode* node) {
        if (node== nullptr) return new AVLTreeNode(value);
        if (comparison(value,node->value)) node->left = addElement2(value, node->left);
        else if (comparison(node->value,value)) node->right = addElement2(value, node->right);
        else return node;

        node->height = 1 + std::max(height(node->left), height(node->right));
        int balance = getBalance(node);

        if (balance > 1 && comparison(value,node->left->value)) return rightRotate(node);
        if (balance < -1 && comparison(node->right->value, value)) return leftRotate(node);
        if (balance > 1 && comparison(node->left->value, value)) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }
        if (balance < -1 && comparison(value, node->right->value)) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }
        return node;
    }
    void deleteElement(const std::string& value) {
        root = deleteHelper(root, value);
    }

    AVLTreeNode* deleteHelper(AVLTreeNode* root, const std::string& value) {
        if (!root) {
            std::cout << "Sorry, there is no such element" << std::endl;
            return root;
        }
        if (value < root->value) root->left = deleteHelper(root->left, value);
        else if (value > root->value) root->right = deleteHelper(root->right, value);
        else {
            if (!root->left || !root->right) {
                AVLTreeNode* temp = root->left ? root->left : root->right;
                if (!temp) {
                    temp = root;
                    root = nullptr;
                } else *root = *temp;
                delete temp;
            } else {
                AVLTreeNode* temp = minValueNode(root->right);
                root->value = temp->value;
                root->right = deleteHelper(root->right, temp->value);
            }
        }
        if (!root) return root;
        root->height = 1 + std::max(height(root->left), height(root->right));
        int balance = getBalance(root);
        if (balance > 1 && getBalance(root->left) >= 0) return rightRotate(root);
        if (balance > 1 && getBalance(root->left) < 0) {
            root->left = leftRotate(root->left);
            return rightRotate(root);
        }
        if (balance < -1 && getBalance(root->right) <= 0) return leftRotate(root);
        if (balance < -1 && getBalance(root->right) > 0) {
            root->right = rightRotate(root->right);
            return leftRotate(root);
        }
        return root;
    }
    AVLTreeNode* minValueNode(AVLTreeNode* node) {
        AVLTreeNode* current = node;
        while (current->left != nullptr) current = current->left;
        return current;
    }
    int countNodes(AVLTreeNode* node) {
        if (node == nullptr) {
            return 0;
        }
        return 1 + countNodes(node->left) + countNodes(node->right);
    }
    int findNum(const std::string& data) {
        if (findElement(data)!= nullptr){
            return countNodes(findElement(data)->left)+1;
        }
        std::cout << "there is no such element" << std::endl;
        return 0;
    }

    AVLTreeNode* findElement(const std::string& value) {
        return findElementHelper(root, value);
    }

    AVLTreeNode* findElementHelper(AVLTreeNode* node, const std::string& value) {
        if (!node) {
            std::cout << "Sorry, there is no such element" << std::endl;
            return nullptr;
        }
        if (value == node->value) return node;
        if (comparison(value, node->value)) return findElementHelper(node->left, value);
        return findElementHelper(node->right, value);
    }
    AVLTreeNode* findMax(AVLTreeNode* node) {
        while (node->right != nullptr) {
            node = node->right;
        }
        return node;
    }
    AVLTreeNode* findClosestElement(AVLTreeNode* node, const std::string& value, bool isStart) {
        AVLTreeNode* closest = nullptr;
        while (node != nullptr) {
            if (isStart) {
                if (node->value == value || comparison(value, node->value)) {
                    closest = node;
                    node = node->left;
                } else {
                    node = node->right;
                }
            } else {
                if (node->value == value || comparison(node->value, value)) {
                    closest = node;
                    node = node->right;
                } else {
                    node = node->left;
                }
            }
        }
        return closest;
    }
    AVLTree findInterval(const std::string& v1, const std::string& v2) {
        AVLTree result;
        if (root == nullptr) {
            std::cout << "Tree is empty" << std::endl;
            return result;
        }
        if (comparison(v2, v1) || comparison(v2, minValueNode(root)->value) || comparison(findMax(root)->value, v1)) {
            std::cout << "Invalid interval" << std::endl;
            return result;
        }
        AVLTreeNode* start = findClosestElement(root, v1, true);
        AVLTreeNode* end = findClosestElement(root, v2, false);
        if (start == nullptr || end == nullptr || start->value > end->value) {
            std::cout << "No elements in the given interval" << std::endl;
            return result;
        }
        copyInterval(root, start->value, end->value, result);
        return result;
    }
    void copyInterval(AVLTreeNode* node, const std::string& v1, const std::string& v2, AVLTree& result) {
        if (node == nullptr) {
            return;
        }
        if (comparison(v1, node->value)) {
            copyInterval(node->left, v1, v2, result);
        }
        if ((node->value == v1 || comparison(v1, node->value)) && (node->value == v2 || comparison(node->value, v2))) {
            result.addElement(node->value);
        }
        if (comparison(node->value, v2)) {
            copyInterval(node->right, v1, v2, result);
        }
    }

    void print() {
        if (root== nullptr){
            std::cout << "Tree is empty" << std::endl;
            return;
        }
        printSubtree(root);
        std::cout << std::endl;
    }

    void printSubtree(AVLTreeNode* node) {
        if (!node) return;
        printSubtree(node->left);
        std::cout << node->value << " ";
        printSubtree(node->right);
    }
};
template <typename ListType>
void fillRandom(int n, ListType& list){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> length(1, 10);
    std::uniform_int_distribution<> code(65, 90);
    for (int i = 0; i < n; ++i) {
        std::string item;
        int len = length(gen);
        for (int j=0; j<len; j++){
            char c = code(gen);
            item+=c;
        }
        list.addElement(item);
    }
}
template <typename ListType>
void interactiveChoose(ListType& list){
    while (true){
        std::cout << "choose what you want to do:\n"
                     "1. add an element\n"
                     "2. delete an element\n"
                     "3. find an element\n"
                     "4. find elements in interval\n"
                     "5. print the list\n"
                     "6. fill with random values\n"
                     "7. exit"
                     << std::endl;
        int action;
        std::cin >> action;
        if (std::cin.fail() || action<1 || action> 7){
            std::cout << "error" << std::endl;
            return;
        }
        std::string value, value2;
        int n;
        switch (action) {
            case 1:
                std::cout << "enter the value" << std::endl;
                std::cin >> value;
                if (std::cin.fail() || !check(value)){
                    std::cout << "Inappropriate value" << std::endl;
                    return;
                }
                list.addElement(value);
                break;
            case 2:
                std::cout << "enter the value" << std::endl;
                std::cin >> value;
                if (std::cin.fail() || !check(value)){
                    std::cout << "Inappropriate value" << std::endl;
                    return;
                }
                list.deleteElement(value);
                break;
            case 3:
                std::cout << "enter the value" << std::endl;
                std::cin >> value;
                if (std::cin.fail() || !check(value)){
                    std::cout << "Inappropriate value" << std::endl;
                    return;
                }
                if(list.findNum(value)!= 0) {
                    std::cout << "this element has number " << list.findNum(value) << " in order"
                              << std::endl;
                }
                break;
            case 4:
                std::cout << "enter the start and the end of the interval" << std::endl;
                std::cin >> value >> value2;
                if (std::cin.fail() || !check(value) || !check(value2)){
                    std::cout << "Inappropriate value" << std::endl;
                    return;
                }
                list.findInterval(value, value2).print();
                break;
            case 5:
                list.print();
                break;
            case 6:
                std::cout << "enter number of elements" << std::endl;
                std::cin >> n;
                if (std::cin.fail()){
                    std::cout << "error" << std::endl;
                    return;
                }
                fillRandom(n, list);
                break;
            case 7:
                return;
            default:
                return;
        }
    }
}

void interactive(){
    std::cout << "choose with which type of ordered list you want to work:\n"
                 "1. Linked list\n"
                 "2. Array list\n"
                 "3. Binary search tree\n"
                 "4. AVL tree\n"
                 "5. 2-3 tree"
                 << std::endl;
    int type;
    std::cin >> type;
    if (std::cin.fail() || type<1 || type>5){
        std::cout << "Invalid value" << std::endl;
        return;
    }
    if (type==1){
        LinkedList list;
        interactiveChoose(list);
    } else if(type == 2){
        ArrayList list;
        interactiveChoose(list);
    } else if(type==3){
        BinaryTree list;
        interactiveChoose(list);
    } else if(type==4){
        AVLTree list;
        interactiveChoose(list);
    }
}
int main() {
    interactive();
    return 0;
}
