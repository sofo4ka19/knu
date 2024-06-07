//
// Created by User on 07.06.2024.
//
#include <iostream>
#include <vector>
//1----------------------------------------------------------------------------------------------------------
struct Node{
    int value;
    Node* next;
    Node* prev;
    Node(int value): value(value), next(nullptr), prev(nullptr) {}
};
struct LinkedList{
    Node* start;
    Node* end;

    LinkedList(): start(nullptr), end(nullptr) {}
};
void sortChoose(Node*& root){
    int min_value = INT_MAX;
    Node* min_el = root;
    Node* current = root;
    while (current!= nullptr){
        if (current->value<min_value){
            min_value=current->value;
            min_el=current;
        }
        current=current->next;
    }
    min_el->value=root->value;
    root->value=min_value;
    if (root->next!= nullptr) sortChoose(root->next);
}
//---------------------------------------------------------------------------------------------------------
void print(Node*& root){
    Node* current = root;
    while (current!= nullptr){
        std::cout << current->value << " ";
        current=current->next;
    }
    std::cout<< std::endl;
}
void fillRandom(LinkedList& list, int size){
    if (list.start== nullptr){
        list.start = list.end = new Node(rand()%100);
        size--;
    }
    for (int i = 0; i < size; ++i) {
        Node* newNode = new Node(rand()%100);
        newNode->prev=list.end;
        list.end->next=newNode;
        list.end=list.end->next;
    }
}
//2----------------------------------------------------------------------------------------------------------
struct TreeNode{
    int value;
    TreeNode* left;
    TreeNode* right;

    TreeNode(int value): value(value), left(nullptr), right(nullptr) {}
};
struct QueueNode{
    TreeNode* value;
    QueueNode* next;
    QueueNode* prev;

    QueueNode(TreeNode* value): value(value), next(nullptr), prev(nullptr) {}
};
struct Queue{
    QueueNode* start;
    QueueNode* end;

    Queue(): start(nullptr), end(nullptr) {};

    void add(TreeNode* value){
        QueueNode* node = new QueueNode(value);
        if (isEmpty()){
            start=end=node;
            return;
        }
        node->prev=end;
        end->next=node;
        end=end->next;
    }
    void remove(){
        if (isEmpty()){
            return;
        }
        else if(start->next== nullptr){
            end = nullptr;
            delete start;
            start= nullptr;
            return;
        }
        QueueNode* newStart = start->next;
        newStart->prev = nullptr;
        delete start;
        start=newStart;
    }
    bool isEmpty(){
        if(start== nullptr){
            return true;
        }
        return false;
    }
};
void printTree(TreeNode* root){
    if (root== nullptr){
        return;
    }

    Queue q;
    q.add(root);
    while (!q.isEmpty()){
        int levelSize = 0;
        QueueNode* temp = q.start;
        while (temp != nullptr) {
            ++levelSize;
            temp = temp->next;
        }

        for (int i = 0; i < levelSize; ++i) {
            TreeNode* node = q.start->value;
            q.remove();

            // Виводимо значення вузла
            std::cout << node->value << " ";

            // Додаємо дочірні вузли в чергу
            if (node->left != nullptr) {
                q.add(node->left);
            }
            if (node->right != nullptr) {
                q.add(node->right);
            }
        }
        // Переходимо на новий рівень
        std::cout << std::endl;
    }
}
//3-----------------------------------------------------------------------------------------------------------
struct GraphNode{
    int vertex;
    GraphNode* next;

    GraphNode(int vertex): vertex(vertex), next(nullptr) {}
};
struct Graph{
    int numVertices;
    GraphNode** graph;

    Graph(int numVertices): numVertices(numVertices){
        graph = new GraphNode*[numVertices];
        for (int i = 0; i < numVertices; ++i) {
            graph[i]= nullptr;
        }
    }
    bool checkAdj(int v1, int v2){
        GraphNode* current = graph[v1];
        while (current!= nullptr){
            if (current->vertex==v2) return true;
            current=current->next;
        }
        return false;
    }
    //-------------------------------------------------------------------------------------------------------
    void addEdge(int v1, int v2){
        GraphNode* edge = new GraphNode(v2);
        edge->next=graph[v1];
        graph[v1]=edge;

        GraphNode* edge_rev = new GraphNode(v1);
        edge_rev->next=graph[v2];
        graph[v2]=edge_rev;
    }
    void print(){
        for (int i = 0; i < numVertices; i++) {
            std::cout << "Vertex " << i << " -> ";
            GraphNode* current = graph[i];
            while (current != nullptr) {
                std::cout << current->vertex << " ";
                current = current->next;
            }
            std::cout << std::endl;
        }
    }
};
int main(){
    LinkedList list;
    fillRandom(list, 35);
    print(list.start);
    sortChoose(list.start);
    print(list.start);

    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);
    printTree(root);

    Graph graph(15);
    for (int i = 0; i < 15; ++i) {
        graph.addEdge(rand()%15, rand()%15);
    }
    graph.addEdge(0,5);
    graph.print();
    std::cout << graph.checkAdj(0,5) << " " << graph.checkAdj(3,8) << " " << graph.checkAdj(5,0);
}