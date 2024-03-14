#include <iostream>
#include <vector>

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

void addElement(LinkedList& list, int value){
    Node* new_node = new Node(value, list.end, list.start);
    (list.start == nullptr)?(list.start = new_node):(list.end->next = new_node);
    list.end = new_node;
    list.start->prev = list.end;
}
void task(LinkedList& list, std::vector<int> step){
    Node* current = list.start;
    int n = step[0];
    for(int i=1; i<=n; i++){
        current = current->next;
        if(i==n){

        }
    }
}

int main(){
    LinkedList list;
    list.start = nullptr;
    list.end = nullptr;
    int N;
    do {
        std::cout << "enter a number of elements" << std::endl;
        std::cin >> N;
    }while(N<1);
    std::vector<int> KK;
    int step;
    while(true){
        std::cout << "enter a step (if it is the end enter a symbol)" << std::endl;
        std::cin >> step;
        if(std::cin.fail()){
            break;
        }
        else{
            KK.push_back(step);
        }
    }
    char choose;
    std::cout << "do you want to fill your list manually (m) or automatically (a)?" << std::endl;
    std::cin >> choose;
    switch (choose) {
        case 'm':
            for(int i=0; i<N; i++) {
                int num;
                std::cout << "enter your element" << std::endl;
                std::cin >> num;
                    addElement(list, num);
            }
        case 'a':
            for(int i=0; i<N; i++){
                addElement(list, rand()%1000);
            }
    }
    return 0;
}