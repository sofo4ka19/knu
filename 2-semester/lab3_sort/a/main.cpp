#include <iostream>
#include <vector>
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
        //if(show) print(array);
        int pivotNum = lomuto(array,low, high, show);
        quickSort(array, low, pivotNum-1, show);
        quickSort(array, pivotNum+1, high, show);
    }
}
/*void mergeSort(std::vector<double>& array, int low, int high, bool show){
    int mid = low + (high - low)/2;
    if(mid-low>=1) mergeSort(array, low, mid, show);
    if(high - (mid+1) >= 1) mergeSort(array, mid+1, high, show);

    int i=0, j=mid+1, k=low;
    std::vector<double> temp;
    for(int m=low; m<=mid; m++){
        temp.push_back(array[m]);
    }
    while(i < temp.size() && j<=high){
        if(temp[i] >= array[j]){
            array[k] = temp[i];
            i++;
            k++;
        }
        else{
            array[k] = array[j];
            j++;
            k++;
        }
    }
    while (i<temp.size()){
        array[k] = temp[i];
        i++;
        k++;
    }
    if(show) print(array);
}*/
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
        std::cout << low << " " << high << std::endl;
        print(array);
        std::cout << "we have sorted elements from " << array[low] << " to " << array[high] << std::endl;
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
        mix.push_back(rand()/100);
    }
    std::swap(right[rand()%size],right[rand()%size]);
    std::swap(wrong[rand()%size],wrong[rand()%size]);
}
void demo(int size){
    std::vector<double> right, wrong, mix;
    create(right, wrong, mix, 25);
    std::cout << "actions for array in right order" << std::endl;
    print(mix);
    bubbleSort(mix, 0, 24, true);
    //quickSort(mix, 0, size-1, true);
    //(mergeSort(mix, 0, size-1, true));
    //(combineSort(mix, 10, 0,24, true));

    /*print(array);
    print(bubbleSort(array, 25));
    print(quickSort(array, 0, 24));
    print(mergeSort(array, 0, 24));
    print(combineSort(array, 10, 0,24));

    print(array);
    print(bubbleSort(array, 25));
    print(quickSort(array, 0, 24));
    print(mergeSort(array, 0, 24));
    print(combineSort(array, 10, 0,24));*/
}
int main() {
    demo(25);
    return 0;
}
