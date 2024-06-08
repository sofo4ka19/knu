//
// Created by User on 08.06.2024.
//
#include <iostream>

namespace var_10{
    //1----------------------------------------------------------------------------------------------------------
    struct Node{
        int koef;
        int pow;
        Node* next;

        Node(int koef, int pow): koef(koef), pow(pow), next(nullptr) {}
    };
    struct LinkedList{
        Node* start;
        Node* end;

        LinkedList(): start(nullptr), end(nullptr) {}
        //вважаємо що вже відсортовано
        void addElement(int koef, int pow){
            Node* node = new Node(koef, pow);
            if(start== nullptr){
                start=end=node;
                return;
            }
            end->next=node;
            end=node;
        }
        LinkedList findPohidna(){
            LinkedList pohidna;
            Node* current = start;
            while(current!= nullptr){
                if (current->pow!=0){
                    pohidna.addElement(current->koef * current->pow, current->pow - 1);
                }
                current=current->next;
            }
            return pohidna;
        }
        int powerty(int num, int pow){
            int result=1;
            for (int i = 0; i < pow; ++i) {
                result*=num;
            }
            return result;
        }
        int count(int x){
            if (start== nullptr) return 0;
            Node* current = start;
            int sum=0;
            while (current!= nullptr){
                sum+=current->koef * powerty(x,current->pow);
                current=current->next;
            }
            return sum;
        }
    };
    //---------------------------------------------------------------------------------------------------------
    void print(Node *&root) {
        Node *current = root;
        while (current != nullptr) {
            std::cout << current->koef << "x^" << current->pow << "+";
            current = current->next;
        }
        std::cout << std::endl;
    }
    //2--------------------------------------------------------------------------------------------------------
    void sort(int* array, const int size){
        bool rigthPos[size];
        for (int i = 0; i < size; ++i) {
            rigthPos[i]= false;
        }
        int i=0;
        while (i<size){
            if(!rigthPos[i]){
                int k=0;
                for (int j = 0; j < size; ++j) {
                    if (array[i]>array[j]) k++;
                }
                while (rigthPos[k]){
                    k++;
                }
                int temp = array[i];
                array[i]=array[k];
                array[k]=temp;
                rigthPos[k]=true;
            } else{
                i++;
            }
        }
    }
    //---------------------------------------------------------------------------------------------------------
    void print(int* array, int size){
        for (int i = 0; i < size; ++i) {
            std::cout << array[i] << " ";
        }
        std::cout << std::endl;
    }
    int main(){
        LinkedList list;
        for (int i = 0; i < 10; ++i) {
            list.addElement(rand()%10+1,i);
        }
        print(list.start);
        Node* start = list.findPohidna().start;
        print(start);
        std::cout<<list.findPohidna().count(2)<<std::endl;

        int array[35];
        for (int i = 0; i < 35; ++i) {
            array[i] = rand()%100;
            std::cout << array[i] << " ";
        }
        std::cout<< std::endl;
        sort(array,35);
        print(array, 35);
        return 0;
    }
}