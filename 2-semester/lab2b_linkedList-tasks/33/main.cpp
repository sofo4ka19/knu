#include <iostream>
#include <vector>

struct Task{
    std::string name;
    double arriveTime;
    double processTime;
};

int main() {
    std::vector<Task> planner;
    std::cout << "add elements to your planner" << std::endl;
    do{
        Task add;
        std::cout << "add name of the task" << std::endl;
        std::cin >> add.name;
        std::cout << "add arrive time" << std::endl;
        std::cin >> add.arriveTime;
        std::cout << "add how many time it needs" << std::endl;
        std::cin >> add.processTime;
        planner.push_back(add);
    }while(!std::cin.fail());
    return 0;
}
