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
        if(el1[i]<el2[i]){
            return false;
        }
        else if(el1[i]>el2[i]){
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
    return el2<=el1;
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
int getIndexOfType(const std::string& type){
    for (int i = 0; i < train_types.size(); ++i) {
        if(type==train_types[i]){
            return i;
        }
    }
};

void countingSort(std::vector<Train>& array, int start, int end, int position=0, int size=train_types.size()){
    int count[size];
    for(int i=0; i<size; i++){
        count[i]=0;
    }
    for (int i = start; i <= end ; i++) {
        (position == 0) ? (count[getIndexOfType(array[i].type)]++) : (count[(array[i].num / position) % 10]++);
    }

    for(int i=1; i<size; i++){
        count[i]+=count[i-1];
    }
    Train temp[end-start+1];
    for (int i = end; i >= start; i--) {
        (position==0)?(temp[--count[getIndexOfType(array[i].type)]]=array[i]):(temp[--count[(array[i].num/position)%10]]=array[i]);
    }
    for(int i=start; i<=end; i++){
        array[i]= temp[i-start];
    }
}
void radixSort(std::vector<Train>& array, int start, int end){
        for (int i = 1; i <= 1000; i*=10) {
            countingSort(array, start, end, i, 10);
        }

}
bool isDateEqual(Date el1, Date el2){
    if(el1.year==el2.year && el1.month==el2.month && el1.day==el2.day && el1.hour==el2.hour && el1.minute==el2.minute) return true;
    return false;
}
void findIntervals(std::vector<Period>& intervals, int field, const std::vector<Train>& array, int start, int end){
    int new_start=start, new_end=start;
    for (int i = start+1; i <= end; i++) {
        switch (field) {
            case 0:
                if(array[i].ID!=array[i-1].ID){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 1:
                if(array[i].num!=array[i-1].num){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 2:
                if(array[i].name!=array[i-1].name){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 3:
                if(array[i].type!=array[i-1].type){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 4:
                if(!isDateEqual(array[i].arrive,array[i-1].arrive)){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 5:
                if(!isDateEqual(array[i].leave,array[i-1].leave)){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            case 6:
                if(array[i].popularity!=array[i-1].popularity){
                    if(new_end-new_start!=0) intervals.push_back({new_start, new_end});
                    new_start=i;
                }
                break;
            default:
                return;
        }
        new_end=i;
    }
    if(new_end-new_start!=0){
        intervals.push_back({new_start, new_end});
    }
}
void sort(const std::vector<int>& fields, std::vector<Train>& array, const int& size){
    std::vector<Period> intervals = {{0, size-1}};
    for(int field : fields){
        size_t intervals_size = intervals.size();
        for (int j = 0; j < intervals_size; ++j) {
            switch (field) {
                case 1:
                    radixSort(array, intervals[j].start, intervals[j].end);
                    findIntervals(intervals, field, array, intervals[j].start, intervals[j].end);
                    break;
                case 3:
                    countingSort(array, intervals[j].start, intervals[j].end);
                    findIntervals(intervals, field, array, intervals[j].start, intervals[j].end);
                    break;
                default:
                    mergeSort(array, intervals[j].start, intervals[j].end, field);
                    findIntervals(intervals, field, array, intervals[j].start, intervals[j].end);
                    break;
            }
        }
        std::cout<<std::endl;
        intervals.erase(intervals.begin(), intervals.begin()+intervals_size);

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
    std::cout << "the result" << std::endl;
    print(array);
}
int main() {
    interactive();
    return 0;
}
