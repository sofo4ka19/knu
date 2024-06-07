//
// Created by User on 07.06.2024.
//
#include <iostream>

namespace var_52{
    //1--------------------------------------------------------------------------------------------------------
    struct Node{
        int value;
        Node* prev;
        Node* next;

        Node(int value, Node* prev= nullptr, Node* next = nullptr): value(value), prev(prev), next(next) {}
    };
    struct LinkedList{
        Node* start;
        Node* end;

        LinkedList(): start(nullptr), end(nullptr) {}

        void addElement(int data){
            if (start== nullptr){
                Node* node = new Node(data);
                start=end=node;
                return;
            }
            Node* node = new Node(data,end,start);
            end->next=node;
            start->prev=node;
            end = end->next;
        }
        void sortList(){
            if (start==end) return;
            Node* current;
            if (start->value%2==0){
                current = start;
                while (current->value%2==0 && current!=end){
                    current=current->next;
                }
                if (current==end) return;
                start->value=current->value;
            }else{
                current=start->next;
            }
            Node* last=start;
            do {
                if(current->value%2!=0){
                    last = last->next;
                    if(last->next!=current) {
                        int temp = last->value;
                        last->value = current->value;
                        current->value = temp;
                    }
                }
                current=current->next;
            } while (current!=start);
        }
    };
    //-------------------------------------------------------------------------------------------------------

    void print(Node *&root) {
        Node *current = root;
        do{
            std::cout << current->value << " ";
            current = current->next;
        }while (current != root);
        std::cout << std::endl;
    }

    void fillRandom(LinkedList &list, int size) {
        for (int i = 0; i < size; ++i) {
            list.addElement(rand()%100);
        }
    }
    //2----------------------------------------------------------------------------------------------------------
    struct TreeNode{
        int value;
        TreeNode* left;
        TreeNode* right;

        TreeNode(int value): value(value), left(nullptr), right(nullptr) {}
    };
    struct StackNode{
        TreeNode* value;
        StackNode* next;
        StackNode* prev;

        StackNode(TreeNode* value): value(value), next(nullptr), prev(nullptr) {}
    };
    struct Stack{
        StackNode* start;
        StackNode* end;

        Stack(): start(nullptr), end(nullptr) {}

        void add(TreeNode* value){
            StackNode* node = new StackNode(value);
            if (start== nullptr){
                start=end=node;
                return;
            }
            node->prev=end;
            end->next=node;
            end=end->next;
        }
        void remove(){
            if (start == nullptr) return;
            if(start==end){
                start=end= nullptr;
                return;
            }
            StackNode* newEnd = end->prev;
            newEnd->next= nullptr;
            delete end;
            end = newEnd;
        }
        bool isEmpty(){
            if(start== nullptr) return true;
            return false;
        }
    };
    void reverse(TreeNode* root){
        if (root== nullptr) return;
        Stack nodes;
        nodes.add(root);
        Stack output;
        while (!nodes.isEmpty()){
            TreeNode* current = nodes.end->value;
            nodes.remove();
            output.add(current);
            if (current->left!= nullptr) nodes.add(current->left);
            if(current->right!= nullptr) nodes.add(current->right);
        }
        while (!output.isEmpty()){
            std::cout << output.end->value->value << " ";
            output.remove();
        }
        std::cout<<std::endl;
    }
    //3--------------------------------------------------------------------------------------------------------
    struct GraphNode{
        int vertex;
        GraphNode* next;

        GraphNode(int vertex): vertex(vertex) {}
    };
    struct Graph{
        int numVertices;
        GraphNode** graph;

        Graph(int numVertices): numVertices(numVertices) {
            graph = new GraphNode*[numVertices];
            for (int i = 0; i < numVertices; ++i) {
                graph[i] = nullptr;
            }
        }
        void addEdge(int v1, int v2){
            GraphNode* edge = new GraphNode(v2);
            edge->next=graph[v1];
            graph[v1]=edge;
        }
        GraphNode* findAdj(int v1){
            GraphNode* vertices;
            for (int i = 0; i < ; ++i) {

            }
        }
    };
    int main(){
        LinkedList list;
        fillRandom(list, 35);
        print(list.start);
        list.sortList();
        print(list.start);

        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->right = new TreeNode(3);
        root->left->left = new TreeNode(4);
        root->left->right = new TreeNode(5);
        root->right->left = new TreeNode(6);
        root->right->right = new TreeNode(7);
        reverse(root);
        return 0;
    }
}