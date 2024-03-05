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
void staticEnqueue(Point *array, int size, int& index, Point add = enqueue()){
    if(index==size){
        std::cout << "Error. Your array is full" << std::endl;
    }
    else{
        array[index]=add;
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
void interactive(std::vector<Point>& array, Point*& static_array, LinkedList& list){
    int type, action=0;
    bool isEnd = false;
    while(!isEnd){
        std::cout << "choose type of the list: 1 - static array; 2 - vector (dynamic array); 3 - linked list" << std::endl;
        std::cin >> type;
        bool anotherType = false;
        while(!anotherType && !isEnd) {
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
                    std::cout << "error" << std::endl;
                    break;
            }
            if(!anotherType && !isEnd){
                std::cout << "choose what to do: 0 - create an empty array; 1 - add element to the end; 2 - remove element from the start; 3 - check if it is empty; 4 - print elements" << std::endl;
                std::cin >> action;
            }
            else{ action = 0;}
        }
    }

}
void demo(std::vector<Point>& array, Point*& static_array, LinkedList& list){
    std::cout << "firstly, let's work with static array which contains 3 elements" << std::endl;
    int index=0;
    static_array = new Point[3];
    std::cout << "check if it's empty" << std::endl;
    (staticIsEmpty(index))?(std::cout << "array is empty" << std::endl):(std::cout << "array is not empty" << std::endl);
    std::cout << "add element (0;0;0) in the end of the array" << std::endl;
    staticEnqueue(static_array, 3, index, {0,0,0});
    std::cout << "add element (-2;0;5) in the end of the array" << std::endl;
    staticEnqueue(static_array, 3, index, {-2,0,5});
    std::cout << "add element (0;10;2.5) in the end of the array" << std::endl;
    staticEnqueue(static_array, 3, index, {0,10,2.5});
    std::cout << "try to add element (0;3;0) in the end of the array" << std::endl;
    staticEnqueue(static_array, 3, index, {0,3,0});
    std::cout << "print what we have" << std::endl;
    staticPrint(static_array, index);
    std::cout << "delete the first element" << std::endl;
    staticDequeue(static_array, index);
    std::cout << "print what we have" << std::endl;
    staticPrint(static_array, index);

    std::cout << "now let's work with vector array" << std::endl;
    array = {};
    std::cout << "check if it's empty" << std::endl;
    (is_empty(array))?(std::cout << "array is empty" << std::endl):(std::cout << "array is not empty" << std::endl);
    std::cout << "add element (0;1;0) in the end of the array" << std::endl;
    array.push_back({0,1,0});
    std::cout << "add element (-2;1;5) in the end of the array" << std::endl;
    array.push_back({-2,1,5});
    std::cout << "add element (0;0;2.5) in the end of the array" << std::endl;
    array.push_back({0,0,2.5});
    std::cout << "print what we have" << std::endl;
    print(array);
    std::cout << "delete the first element" << std::endl;
    dequeue(array);
    std::cout << "print what we have" << std::endl;
    print(array);

    std::cout << "now let's work with linked list" << std::endl;
    list.start = nullptr;
    list.end = nullptr;
    std::cout << "check if it's empty" << std::endl;
    (listIsEmpty(list))?(std::cout << "list is empty" << std::endl):(std::cout << "list is not empty" << std::endl);
    std::cout << "add element (0;3;2) in the end of the array" << std::endl;
    listEnqueue(list, {0,3,2});
    std::cout << "add element (-2;3;5) in the end of the array" << std::endl;
    listEnqueue(list, {-2,3,5});
    std::cout << "add element (0;-1;0.5) in the end of the array" << std::endl;
    listEnqueue(list, {0,-1,0.5});
    std::cout << "add element (0;0;2) in the end of the array" << std::endl;
    listEnqueue(list, {0,0,2});
    std::cout << "print what we have" << std::endl;
    listPrint(list.start);
    std::cout << "delete the first element" << std::endl;
    listDequeue(list);
    std::cout << "print what we have" << std::endl;
    listPrint(list.start);

    std::cout << "that's all" << std::endl;
}
int main() {
    std::vector<Point> array;
    Point* static_array = nullptr;
    LinkedList list;
    int mode;
    std::cout << "Choose the mode: 1 - interactive; 2 - demonstration; 3 - benchmark" << std::endl;
    std::cin >> mode;
    switch (mode) {
        case 1:
            interactive(array, static_array, list);
            break;
        case 2:
            demo(array, static_array, list);
            break;
        case 3:
            break;
        default:
            break;
    }

    return 0;
}
