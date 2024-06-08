//
// Created by User on 08.06.2024.
//
#include <iostream>

namespace var_2{
    struct Node{
        int value;
        Node* next;
        Node* prev;

        Node(int value): value(value), next(nullptr), prev(nullptr) {}
    };
    struct LinkedList{
        Node *start;
        Node* end;

        LinkedList(): start(nullptr), end(nullptr) {}

        void task(){
            if (start== nullptr || start->next==end){
                return;
            }
            Node* minValue = start;
            Node* maxValue = end;
            Node* current = start;
            int i = 1, j=1, k=INT_MAX;
            while (current!= nullptr){
                if (current->value<minValue->value){
                    minValue=current;
                    j=i;
                }
                if (current->value>maxValue->value){
                    maxValue=current;
                    k=i;
                }
                current=current->next;
                i++;
            }
            if (k>j){
                minValue=minValue->next;
                while (minValue!=maxValue){
                    std::cout << minValue->value << " ";
                    minValue=minValue->next;
                }
                std::cout << std::endl;
            } else{
                maxValue=maxValue->next;
                while (maxValue!=minValue){
                    std::cout << minValue->value << " ";
                    maxValue=maxValue->next;
                }
                std::cout << std::endl;
            }
        }
        //--------------------------------------------------------------------------------------------------------
    };
    void print(Node *&root) {
        Node *current = root;
        while (current != nullptr) {
            std::cout << current->value << " ";
            current = current->next;
        }
        std::cout << std::endl;
    }

    void fillRandom(LinkedList &list, int size) {
        if (list.start == nullptr) {
            list.start = list.end = new Node(rand() % 100);
            size--;
        }
        for (int i = 0; i < size; ++i) {
            Node *newNode = new Node(rand() % 100);
            newNode->prev = list.end;
            list.end->next = newNode;
            list.end = list.end->next;
        }
    }
    //2---------------------------------------------------------------------------------------------------------
    struct TreeNode{
        int value;
        TreeNode* left;
        TreeNode* right;

        TreeNode(int value): value(value), left(nullptr), right(nullptr) {}
    };
    template <typename T>
    struct QueueNode{
        T value;
        QueueNode* next;
        QueueNode* prev;

        QueueNode(T value, QueueNode* prev= nullptr, QueueNode* next= nullptr): value(value), next(next), prev(prev) {}
    };
    template <typename T>
    struct Queue{
        QueueNode<T>* start;
        QueueNode<T>* end;

        Queue(): start(nullptr), end(nullptr) {}

        void add(TreeNode* data){
            QueueNode<T>* node = new QueueNode<T>(data);
            if (start== nullptr){
                start=end=node;
                return;
            }
            end->next=node;
            node->prev=end;
            end=end->next;
        }
        void remove(){
            if (start== nullptr) return;
            if (start==end){
                delete start;
                start=end= nullptr;
                return;
            }
            QueueNode<T>* newStart = start->next;
            newStart->prev= nullptr;
            delete start;
            start = newStart;
        }
        bool isEmpty(){
            if (start== nullptr){
                return true;
            }
            return false;
        }
    };
    void printTree(TreeNode*& root){
        if (root== nullptr) return;
        Queue<TreeNode*> q;
        q.add(root);
        while (!q.isEmpty()){
            int levelSize=0;
            QueueNode<TreeNode*>* temp = q.start;
            while (temp!= nullptr){
                levelSize++;
                temp=temp->next;
            }

            for (int i = 0; i < levelSize; ++i) {
                TreeNode* current = q.start->value;
                q.remove();
                std::cout << current->value << " ";

                if (current->left!= nullptr) q.add(current->left);
                if (current->right!= nullptr) q.add(current->right);
            }
            std::cout << std::endl;
        }
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
            graph=new GraphNode*[numVertices];
            for (int i = 0; i < numVertices; ++i) {
                graph[i]= nullptr;
            }
        }
        bool hasEdge(int v1, int v2){
            GraphNode* current = graph[v1];
            while (current!= nullptr){
                if (current->vertex==v2) return true;
                current=current->next;
            }
            return false;
        }
        bool isOriented(){
            for (int i = 0; i < numVertices; ++i) {
                GraphNode* current = graph[i];
                while (current!= nullptr){
                    if(!hasEdge(current->vertex,i)) return true;
                    current=current->next;
                }
            }
            return false;
        }
        //за умови, що граф зв'язний, інакше - потрібна перевірка
        bool isEiler(){
            if(isOriented()){
                int in[numVertices];
                int out[numVertices];
                for (int i = 0; i < numVertices; ++i) {
                    in[i]=0;
                    out[i]=0;
                }
                for (int i = 0; i < numVertices; ++i) {
                    GraphNode* current = graph[i];
                    int n=0;
                    while (current!= nullptr){
                        in[current->vertex]++;
                        n++;
                        current=current->next;
                    }
                    out[i]=n;
                }
                for (int i = 0; i < numVertices; ++i) {
                    if (in[i]!=out[i]) return false;
                }
            }else{
                for (int i = 0; i < numVertices; ++i) {
                    GraphNode* current = graph[i];
                    int n=0;
                    while (current!= nullptr){
                        n++;
                        current=current->next;
                    }
                    if (n%2!=0) return false;
                }
            }
            return true;
        }
        //----------------------------------------------------------------------------------------------------
        void addEdge(int v1, int v2){
            GraphNode* node = new GraphNode(v2);
            node->next=graph[v1];
            graph[v1]= node;
        }
    };
    int main(){
        LinkedList list;
        fillRandom(list, 35);
        print(list.start);
        list.task();

        TreeNode *root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->right = new TreeNode(3);
        root->left->left = new TreeNode(4);
        root->left->right = new TreeNode(5);
        root->right->left = new TreeNode(6);
        root->right->right = new TreeNode(7);
        printTree(root);

        Graph undirectedGraph(6);
        undirectedGraph.addEdge(0, 1);
        undirectedGraph.addEdge(0, 3);
        undirectedGraph.addEdge(1, 2);
        undirectedGraph.addEdge(2, 4);
        undirectedGraph.addEdge(3, 5);
        undirectedGraph.addEdge(4, 5);
        undirectedGraph.addEdge(1, 0);
        undirectedGraph.addEdge(3, 0);
        undirectedGraph.addEdge(2, 1);
        undirectedGraph.addEdge(4, 2);
        undirectedGraph.addEdge(5, 3);
        undirectedGraph.addEdge(5, 4);
        (undirectedGraph.isEiler())? std::cout << "yes":std::cout<<"no";
        std::cout<<std::endl;

        Graph directedGraph(4);
        directedGraph.addEdge(0, 1);
        directedGraph.addEdge(1, 2);
        directedGraph.addEdge(2, 3);
        directedGraph.addEdge(3, 0);
        (directedGraph.isEiler())? std::cout << "yes":std::cout<<"no";
        std::cout<<std::endl;
        return 0;
    }
}