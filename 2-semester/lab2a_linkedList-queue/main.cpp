#include <iostream>
#include <vector>

struct Point{
    float x;
    float y;
    float z;
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
int main() {
    int type, action=0;
    std::vector<Point> array;
    bool isEnd = false;
    Point* static_array = nullptr;
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
