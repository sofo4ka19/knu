#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>

struct Date{
    int day;
    int month;
    int year;
    int hour;
    int minute;
};
struct Train{
    int ID;
    int num;
    std::string name;
    std::string type;
    Date arrive;
    Date leave;
    double popularity;
};
struct Element{
    bool change;
    Train train;
};
void addElement(std::vector<Element>& aray){
    static int id=1;
    Train add = {id};
    std::cout << "add information: code, name, type, time and date of arrive and popularity" << std::endl;
    std::cin >> add.num >> add.name >> add.type >> add.arrive.hour >> add.arrive.minute >> add.arrive.day >> add.arrive.month >> add.arrive.year >> add.leave.hour >> add.leave.minute >> add.leave.day >> add.leave.month >> add.leave.year >> add.popularity;
    aray.push_back({true,add});
    id++;
}
void saveText(const Train& cur_train){
    std::ofstream outfile("data.txt");
    outfile << std::setw(5) << cur_train.ID << "|";
    outfile << std::setw(5) << cur_train.num << "|";
    outfile << std::setw(20) << cur_train.name << "|";
    outfile << std::setw(15) << cur_train.type << "|";
    outfile << std::setw(20) << cur_train.arrive.hour << ":" << cur_train.arrive.minute << " " << cur_train.arrive.day << "." << cur_train.arrive.month << "." << cur_train.arrive.year << "|";
    outfile << std::setw(20) << cur_train.leave.hour << ":" << cur_train.leave.minute << " " << cur_train.leave.day << "." << cur_train.leave.month << "." << cur_train.leave.year << "|";
    outfile << std::setw(5) << cur_train.popularity << std::endl;
    outfile.close();
}
void saveBinary(const Train& cur_train){
    std::ofstream outfile("data.bin", std::ios::binary);
    outfile.write(reinterpret_cast<const char*>(&cur_train), sizeof(Train));
    outfile.close();
}
void save(std::vector<Element>& aray){
    for (auto& element : aray) {
        if (element.change) {
            saveText(element.train);
            saveBinary(element.train);
            element.change=false;
        }
    }
}
int main() {
    int choose;
    std::vector<Element> array;
    bool isEnd=false;
    while(!isEnd) {
        std::cout << "Choose the command: 1 - adding element; 2 - save element" << std::endl;
        std::cin >> choose;
        switch (choose) {
            case 1:
                addElement(array);
                break;
            case 2:
                save(array);
                break;
            default:
                isEnd = true;
        }
    }
    return 0;
}
