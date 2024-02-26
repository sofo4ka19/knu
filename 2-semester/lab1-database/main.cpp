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
void readFile(std::vector<Element>& aray){
    std::ifstream infile("data.txt");
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        Train train;
        char delimiter;

        iss >> train.ID >> delimiter >> train.num >> delimiter >> train.name >> train.type >> train.arrive.hour >> delimiter >> train.arrive.minute >> delimiter >>
            train.arrive.day >> delimiter >> train.arrive.month >> delimiter >>
            train.arrive.year  >> train.leave.hour >> delimiter >> train.leave.minute >> delimiter >>
            train.leave.day >> delimiter >> train.leave.month >> delimiter >>
            train.leave.year >> delimiter >> train.popularity;
            aray.push_back({false, train});
    }
}
void addElement(std::vector<Element>& aray){
    int id=1;
    if(size(aray)!=0){
        id=aray[size(aray)-1].train.ID+1;
    }
    Train add = {id};
    std::cout << "add information: code, name, type, time and date of arrive and popularity" << std::endl;
    std::cin >> add.num >> add.name >> add.type >> add.arrive.hour >> add.arrive.minute >> add.arrive.day >> add.arrive.month >> add.arrive.year >> add.leave.hour >> add.leave.minute >> add.leave.day >> add.leave.month >> add.leave.year >> add.popularity;
    aray.push_back({true,add});
    id++;
}
void saveText(const Train& cur_train){
    std::ofstream outfile("data.txt", std::ios::app);
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
    std::ofstream outfile("data.bin", std::ios::ate | std::ios::app | std::ios::binary);
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
void printAll(std::vector<Element>& aray){
    std::cout << std::setw(5) << "Number" << "|";
    std::cout << std::setw(20) << "Name of the train"<< "|";
    std::cout << std::setw(15) << "Train type"<< "|";
    std::cout << std::setw(20) << "Arrival time"<< "|";
    std::cout << std::setw(20) << "Leave time"<< "|";
    std::cout << std::setw(5) << "Rate" << std::endl;
    for(int i=0; i<size(aray)-1; i++){
        Train el = aray[i].train;
        std::cout << std::setw(5) << el.num << "|";
        std::cout << std::setw(20) << el.name << "|";
        std::cout << std::setw(15) << el.type << "|";
        std::cout << std::setw(20) << el.arrive.hour << ":" << el.arrive.minute << " " << el.arrive.day << "." << el.arrive.month << "." << el.arrive.year << "|";
        std::cout << std::setw(20) << el.leave.hour << ":" << el.leave.minute << " " << el.leave.day << "." << el.leave.month << "." << el.leave.year << "|";
        std::cout << std::setw(5) << el.popularity << std::endl;
    }
}
int main() {
    int choose;
    std::vector<Element> array;
    readFile(array);
    bool isEnd=false;
    while(!isEnd) {
        std::cout << "Choose the command: 1 - adding element; 2 - save element; 3 - print whole information" << std::endl;
        std::cin >> choose;
        switch (choose) {
            case 1:
                addElement(array);
                break;
            case 2:
                save(array);
                break;
            case 3:
                printAll(array);
                break;
            default:
                isEnd = true;
        }
    }
    return 0;
}
