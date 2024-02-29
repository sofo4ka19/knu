#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>
#include <chrono>
#include <cstdlib>
#include <random>
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
void readFile(std::vector<Element>& aray, std::string file="data.txt"){
    std::ifstream infile(file);
    std::string line;
    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        Train train;
        char delimiter;

        iss >> train.ID >> delimiter >> train.num >> delimiter >> train.name >> delimiter >> train.type >> delimiter >> train.arrive.hour >> delimiter >> train.arrive.minute >>
            train.arrive.day >> delimiter >> train.arrive.month >> delimiter >>
            train.arrive.year >> delimiter  >> train.leave.hour >> delimiter >> train.leave.minute >>
            train.leave.day >> delimiter >> train.leave.month >> delimiter >>
            train.leave.year >> delimiter >> train.popularity;
            aray.push_back({false, train});
    }
}
void addElement(std::vector<Element>& aray){
    int id;
    if(size(aray)!=0){
        id=aray[size(aray)-1].train.ID+1;
    }
    else{ id=1;}
    Train add = {id};
    std::cout << "add information: code, name, type, time and date of arrive and popularity" << std::endl;
    std::cin >> add.num >> add.name >> add.type >> add.arrive.hour >> add.arrive.minute >> add.arrive.day >> add.arrive.month >> add.arrive.year >> add.leave.hour >> add.leave.minute >> add.leave.day >> add.leave.month >> add.leave.year >> add.popularity;
    aray.push_back({true,add});
}
void saveText(const Train& cur_train, std::string place){
    std::ofstream outfile(place, std::ios::app);
    outfile << std::setw(5) << cur_train.ID << "|";
    outfile << std::setw(5) << cur_train.num << "|";
    outfile << std::setw(20) << cur_train.name << " |";
    outfile << std::setw(15) << cur_train.type << " |";
    outfile << std::setw(20) << cur_train.arrive.hour << ":" << cur_train.arrive.minute << " " << cur_train.arrive.day << "." << cur_train.arrive.month << "." << cur_train.arrive.year << "|";
    outfile << std::setw(20) << cur_train.leave.hour << ":" << cur_train.leave.minute << " " << cur_train.leave.day << "." << cur_train.leave.month << "." << cur_train.leave.year << "|";
    outfile << std::setw(5) << cur_train.popularity << std::endl;
    outfile.close();
}
void saveBinary(const Train& cur_train, std::string place){
    std::ofstream outfile(place, std::ios::ate | std::ios::app | std::ios::binary);
    outfile.write(reinterpret_cast<const char*>(&cur_train), sizeof(Train));
    outfile.close();
}
void save(std::vector<Element>& aray, std::string textFile = "data.txt", std::string binFile = "data.bin"){
    for (auto& element : aray) {
        if (element.change) {
            saveText(element.train, textFile);
            saveBinary(element.train, binFile);
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
    for(int i=0; i<size(aray); i++){
        Train el = aray[i].train;
        std::cout << std::setw(5) << el.num << "|";
        std::cout << std::setw(20) << el.name << "|";
        std::cout << std::setw(15) << el.type << "|";
        std::cout << std::setw(20) << el.arrive.hour << ":" << el.arrive.minute << " " << el.arrive.day << "." << el.arrive.month << "." << el.arrive.year << "|";
        std::cout << std::setw(20) << el.leave.hour << ":" << el.leave.minute << " " << el.leave.day << "." << el.leave.month << "." << el.leave.year << "|";
        std::cout << std::setw(5) << el.popularity << std::endl;
    }
}

void search1(const std::string search, std::vector<Element>& aray){
    std::vector<Element> result;
    for(int i=0; i<size(aray); i++){
        bool isOk = true;
        std::string el = aray[i].train.name;
        for(int k=0; k<search.length(); k++){
            if (search[k]!=el[k]){
                isOk = false;
                break;
            }
        }
        if(isOk) result.push_back(aray[i]);
    }
    printAll(result);
}

void search2(int searchNum, std::vector<Element>& aray){
    std::vector<Element> result;
    for(int i=0; i<size(aray); i++){
        if(aray[i].train.num>=searchNum) result.push_back(aray[i]);
    }
    printAll(result);
}

void search3(float rate, std::vector<Element>& aray){
    std::vector<Element> result;
    for(int i=0; i<size(aray); i++){
        if(aray[i].train.popularity<=rate) result.push_back(aray[i]);
    }
    printAll(result);
}

void search4(Date min, Date max, std::vector<Element>& aray){
    std::vector<Element> result;
    for(int i=0; i<size(aray); i++){
        Date el=aray[i].train.arrive;
        bool isOk=true;
        if(el.year<min.year || el.year>max.year){
            isOk=false;
        }
        else if(el.year==min.year && el.year==max.year){
            if(el.month<min.month || el.month>max.month){
                isOk=false;
            }
            else if(el.month==min.month && el.month==max.month){
                if(el.day<min.day || el.day>max.day){
                    isOk=false;
                }
                else if(el.day==min.day && el.day==max.day){
                    if(el.hour<min.hour || el.hour>max.hour){
                        isOk=false;
                    }
                    else if(el.hour==min.hour && el.hour==max.hour){
                        if(el.minute<min.minute || el.minute>max.minute){
                            isOk=false;
                        }
                    }
                    else if(el.hour == min.hour){
                        if(el.minute<min.minute){
                            isOk=false;
                        }
                    }
                    else if(el.hour == max.hour){
                        if(el.minute>max.minute){
                            isOk=false;
                        }
                    }
                }
                else if (el.day==min.day){
                    if (el.hour<min.hour){
                        isOk=false;
                    }
                    else if(el.hour == min.hour){
                        if(el.minute<min.minute){
                            isOk=false;
                        }
                    }
                }
                else if (el.day==max.day){
                    if (el.hour>max.hour){
                        isOk=false;
                    }
                    else if(el.hour == max.hour){
                        if(el.minute>max.minute){
                            isOk=false;
                        }
                    }
                }
            }
            else if(el.month==min.month){
                if(el.day<min.day){
                    isOk=false;
                }
                else if (el.day==min.day){
                    if (el.hour<min.hour){
                        isOk=false;
                    }
                    else if(el.hour == min.hour){
                        if(el.minute<min.minute){
                            isOk=false;
                        }
                    }
                }
            }
            else if(el.month==max.month){
                if(el.day>max.day){
                    isOk=false;
                }
                else if (el.day==max.day){
                    if (el.hour>max.hour){
                        isOk=false;
                    }
                    else if(el.hour == max.hour){
                        if(el.minute>max.minute){
                            isOk=false;
                        }
                    }
                }
            }
        }
        else if(el.year==min.year){
            if(el.month<min.month){
                isOk=false;
            }
            else if(el.month==min.month){
                if(el.day<min.day){
                    isOk=false;
                }
                else if (el.day==min.day){
                    if (el.hour<min.hour){
                        isOk=false;
                    }
                    else if(el.hour == min.hour){
                        if(el.minute<min.minute){
                            isOk=false;
                        }
                    }
                }
            }
        }
        else if(el.year==max.year){
            if(el.month>max.month){
                isOk=false;
            }
            else if(el.month==max.month){
                if(el.day>max.day){
                    isOk=false;
                }
                else if (el.day==max.day){
                    if (el.hour>max.hour){
                        isOk=false;
                    }
                    else if(el.hour == max.hour){
                        if(el.minute>max.minute){
                            isOk=false;
                        }
                    }
                }
            }
        }
        if(isOk) result.push_back(aray[i]);
    }
    printAll(result);
}
void interactive(std::vector<Element>& array){
    int choose;
    bool isEnd=false;
    while(!isEnd) {
        std::cout << "Choose the command: 1 - adding element; 2 - save element; 3 - print whole information; 4 - searching the element" << std::endl;
        std::cin >> choose;
        std::string search;
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
            case 4:
                std::cout << "what criteria you want to choose: 1 - name of the train; 2 - min number of train; 3 - max rate of popularity; 4 - period of time" << std::endl;
                int choose2;
                std::cin >> choose2;
                switch (choose2) {
                    case 1:
                        std::cout << "enter first symbols of the name of the train" << std::endl;
                        std::cin >> search;
                        search1(search, array);
                        break;
                    case 2:
                        int num;
                        std::cout << "enter min number of train" << std::endl;
                        std::cin >> num;
                        search2(num, array);
                        break;
                    case 3:
                        float rate;
                        std::cout << "enter max rate of the popularity" << std::endl;
                        std::cin >> rate;
                        search3(rate, array);
                        break;
                    case 4:
                        Date min, max;
                        std::cout << "enter min time and date of arrival" << std::endl;
                        std::cin >> min.hour >> min.minute >> min.day >> min.month >> min.year;
                        std::cout << "enter max time and date of arrival" << std::endl;
                        std::cin >> max.hour >> max.minute >> max.day >> max.month >> max.year;
                        search4(min, max, array);
                        break;
                    default:
                        std::cout << "Error, try again" << std::endl;
                        break;
                }
                break;
            default:
                isEnd = true;
        }
    }
}
void demo(std::vector<Element>& aray){
    std::cout << "0. All data were restored, print it in console" << std::endl;
    printAll(aray);
    std::cout << "1. Add an element to the vector (2552, Dnipro-Kyiv, ordinary, 20:55 29.02.2024, 21:15 29.02.2024, 1.1)" << std::endl;
    int id;
    if(size(aray)!=0){
        id=aray[size(aray)-1].train.ID+1;
    }
    else{ id=1;}
    aray.push_back({true, {id, 2552, "Dnipro-Kyiv", "ordinary", {29,02,2024, 20,55}, {29,02,2024,21,15}, 1.1}});
    std::cout << "2. Save it to binary and text files" << std::endl;
    save(aray);
    std::cout << "Now you can check that our information were saved in the files" << std::endl;
    std::cout << "3. Printing all data" << std::endl;
    printAll(aray);
    std::cout << "4. Searching by name (Kyiv)" << std::endl;
    search1("Kyiv", aray);
    std::cout << "5. Searching by min number (2500)" << std::endl;
    search2(2500, aray);
    std::cout << "6. Searching by max rate of popularity (1.2)" << std::endl;
    search3(1.2, aray);
    std::cout << "7. Searching by period of time (20:00 25.02.2024 - 10:10 05.03.2024)" << std::endl;
    search4({25,02,2024,20,00}, {05,03,2024,10,10}, aray);
    std::cout << "That's all" << std::endl;
}
void benchmark(){
    std::vector<Element> array;
    std::random_device rd;
    std::mt19937 mersenne(rd());
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;
    int id=1;
    int N=10;
    bool isEnd;
    duration<double, std::milli> ms_double;
    do{
        auto t0 = high_resolution_clock::now();
        readFile(array, "benchmark.txt");
        auto t1 = high_resolution_clock::now();
        for(int i=0; i<N; i++){
            array.push_back({true, {id, rand()%10000, std::to_string(mersenne()%100000000000000000), std::to_string(mersenne()%10000000), {rand()%31+1, rand()%12+1, rand()%2030+1, rand()%24, rand()%60}, {rand()%31+1, rand()%12+1, rand()%2030+1, rand()%24, rand()%60}, 0.1*(rand()%20)}});
            id++;
        }
        auto t2 = high_resolution_clock::now();
        save(array, "benchmark.txt", "benchmark.bin");
        auto t3 = high_resolution_clock::now();
        search1(std::to_string(rand()/1000), array);
        auto t4 = high_resolution_clock::now();
        search2(rand()%10000, array);
        auto t5 = high_resolution_clock::now();
        search3(0.1*(rand()%20), array);
        auto t6 = high_resolution_clock::now();
        search4({rand()%31+1, rand()%12+1, rand()%2030+1, rand()%24, rand()%60}, {rand()%31+1, rand()%12+1, rand()%2030+1, rand()%24, rand()%60},array);
        auto t7 = high_resolution_clock::now();
        duration<double, std::milli> ms_double1 = t1 - t0;
        duration<double, std::milli> ms_double2 = t2 - t1;
        duration<double, std::milli> ms_double3 = t3 - t2;
        duration<double, std::milli> ms_double4 = t4 - t3;
        duration<double, std::milli> ms_double5 = t5 - t4;
        duration<double, std::milli> ms_double6 = t6 - t5;
        duration<double, std::milli> ms_double7 = t7 - t6;
        duration<double, std::milli> ms_double = t7 - t0;
        std::cout << "for " << N << " elements: restoring previous - " << ms_double1.count() << "ms; adding - " << ms_double2.count() << "ms; saving - "<< ms_double3.count() << "ms; searching by name - " << ms_double4.count() << "ms; searching by min num - "<< ms_double5.count() << "ms; searching by max rate - "<< ms_double6.count() << "ms; searching by period of time for arrival - " << ms_double7.count() << "ms; at all - " << ms_double.count() << std::endl;
        isEnd = ms_double.count()<10000.0;
        if(ms_double.count()<1000){
            N*=2;
        }
        else{
            const int N1=N;
            N+=N1;
        }
    }while(isEnd);
}
int main() {
    int choose;
    std::vector<Element> array;
    readFile(array);
    std::cout << "Choose the mode: 1 - interactive (you manage all processes), 2 - demonstration, 3 - benchmark" << std::endl;
    std::cin >> choose;
    switch (choose) {
        case 1:
            interactive(array);
            break;
        case 2:
            demo(array);
            break;
        case 3:
            benchmark();
            break;
        default:
            std::cout << "Error";
            break;
    }

    return 0;
}
