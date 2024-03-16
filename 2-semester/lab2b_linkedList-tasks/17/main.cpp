#include <iostream>
#include <vector>
#include <limits>

struct Node{
    int value;
    Node* prev;
    Node* next;

    Node(int value, Node* prev = nullptr, Node* next = nullptr): value(value), prev(prev), next(next) { }
};
struct LinkedList {
    Node* start;
    Node* end;

    LinkedList(Node* start = nullptr, Node* end = nullptr): start(start), end(end) {}
};
void listPrint(Node* start, Node* end)
{
    Node *current = start;
    if(current == nullptr){
        std::cout << "list is empty" << std::endl;
    }
    else {
        do {
            std::cout << current->value << " ";
            current = current->next;
        }while(current!=start);
        std::cout << std::endl;
    }
}
void addElement(LinkedList& list, int value){
    Node* new_node = new Node(value, list.end);
    (list.start== nullptr)?(list.start = new_node):(list.end->next = new_node);
    list.end = new_node;
    list.start->prev=list.end;
    list.end->next=list.start;
}
void task(Node* start, std::vector<int> step, const int& type, const int add=0, int N=0) {
    Node *current = start;
    int i = 0, j = 0, k = 0;
    while (current != current->prev) {
        if (i == step[j]) {
            current->prev->next = current->next;
            current->next->prev = current->prev;
            switch (type) {
                case 1:
                    std::cout << current->value << " ";
                    break;
                case 2:
                    k++;
                    if (current->value == add) {
                        std::cout << k << std::endl;
                    }
                    break;
                case 3:
                    k++;
                    if (N - k == add) {
                        std::cout << current->value << std::endl;
                    }
                    break;
                default:
                    break;
            }
            i = 0;
            (j == step.size() - 1) ? (j = 0) : (j++);
        } else {
            i++;
        }
        current = current->next;
    }
    if (type == 1 || (type == 3 && add == 0)) {
        std::cout << current->value << std::endl;
    } else if (type == 2 && add == current->value) {
        std::cout << ++k << std::endl;
    }
}
int main(){
    LinkedList list;
    int N;
    do {
        std::cout << "enter a number of elements" << std::endl;
        std::cin >> N;
    }while(N<1);
    for(int i=1; i<=N; i++){
        addElement(list, i);
    }
    std::cout << "your list contain next elements" << std::endl;
    listPrint(list.start, list.end);
    std::vector<int> KK;
    int step;
    while(true){
        std::cout << "enter a step (if it is the end, enter a symbol)" << std::endl;
        std::cin >> step;
        if(std::cin.fail()){
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            break;
        }
        else{
            KK.push_back(step);
        }
    }
    int choose, add;
    std::cout << "choose what to print: 1 - list of elements in order of deleting; 2 - which in order was an element; 3 - which element was deleted in a number from the end" << std::endl;
    std::cin >> choose;
    switch (choose) {
        case 2:
            std::cout << "enter an element" << std::endl;
            std::cin >> add;
            break;
        case 3:
            std::cout << "enter a number of order position from the end" << std::endl;
            std::cin >> add;
            break;
        default:
            break;

    }
    task(list.start, KK, choose, add, N);
    return 0;
}
