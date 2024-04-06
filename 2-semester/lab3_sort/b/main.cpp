#include <iostream>
#include <vector>
#include <iomanip>
#include <cstring>

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
std::vector<std::string> train_types = {"international", "speed", "ordinary", "commuter"};
void print(const std::vector<Train>& aray){
    std::cout << std::setw(4) << "ID" << "|";
    std::cout << std::setw(6) << "Number" << "|";
    std::cout << std::setw(20) << "Name of the train"<< "|";
    std::cout << std::setw(15) << "Train type"<< "|";
    std::cout << std::setw(20) << "Arrival time"<< "|";
    std::cout << std::setw(20) << "Leave time"<< "|";
    std::cout << std::setw(5) << "Rate" << std::endl;
    for( const Train& el:aray){
        std::cout << std::setw(4) << el.ID << "|";
        std::cout << std::setw(6) << el.num << "|";
        std::cout << std::setw(20) << el.name << "|";
        std::cout << std::setw(15) << el.type << "|";
        std::cout << std::setw(6) << el.arrive.hour << ":" << std::setw(2) << el.arrive.minute << " " << std::setw(2) << el.arrive.day << "." << std::setw(2) << el.arrive.month << "." << std::setw(4) << el.arrive.year << "|";
        std::cout << std::setw(6) << el.leave.hour << ":" << std::setw(2) << el.leave.minute << " " << std::setw(2) << el.leave.day << "." << std::setw(2) << el.leave.month << "." << std::setw(4) << el.leave.year << "|";
        std::cout << std::setw(5) << el.popularity << std::endl;
    }
}
void addElement(std::vector<Train>& aray, int id){
    Train add = {id};
    std::cout << "add information: code, name, type, time and date of arrive and popularity" << std::endl;
    std::cin >> add.num >> add.name >> add.type >> add.arrive.hour >> add.arrive.minute >> add.arrive.day >> add.arrive.month >> add.arrive.year >> add.leave.hour >> add.leave.minute >> add.leave.day >> add.leave.month >> add.leave.year >> add.popularity;
    aray.push_back(add);
}
void randomFillArray(std::vector<Train>& array, int size){
    std::vector<std::string> cities = {"Kyiv", "Lviv", "Dnipro", "Kharkiv", "Kryvyi Rih", "Odesa", "Ternopil", "Uzhorod", "Poznan", "Warsav" };
    for (int i = 0; i < size; ++i) {
        array.push_back({i+1, rand()%9000+1000, cities[rand()%10]+"-"+cities[rand()%10],train_types[rand()%4], {rand()%31+1, rand()%12+1, 2024, rand()%24, rand()%60}, {rand()%31+1, rand()%12+1, 2024, rand()%24, rand()%60}, (rand()%20)/10.0 });
    }
}
bool compare(std::string el1, std::string el2){
    for(int i=0; i<std::min(el1.size(), el2.size()); i++){
        if(el1[0]<el2[0]){
            return false;
        }
        else if(el1[0]>el2[0]){
            return true;
        }
    }
    return false;
}
bool compare(Date el1, Date el2){
    if(el1.year > el2.year) return true;
    if(el1.month > el2.month) return true;
    if(el1.day > el2.day) return true;
    if(el1.hour > el2.hour) return true;
    if(el1.minute > el2.minute) return true;
    return false;
}
bool compare(double el1, double el2){
    if(el2>el1){
        return true;
    }
    else{
        return false;
    }
}
void merge(std::vector<Train>& array, int low, int mid, int high, int field) {
    int i = 0, j = mid + 1, k = low;
    std::vector<Train> temp;
    for (int m = low; m <= mid; m++) {
        temp.push_back(array[m]);
    }
    while (i < temp.size() && j <= high) {
        switch (field) {
            case 0:
                if (compare(array[j].ID, temp[i].ID)) {
                    array[k] = temp[i];
                    i++;
                    k++;
                } else {
                    array[k] = array[j];
                    j++;
                    k++;
                }
                break;
            case 2:
                if (compare(array[j].name, temp[i].name)) {
                    array[k] = temp[i];
                    i++;
                    k++;
                } else {
                    array[k] = array[j];
                    j++;
                    k++;
                }
                break;
            case 4:
                if (compare(array[j].arrive, temp[i].arrive)) {
                    array[k] = temp[i];
                    i++;
                    k++;
                } else {
                    array[k] = array[j];
                    j++;
                    k++;
                }
                break;
            case 5:
                if (compare(array[j].leave, temp[i].leave)) {
                    array[k] = temp[i];
                    i++;
                    k++;
                } else {
                    array[k] = array[j];
                    j++;
                    k++;
                }
                break;
            case 6:
                if (compare(array[j].popularity, temp[i].popularity)) {
                    array[k] = temp[i];
                    i++;
                    k++;
                } else {
                    array[k] = array[j];
                    j++;
                    k++;
                }
                break;
            default:
                return;
        }
    }
    while (i < temp.size()) {
        array[k] = temp[i];
        i++;
        k++;
    }
}

void mergeSort(std::vector<Train>& array, int low, int high, int field) {
    if (low >= high)
        return;

    int mid = low + (high - low) / 2;
    mergeSort(array, low, mid, field);
    mergeSort(array, mid + 1, high, field);
    merge(array, low, mid, high, field);
}
void countingSort(){
    //this method can sort only int type
}
void interactive(){
    int choose, size;
    std::vector<Train> array;
    std::cout << "enter number of elements in array" << std::endl;
    std::cin >> size;
    std::cout << "Do you want to fill database manually (1) or random (2) ?" << std::endl;
    std::cin >> choose;
    if(std::cin.fail()){
        return ;
    }
    switch (choose) {
        case 1:
            for(int i=0; i<size; i++){
                addElement(array, i+1);
            }
            break;
        case 2:
            randomFillArray(array, size);
            break;
        default:
            return;
    }
    print(array);
}
int main() {
    interactive();
    return 0;
}
