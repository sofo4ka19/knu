#include <iostream>
#include <chrono>
#include <random>

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
void listPrint(Node* start)
{
    Node *current = start;
    if(current == nullptr){
        std::cout << "list is empty" << std::endl;
    }
    else {
        while (current != nullptr) {
            std::cout << current->value << " ";
            current = current->next;
        }
        std::cout << std::endl;
    }
}

void addElement(LinkedList& list, int value){
    Node* new_node = new Node(value, list.end);
    (list.start == nullptr)?(list.start = new_node):(list.end->next = new_node);
    list.end = new_node;
}
LinkedList interleave(LinkedList list1, LinkedList list2){
    LinkedList list;
    while(list1.start!= nullptr || list2.start!= nullptr){
        if(list1.start!= nullptr){
            addElement(list, list1.start->value);
            list1.start=list1.start->next;
        }
        if(list2.start!= nullptr){
            addElement(list, list2.start->value);
            list2.start=list2.start->next;
        }
    }
    return list;
}
LinkedList rotate(LinkedList list, int begin, int end, int new_begin){
    LinkedList result, add;
    int i=0;
    while(list.start!= nullptr) {
        if(i<begin || i>=new_begin){
            addElement(result, list.start->value);
            if(i==end){
                while(add.start!= nullptr){
                    addElement(result, add.start->value);
                    add.start=add.start->next;
                }
            }
        }
        else{
            addElement(add, list.start->value);
        }
        list.start=list.start->next;
        i++;
    }
    return result;
}
void fillList(LinkedList& list){
    while(true){
        int el;
        std::cin >> el;
        if(std::cin.fail()){
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            break;
        }
        else{
            addElement(list, el);
        }
    }
}
void interactive(LinkedList& list1, LinkedList& list2){
    int choose;
    std::cout << "what function you want to have? 1 - interleave, 2 - rotate" << std::endl;
    std::cin >> choose;
    switch (choose) {
        case 1:
            std::cout << "fill the first list (to exit enter a symbol)" << std::endl;
            fillList(list1);
            listPrint(list1.start);
            std::cout << "fill the second list (to exit enter a symbol)" << std::endl;
            fillList(list2);
            listPrint(list2.start);
            std::cout << "the result of interleave" << std::endl;
            listPrint(interleave(list1, list2).start);
            break;
        case 2:
            std::cout << "fill the list (to exit enter a symbol)" << std::endl;
            fillList(list1);
            listPrint(list1.start);
            int begin, end, new_begin;
            std::cout << "enter begin, end, new_begin" << std::endl;
            std::cin >> begin >> end >> new_begin;
            std::cout << "the result of rotate" << std::endl;
            listPrint(rotate(list1, begin, end, new_begin).start);
            break;
        default:
            break;
    }

}
void demo(LinkedList& list1, LinkedList& list2){
    std::cout << "fill the first list: 1 2 3 4 5; and the second: 6 7 8 9 10" << std::endl;
    for(int i=1; i<=5; i++){
        addElement(list1, i);
        addElement(list2, i+5);
    }
    std::cout << "the result of interleave" << std::endl;
    listPrint(interleave(list1, list2).start);
    std::cout << "add 11 12 13 14 to second list" << std::endl;
    for(int i=11; i<=14; i++){
        addElement(list2, i);
    }
    std::cout << "the result of interleave" << std::endl;
    listPrint(interleave(list1, list2).start);
}
void benchmark(){
    std::random_device rd;
    std::mt19937 mersenne(rd());
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;
    int N=100, N1;
    bool isEnd;
    do{
        LinkedList list1, list2;
        auto t0 = high_resolution_clock::now();
        for(int i=0; i<N; i++){
            addElement(list1, rand()%1000);
            addElement(list2, rand()%1000);
        }
        auto t1 = high_resolution_clock::now();
        interleave(list1, list2);
        auto t2 = high_resolution_clock::now();
        for(int i=0; i<N; i++){
            addElement(list2, rand()%1000);
        }
        auto t3 = high_resolution_clock::now();
        interleave(list1, list2);
        auto t4 = high_resolution_clock::now();
        duration<double, std::milli> ms_double1 = t2-t1;
        duration<double, std::milli> ms_double2 = t4-t3;
        std::cout << "for " << N << " elements in both arrays, time of interleave is " << ms_double1.count() << "ms; if we add " << N << " elements to the second array, time of interleave is " << ms_double2.count() << "ms" << std::endl;
        isEnd = ms_double2.count()<1500.0;
        if(ms_double2.count()<1000.0){
            N*=2;
            N1=N;
        }
        else{
            N+=N1;
        }
    }while(isEnd);
}
int main() {
    LinkedList list1;
    LinkedList list2;
    int mode;
    std::cout << "Choose the mode: 1 - interactive; 2 - demonstration; 3 - benchmark" << std::endl;
    std::cin >> mode;
    switch (mode) {
        case 1:
            interactive(list1, list2);
            break;
        case 2:
            demo(list1, list2);
            break;
        case 3:
            benchmark();
            break;
        default:
            std::cout << "error";
            break;
    }
    return 0;
}
