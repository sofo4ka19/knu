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
void enqueue(std::vector<Point>& array){
    Point add;
    std::cout << "enter x coordinate" << std::endl;
    std::cin >> add.x;
    std::cout << "enter y coordinate" << std::endl;
    std::cin >> add.y;
    std::cout << "enter z coordinate" << std::endl;
    std::cin >> add.z;
    array.push_back(add);
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
int main() {
    std::vector<Point> array = {};
    bool isEnd = false;
    do{
        int choose;
        std::cout << "choose what to do: 1 - add element to the end; 2 - remove element from the start; 3 - check if it is empty; 4 - print elements" << std::endl;
        std::cin >> choose;
        std::string isEmpty;
        switch (choose) {
            case 1:
                enqueue(array);
                break;
            case 2:
                dequeue(array);
                break;
            case 3:
                if(is_empty(array)){
                    isEmpty = "empty";
                }
                else{ isEmpty = "not empty";}
                std::cout << isEmpty << std::endl;
                break;
            case 4:
                print(array);
                break;
            default:
                isEnd=true;
                break;
        }
    }while(!isEnd);
    return 0;
}
