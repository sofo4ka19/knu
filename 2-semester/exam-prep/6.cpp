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
    struct Sparce{
        int value;
        int row;
        int column;
        Sparce* nextRow;
        Sparce* nextColumn;

        Sparce(int value, int row, int column): value(value), row(row), column(column), nextColumn(nullptr), nextRow(
                nullptr) {}
    };
    //?
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
        std::cout << countBigger(root,2);
        return 0;
    }
}