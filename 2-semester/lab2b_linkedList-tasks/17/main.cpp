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

}
