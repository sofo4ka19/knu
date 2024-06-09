//
// Created by User on 08.06.2024.
//
#include <iostream>

namespace var_6{
    //1-----------------------------------------------------------------------------------------------------------
    struct Node{
        int value;
        Node* next;
        Node* prev;

        Node(int value, Node* prev = nullptr, Node* next= nullptr): value(value), next(next), prev(prev) {}
    };
    struct LinkedList{
        Node* start;
        Node* end;

        LinkedList(): start(nullptr), end(nullptr) {}

        void removeRows(){
            if (start== nullptr || start->next== nullptr) return;
            Node* current = start->next;
            while (current!= end->next){
                if (current->prev->value==current->value){
                    if (current==end){
                        current->prev->next= nullptr;
                        current=current->prev;
                        delete end;
                        end=current;
                    } else{
                        current->prev->next=current->next;
                        current->next->prev=current->prev;
                        Node* newNode = current->next;
                        delete current;
                        current=newNode;
                    }
                } else{
                    current=current->next;
                }
            }
        }
        //--------------------------------------------------------------------------------------------------
        void addElement(int value){
            Node* newNode= new Node(value);
            if (start== nullptr){
                start=end=newNode;
                return;
            }
            end->next=newNode;
            newNode->prev=end;
            end=end->next;
        }
    };
    void print(Node *&root) {
        Node *current = root;
        while (current != nullptr) {
            std::cout << current->value << " ";
            current = current->next;
        }
        std::cout << std::endl;
    }
    //2--------------------------------------------------------------------------------------------------------
    struct SparceMatrix{
        int value;
        int row;
        int column;
        SparceMatrix* nextRow;
        SparceMatrix* nextColumn;

        SparceMatrix(int value, int row, int column): value(value), row(row), column(column), nextColumn(nullptr), nextRow(
                nullptr) {}
    };
    void countB(SparceMatrix** rows, SparceMatrix** columns, int size){
        int B[size][size];
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                B[i][j]=0;
                SparceMatrix* el1 = rows[i];
                SparceMatrix* el2 = columns[j];
                while (el1!= nullptr && el2!= nullptr){
                    if (el1->column==el2->row){
                        B[i][j]+=el1->value*el2->value;
                        std::cout <<el1->value << "*" << el2->value << "+";
                        el1=el1->nextRow;
                        el2 = el2->nextColumn;
                    }
                    else if(el1->column>el2->row){
                        el2=el2->nextColumn;
                    } else{
                        el1=el1->nextRow;
                    }
                }
                std::cout << "=" << B[i][j] << std::endl;
            }
        }
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                std::cout << B[i][j] << " ";
            }
            std::cout << std::endl;
        }
    }
    //3--------------------------------------------------------------------------------------------------------
    struct TreeNode{
        int value;
        TreeNode* left;
        TreeNode* right;

        TreeNode(int value): value(value), left(nullptr), right(nullptr) {}
    };
    int countBigger(TreeNode*root, const int& num){
        if(root== nullptr) return 0;
        if (root->value<=num){
            return countBigger(root->left, num) + countBigger(root->right, num);
        }else{
            return countBigger(root->left, num) + countBigger(root->right, num)+1;
        }
    }
    //---------------------------------------------------------------------------------------------------------
    int main(){
        LinkedList list;
        for (int i = 0; i < 30; ++i) {
            list.addElement(rand()%3);
        }
        print(list.start);
        list.removeRows();
        print(list.start);

        TreeNode *root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->right = new TreeNode(3);
        root->left->left = new TreeNode(4);
        root->left->right = new TreeNode(5);
        root->right->left = new TreeNode(6);
        root->right->right = new TreeNode(7);
        std::cout << countBigger(root,2) << std::endl;

        SparceMatrix* rows[4];
        SparceMatrix* cols[4];

        int matrix[4][4]={
                {0, 1, 2, 0},
                {0, 0, 0 ,1},
                {2, 0, 1, 0},
                {0, 4, 1,0}
        };

        auto* el1 = new SparceMatrix(1, 0, 1);
        auto* el2 = new SparceMatrix(2, 0, 2);
        rows[0] = el1;
        cols[1]= el1;
        cols[2]= el2;
        el1->nextRow = el2;
        auto* el3 = new SparceMatrix(1,1, 3);
        auto* el4 = new SparceMatrix(2, 2, 0);
        auto* el5 = new SparceMatrix(1, 2, 2);
        rows[1] = el3;
        rows[2]= el4;
        cols[3] = el3;
        cols[0] = el4;
        el2->nextColumn = el5;
        el4->nextRow = el5;
        auto* el6 = new SparceMatrix(4, 3, 1);
        auto* el7 = new SparceMatrix(1, 3, 2);
        rows[3] = el6;
        el1->nextColumn = el6;
        el5->nextColumn = el7;
        el6->nextRow= el7;
        countB(rows, cols, 4);
        return 0;
    }
}