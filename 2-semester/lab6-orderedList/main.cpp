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
    int findNum(const Node* item){
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
    void fillRandom(int n){
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
            addElement(item);
        }
    }
};
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
                if(list.findElement(value)!= nullptr) {
                    std::cout << "this element has number " << list.findNum(list.findElement(value)) << " in order"
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
                list.fillRandom(n);
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
    switch (type) {
        case 1:
            LinkedList list;
            interactiveChoose(list);

    }
}
int main() {
    interactive();
    return 0;
}
