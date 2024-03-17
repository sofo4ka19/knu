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
int main() {
    std::vector<double> array;
    for(int i=0; i<25; i++){
        array.push_back(rand()/100.0);
    }
    print(array);
    print(bubbleSort(array, 25));
    return 0;
}
