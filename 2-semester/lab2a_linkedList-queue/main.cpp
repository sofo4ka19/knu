#include <iostream>
#include <vector>

struct Point{
    float x;
    float y;
    float z;
};
struct Node{
    Point value;
    Node* prev;
    Node* next;

    Node(Point value, Node* prev = nullptr, Node* next = nullptr): value(value), prev(prev), next(next) { }
};
struct LinkedList {
    Node* start;
    Node* end;

    LinkedList(Node* start = nullptr, Node* end = nullptr): start(start), end(end) {}
};
bool is_empty(std::vector<Point>& array){
    return array.empty();
}
void print(std::vector<Point>& array){
    if (is_empty(array)){
        std::cout << "array is empty" << std::endl;
    }
    else{
        for(int i=0; i<array.size(); i++) {
            std::cout << "(" << array[i].x << ";" << array[i].y << ";" << array[i].z << ")" << std::endl;
        }
    }
}
/*void create_empty(){
    std::vector<Point> array = {};
}*/
Point enqueue(){
    Point add;
    std::cout << "enter x coordinate" << std::endl;
    std::cin >> add.x;
    std::cout << "enter y coordinate" << std::endl;
    std::cin >> add.y;
    std::cout << "enter z coordinate" << std::endl;
    std::cin >> add.z;
    return add;
}
void dequeue(std::vector<Point>& array){
    if (is_empty(array)){
        std::cout << "array is empty" << std::endl;
    }
    else{
        array.erase(array.begin());
        std::cout << "first element was deleted" << std::endl;
    }
}
bool staticIsEmpty(int& index){
    if(index==0){
        return true;
    }
    else{
        return false;
    }
}
void staticEnqueue(Point *array, int size, int& index){
    if(index==size){
        std::cout << "Error. Your array is full" << std::endl;
    }
    else{
        array[index]=enqueue();
        index++;
    }
}
void staticDequeue(Point *array, int& index){
    if(staticIsEmpty(index)){
        std::cout << "array is empty" << std::endl;
    }
    else{
        for (int i = 0; i < index-1; ++i) {
            array[i]=array[i+1];
        }
        index--;
        std::cout << "first element was deleted" << std::endl;
    }
}
void staticPrint(Point *array, int& index){
    if (staticIsEmpty(index)){
        std::cout << "array is empty" << std::endl;
    }
    else{
        for(int i=0; i<index; i++) {
            std::cout << "(" << array[i].x << ";" << array[i].y << ";" << array[i].z << ")" << std::endl;
        }
    }
}
void listPrint(Node* start)
{
    Node *current = start;
    if(current == nullptr){
        std::cout << "list is empty" << std::endl;
    }
    else {
        while (current != nullptr) {
            std::cout << "(" << current->value.x << ";" << current->value.y << ";" << current->value.z << ")"
                      << std::endl;
            current = current->next;
        }
    }
}
bool listIsEmpty(LinkedList& list){
    return (list.start == nullptr);
}
void listEnqueue(LinkedList& list, Point value = enqueue()){
    Node* new_node = new Node(value, list.end);
    listIsEmpty(list)?(list.start = new_node):(list.end->next = new_node);
    /*if (list.end == nullptr) {
        list.start = new_node;
    } else {
        list.end->next = new_node;
    }*/
    list.end = new_node;
}
void listDequeue(LinkedList& list){
    if(listIsEmpty(list)){
        std::cout << "list is empty" << std::endl;
    }
    else{
        Node* new_start = list.start->next;
        delete list.start;
        list.start = new_start;
        list.start->prev = nullptr;
        std::cout << "first element was deleted" << std::endl;
    }
}
int main() {
    int type, action=0;
    std::vector<Point> array;
    bool isEnd = false;
    Point* static_array = nullptr;
    LinkedList list;
    do{
        bool anotherType = false;
        std::cout << "choose type of the list: 1 - static array; 2 - vector (dynamic array); 3 - linked list" << std::endl;
        std::cin >> type;
        do {
            switch (type) {
                case 1:
                    int index;
                    switch (action) {
                        case 0:
                            int N;
                            index = 0;
                            std::cout << "enter the number of elements in the static array" << std::endl;
                            std::cin >> N;
                            static_array = new Point[N];
                            break;
                        case 1:
                            staticEnqueue(static_array, N, index);
                            break;
                        case 2:
                            staticDequeue(static_array, index);
                            break;
                        case 3:
                            if (staticIsEmpty(index)) {
                                std::cout << "array is empty" << std::endl;
                            } else {
                                std::cout << "array is not empty" << std::endl;
                            }
                            break;
                        case 4:
                            staticPrint(static_array, index);
                            break;
                        default:
                            anotherType = true;
                            delete[] static_array;
                            break;
                    }
                    break;
                case 2:
                    switch (action) {
                        case 0:
                            array = {};
                            break;
                        case 1:
                            array.push_back(enqueue());
                            break;
                        case 2:
                            dequeue(array);
                            break;
                        case 3:
                            if (is_empty(array)) {
                                std::cout << "array is empty" << std::endl;
                            } else { std::cout << "array is not empty" << std::endl; }
                            break;
                        case 4:
                            print(array);
                            break;
                        default:
                            anotherType=true;
                            break;
                    }
                    break;
                case 3:
                    switch (action){
                        case 0:
                            list.start = nullptr;
                            list.end = nullptr;
                            break;
                        case 1:
                            listEnqueue(list);
                            break;
                        case 2:
                            listDequeue(list);
                            break;
                        case 3:
                            (listIsEmpty(list))?(std::cout << "list is empty" << std::endl):(std::cout << "list is not empty" << std::endl);
                            break;
                        case 4:
                            listPrint(list.start);
                            break;
                        default:
                            anotherType=true;
                            break;
                    }
                    break;
                default:
                    isEnd = true;
                    std::cout << "error";
                    break;
            }
            if(!anotherType){
                std::cout << "choose what to do: 0 - create an empty array; 1 - add element to the end; 2 - remove element from the start; 3 - check if it is empty; 4 - print elements" << std::endl;
                std::cin >> action;
            }
            else{ action = 0;}
        }while(!anotherType);
    }while(!isEnd);


    return 0;
}
