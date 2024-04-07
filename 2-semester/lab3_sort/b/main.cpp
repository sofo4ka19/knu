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
struct Period{
    int start;
    int end;
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
    std::cout << "add information: code, name, time and date (hour, minute, day, month, year) of arrive and left and popularity" << std::endl;
    std::cin >> add.num >> add.name >> add.arrive.hour >> add.arrive.minute >> add.arrive.day >> add.arrive.month >> add.arrive.year >> add.leave.hour >> add.leave.minute >> add.leave.day >> add.leave.month >> add.leave.year >> add.popularity;
    if (std::cin.fail()) return;
    std::cout << "choose type of the train: 0 - international, 1 - speed, 2 - ordinary, 3 - commuter" << std::endl;
    int i;
    std::cin >> i;
    if (std::cin.fail()) return;
    add.type=train_types[i];
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
    if (el1.year != el2.year) {
        return el1.year > el2.year;
    } else if (el1.month != el2.month) {
        return el1.month > el2.month;
    } else if (el1.day != el2.day) {
        return el1.day > el2.day;
    } else if (el1.hour != el2.hour) {
        return el1.hour > el2.hour;
    } else {
        return el1.minute > el2.minute;
    }
}
bool compare(double el1, double el2){
    if(el2>el1){
        return false;
    }
    else{
        return true;
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
int getIndexOfType(std::string type){
    for (int i = 0; i < train_types.size(); ++i) {
        if(type==train_types[i]){
            return i;
        }
    }
};
void countingSort(std::vector<Train>& array, int start, int end){
    //counting sort can sort only integer, but we have a number of types, so let's sort it as in order in array
    //because of that we can't merge it with next count sort for merge sort
    int count[train_types.size()];
    Train temp[end-start+1];
    for (int i = start; i <= end; ++i) {
        count[getIndexOfType(array[i].type)]++;
    }
    for (int i = 1; i < train_types.size(); ++i) {
        count[i]+=count[i-1];
    }
    for (int i = end; i >= start; --i) {
        temp[--count[getIndexOfType(array[i].type)]]=array[i];
    }
    for(int i=start; i<=end; i++){
        array[i]= temp[i];
    }
}
void countSort(std::vector<Train>& array, int start, int end, int position){
    int count[10];
    for(int i=start; i<=end; i++){
        count[(array[i].num/position)%10]++;
    }
    for (int i = 1; i < 10; ++i) {
        count[i]+=count[i-1];
    }
    Train temp[end-start+1];
    for (int i = end; i <= start; --i) {
        temp[--count[(array[i].num/position)%10]]=array[i];
    }
    for(int i=start; i<=end; i++){
        array[i]= temp[i];
    }
}
void radixSort(std::vector<Train>& array, int start, int end){
        for (int i = 1; i <= 1000; i*=10) {
            countSort(array, start, end, i);
        }

}
void sort(std::vector<int> fields, std::vector<Train>& array, const int& size){
    std::vector<Period> intervals = {{0, size-1}};
    switch (fields[0]) {
        case 1:
            radixSort(array, 0, size-1);
            break;
        case 3:
            countingSort(array, 0, size-1);
            break;
        default:
            mergeSort(array, 0, size-1, fields[0]);
            break;
    }
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
    std::cout << "original database" << std::endl;
    print(array);
    std::cout << "How many fields you want use to sort (7 can be the most)?" << std::endl;
    std::cin >> choose;
    if(std::cin.fail() || choose>7 || choose<1){
        return ;
    }
    std::vector<int> fields;
    std::cout << "enter numbers from the list according to the field in order of sorting\n"
                 "0. ID\n"
                 "1. Number of the train\n"
                 "2. Name of the train\n"
                 "3. Type of the train\n"
                 "4. Time and date of arrival\n"
                 "5. Time and date of leaving\n"
                 "6. Popularity\n";
    for (int i = 0; i < choose; ++i) {
        int cur;
        std::cin >> cur;
        if (std::cin.fail() || cur>6 || cur<0){
            std::cout << "error";
            return;
        }
        fields.push_back(cur);
    }
    sort(fields, array, size);
    print(array);
}
int main() {
    interactive();
    return 0;
}
