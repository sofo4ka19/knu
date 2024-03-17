#include <iostream>
#include <vector>
void print(std::vector<double> array){
    for(int i=0; i<array.size(); i++){
        std::cout << array[i] << " ";
    }
    std::cout << std::endl;
}
std::vector<double> bubbleSort(std::vector<double>& array, int N){
    for(int i=1; i<N; i++){
        if(array[i]>array[i-1]){
            std::swap(array[i],array[i-1]);
        }
    }
    if(N!=1){
        bubbleSort(array, N-1);
    }
    return array;
}
std::vector<double> lomuto(std::vector<double>& array, int low, int high){
    int j=low;
    int pivot = array[high];
    for (int i = low; i < high; ++i) {
        if (array[i] >= pivot){
            std::swap(array[i], array[j]);
            j++;
        }
    }
    std::swap(array[high], array[j]);
    if (low<j-1) lomuto(array, low, j-1);
    if(j+1<high) lomuto(array, j+1, high);

    return array;
}
std::vector<double> mergeSort(std::vector<double>& array, int low, int high){
    int mid = low + (high - low)/2;

    if(mid-low>=1) mergeSort(array, low, mid);
    if(high - (mid+1) >= 1) mergeSort(array, mid+1, high);

    int i=0, j=mid+1, k=low;
    std::vector<double> temp;
    for(int m=low; m<=mid+1; m++){
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
    return array;
}

int main() {
    std::vector<double> array;
    for(int i=0; i<25; i++){
        array.push_back(rand()/100.0);
    }
    print(array);
    print(bubbleSort(array, 25));
    print(lomuto(array, 0, 24));
    return 0;
}
