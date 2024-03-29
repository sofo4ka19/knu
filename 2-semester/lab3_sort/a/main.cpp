#include <iostream>
#include <vector>
#include <algorithm>
#include <limits>
#include <random>
#include <chrono>

void print(std::vector<double> array){
    for(int i=0; i<array.size(); i++){
        std::cout << array[i] << " ";
    }
    std::cout << std::endl;
}
void bubbleSort(std::vector<double>& array, int start, int end, bool show){
    for(int i=start+1; i<=end; i++){
        if(array[i]>array[i-1]){
            std::swap(array[i],array[i-1]);
        }
    }
    if(show) print(array);
    if(end!=start+1){
        bubbleSort(array, start, end-1, show);
    }
}
int lomuto(std::vector<double>& array, int low, int high, bool show){
    int j=low;
    int pivot = array[high];
    for (int i = low; i < high; ++i) {
        if (array[i] >= pivot){
            std::swap(array[i], array[j]);
            j++;
        }
    }
    std::swap(array[high], array[j]);
    if(show) print(array);
    return j;
}
void quickSort(std::vector<double>& array, int low, int high, bool show){
    if(low<high){
        int pivotNum = lomuto(array,low, high, show);
        quickSort(array, low, pivotNum-1, show);
        quickSort(array, pivotNum+1, high, show);
    }
}
void merge(std::vector<double>& array, int low, int mid, int high, bool show) {
    int i = 0, j = mid + 1, k = low;
    std::vector<double> temp;
    for (int m = low; m <= mid; m++) {
        temp.push_back(array[m]);
    }
    while (i < temp.size() && j <= high) {
        if (temp[i] >= array[j]) {
            array[k] = temp[i];
            i++;
            k++;
        } else {
            array[k] = array[j];
            j++;
            k++;
        }
    }
    while (i < temp.size()) {
        array[k] = temp[i];
        i++;
        k++;
    }
    if (show) print(array);
}

void mergeSort(std::vector<double>& array, int low, int high, bool show) {
    if (low >= high)
        return;

    int mid = low + (high - low) / 2;
    mergeSort(array, low, mid, show);
    mergeSort(array, mid + 1, high, show);
    merge(array, low, mid, high, show);
}


void combineSort(std::vector<double>& array, int n, int low, int high, bool show){
    int size = high - low + 1;
    if (size <= 1)
        return ;

    else if (size <= n)
    {
        bubbleSort(array,low, high, show);
    }
    else
    {
        int mid = low + (high - low) / 2;
        combineSort(array, n, low, mid, show);
        combineSort(array, n, mid + 1, high, show);
        merge(array, low, mid, high, show);
    }
    if(show) print(array);
}
void create(std::vector<double>& right, std::vector<double>& wrong, std::vector<double>& mix, int size){
    for(int i=0; i<size; i++){
        right.push_back(size-i);
        wrong.push_back(i);
        mix.push_back(rand()/100.0);
    }
    std::swap(right[rand()%size],right[rand()%size]);
    std::swap(wrong[rand()%size],wrong[rand()%size]);
}
void demo(int size){
    std::vector<double> right, wrong, mix, current;
    create(right, wrong, mix, size);
    std::cout << "actions for array in right order:" << std::endl;
    print(right);
    current=right;
    std::cout << "bubble sort:" << std::endl;
    bubbleSort(current, 0, size-1, true);
    current=right;
    std::cout << "quick sort (lomuto):" << std::endl;
    quickSort(current, 0, size-1, true);
    current=right;
    std::cout << "merge sort:" << std::endl;
    mergeSort(current, 0, size-1, true);
    current=right;
    std::cout << "combine sort:" << std::endl;
    combineSort(current, 34, 0,size-1, true);
    std::cout << "library sort:" << std::endl;
    std::sort(right.begin(), right.end(), std::greater<double>());
    print(right);

    std::cout << "actions for array in wrong order:" << std::endl;
    print(wrong);
    current=wrong;
    std::cout << "bubble sort:" << std::endl;
    bubbleSort(current, 0, size-1, true);
    current=wrong;
    std::cout << "quick sort (lomuto):" << std::endl;
    quickSort(current, 0, size-1, true);
    current=wrong;
    std::cout << "merge sort:" << std::endl;
    mergeSort(current, 0, size-1, true);
    current=wrong;
    std::cout << "combine sort:" << std::endl;
    combineSort(current, 34, 0,size-1, true);
    std::cout << "library sort:" << std::endl;
    std::sort(wrong.begin(), wrong.end(), std::greater<double>());
    print(wrong);

    std::cout << "actions for array in mixed order:" << std::endl;
    print(mix);
    current=mix;
    std::cout << "bubble sort:" << std::endl;
    bubbleSort(current, 0, size-1, true);
    current=mix;
    std::cout << "quick sort (lomuto):" << std::endl;
    quickSort(current, 0, size-1, true);
    current=mix;
    std::cout << "merge sort:" << std::endl;
    mergeSort(current, 0, size-1, true);
    current=mix;
    std::cout << "combine sort:" << std::endl;
    combineSort(current, 34, 0,size-1, true);
    std::cout << "library sort:" << std::endl;
    std::sort(mix.begin(), mix.end(), std::greater<double>());
    print(mix);
}
void benchmark() {
    std::random_device rd;
    std::mt19937 mersenne(rd());
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;
    int N = 100;
    std::vector<double> right, wrong, mix, current;
    do {
        create(right, wrong, mix, N);
        std::cout << "for " << N << " elements:" << std::endl;
        current = right;
        auto t0 = high_resolution_clock::now();
        bubbleSort(current, 0, N - 1, false);
        auto t1 = high_resolution_clock::now();
        duration<double, std::milli> ms_double0 = t1 - t0;
        std::cout << "time for array in right order: bubble sort - " << ms_double0.count() << "ms; ";
        current = right;
        t0 = high_resolution_clock::now();
        quickSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "quick sort (lomuto partition scheme) - " << ms_double0.count() << "ms; ";
        current = right;
        t0 = high_resolution_clock::now();
        mergeSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "merge sort - " << ms_double0.count() << "ms; ";
        current = right;
        t0 = high_resolution_clock::now();
        combineSort(current, 34, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "combine sort - " << ms_double0.count() << "ms; ";
        t0 = high_resolution_clock::now();
        std::sort(right.begin(), right.end(), std::greater<double>());
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "library sort - " << ms_double0.count() << "ms" << std::endl;

        current = wrong;
        t0 = high_resolution_clock::now();
        bubbleSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "time for array in wrong order: bubble sort - " << ms_double0.count() << "ms; ";
        current = wrong;
        t0 = high_resolution_clock::now();
        quickSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "quick sort (lomuto partition scheme) - " << ms_double0.count() << "ms; ";
        current = wrong;
        t0 = high_resolution_clock::now();
        mergeSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "merge sort - " << ms_double0.count() << "ms; ";
        current = wrong;
        t0 = high_resolution_clock::now();
        combineSort(current, 34, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "combine sort - " << ms_double0.count() << "ms; ";
        t0 = high_resolution_clock::now();
        std::sort(wrong.begin(), wrong.end(), std::greater<double>());
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "library sort - " << ms_double0.count() << "ms" << std::endl;

        current = mix;
        t0 = high_resolution_clock::now();
        bubbleSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "time for array in mix order: bubble sort - " << ms_double0.count() << "ms; ";
        current = mix;
        t0 = high_resolution_clock::now();
        quickSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "quick sort (lomuto partition scheme) - " << ms_double0.count() << "ms; ";
        current = mix;
        t0 = high_resolution_clock::now();
        mergeSort(current, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "merge sort - " << ms_double0.count() << "ms; ";
        current = mix;
        t0 = high_resolution_clock::now();
        combineSort(current, 34, 0, N - 1, false);
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "combine sort - " << ms_double0.count() << "ms; ";
        t0 = high_resolution_clock::now();
        std::sort(mix.begin(), mix.end(), std::greater<double>());
        t1 = high_resolution_clock::now();
        ms_double0 = t1 - t0;
        std::cout << "library sort - " << ms_double0.count() << "ms" << std::endl;
        N *= 2;
    } while (N < 25600);
}
int main() {
    int choice;
    std::cout << "choose the mode: 1 - demo, 2 - benchmark" << std::endl;
    std::cin >> choice;
    switch (choice) {
        case 1:
            int size;
            std::cout << "enter size of the array" << std::endl;
            std::cin >> size;
            if(std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                break;
            }
            demo(size);
            break;
        case 2:
            benchmark();
            break;
        default:
            break;
    }
    return 0;
}
