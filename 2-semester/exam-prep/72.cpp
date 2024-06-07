//
// Created by User on 07.06.2024.
//
#include <iostream>
namespace var_72 {
//1------------------------------------------------------------------------------------------------------------
    struct Node {
        int value;
        Node *next;

        Node(int value) : value(value), next(nullptr) {}
    };

    struct Sparce {
        int value;
        int position;
        Sparce *next;

        Sparce(int value, int position) : value(value), position(position), next(nullptr) {}
    };

    Sparce *convert(Node *start) {
        Sparce *result= nullptr;
        Sparce *current= nullptr;
        int i = 1;
        while (start != nullptr) {
            if (start->value != 0) {
                Sparce *node = new Sparce(start->value, i);
                if (result == nullptr) {
                    result = current = node;
                } else {
                    current->next = node;
                    current = current->next;
                }
            }
            i++;
            start = start->next;
        }
        return result;
    }

//--------------------------------------------------------------------------------------------------------------------
    void fillRandom(Node*& root, int size) {
        root = new Node(rand() % 3); // Початковий вузол
        Node* current = root;
        for (int i = 1; i < size; ++i) {
            Node* newNode = new Node(rand() % 3);
            current->next = newNode;
            current = current->next;
        }
    }

    void print(Node *root) {
        while (root != nullptr) {
            std::cout << root->value << " ";
            root=root->next;
        }
        std::cout << std::endl;
    }

    void print(Sparce *root) {
        while (root != nullptr) {
            std::cout << "(" << root->position << "," << root->value << ") ";
            root=root->next;
        }
        std::cout << std::endl;
    }
//2-----------------------------------------------------------------------------------------------------------
    struct TreeNode{
        int value;
        TreeNode* left;
        TreeNode* right;

        TreeNode(int value): value(value), left(nullptr), right(nullptr) {}
    };
    struct QueueNode {
        TreeNode *value;
        QueueNode *next;
        QueueNode *prev;

        QueueNode(TreeNode *value) : value(value), next(nullptr), prev(nullptr) {}
    };

    struct Queue {
        QueueNode *start;
        QueueNode *end;

        Queue() : start(nullptr), end(nullptr) {};

        void add(TreeNode *value) {
            QueueNode *node = new QueueNode(value);
            if (isEmpty()) {
                start = end = node;
                return;
            }
            node->prev = end;
            end->next = node;
            end = end->next;
        }

        void remove() {
            if (isEmpty()) {
                return;
            } else if (start->next == nullptr) {
                end = nullptr;
                delete start;
                start = nullptr;
                return;
            }
            QueueNode *newStart = start->next;
            newStart->prev = nullptr;
            delete start;
            start = newStart;
        }

        bool isEmpty() {
            if (start == nullptr) {
                return true;
            }
            return false;
        }
    };
    TreeNode* find(int v, TreeNode*& root){
        if (root== nullptr) return nullptr;
         Queue q;
         int i=0;
         q.add(root);
        while (!q.isEmpty()){
            int levelSize = 0;
            QueueNode* temp = q.start;
            while (temp!= nullptr){
                levelSize++;
                temp=temp->next;
            }

            for (int j = 0; j < levelSize; ++j) {
                TreeNode* current = q.start->value;
                q.remove();
                if (current->value==v){
                    std::cout << "level:" << i << std::endl;
                    return current;
                }
                if (current->left!= nullptr){
                    q.add(current->left);
                }
                if (current->right!= nullptr){
                    q.add(current->right);
                }
            }
            i++;
        }
        return nullptr;
    }
    //3---------------------------------------------------------------------------------------------------------
    struct GraphMatrix{
        int** graph;
        int numVertices;

        GraphMatrix(int numVertices): numVertices(numVertices) {
            graph = new int*[numVertices];
            for (int i = 0; i < numVertices; ++i) {
                graph[i] = new int[numVertices];
            }
        }
    };
    struct GraphNode {
        int vertex;
        GraphNode *next;

        GraphNode(int vertex) : vertex(vertex), next(nullptr) {}
    };

    struct Graph {
        int numVertices;
        GraphNode **graph;

        Graph(int numVertices) : numVertices(numVertices) {
            graph = new GraphNode *[numVertices];
            for (int i = 0; i < numVertices; ++i) {
                graph[i] = nullptr;
            }
        }
        void addEdge(int v1, int v2){
            GraphNode* edge = new GraphNode(v2);
            edge->next = graph[v1];
            graph[v1]=edge;
        }
    };
    Graph fromMatrixToStructure(GraphMatrix graph){
        Graph result(graph.numVertices);
        for (int i = 0; i < graph.numVertices; ++i) {
            for (int j = 0; j < graph.numVertices; ++j) {
                if (graph.graph[i][j]!=0){
                    result.addEdge(i,j);
                }
            }
        }
        return result;
    }
    //-------------------------------------------------------------------------------------------------------
    void fillRandomAndPrint(GraphMatrix& graph){
        for (int i = 0; i < graph.numVertices; ++i) {
            for (int j = 0; j < graph.numVertices; ++j) {
                graph.graph[i][j]=rand()%2;
                std::cout << graph.graph[i][j] << " ";
            }
            std::cout<<std::endl;
        }
    }
    void printGraph(Graph& graph) {
        for (int i = 0; i < graph.numVertices; i++) {
            std::cout << "Vertex " << i << " -> ";
            GraphNode *current = graph.graph[i];
            while (current != nullptr) {
                std::cout << current->vertex << " ";
                current = current->next;
            }
            std::cout << std::endl;
        }
    }
    int main() {
        Node *root = nullptr;
        fillRandom(root, 100);
        print(root);
        print(convert(root));

        TreeNode *node = new TreeNode(1);
        node->left = new TreeNode(2);
        node->right = new TreeNode(3);
        node->left->left = new TreeNode(4);
        node->left->right = new TreeNode(5);
        node->right->left = new TreeNode(6);
        node->right->right = new TreeNode(7);
        std::cout << find(7,node)->value<< std::endl;

        GraphMatrix matrix(12);
        fillRandomAndPrint(matrix);
        Graph graph = fromMatrixToStructure(matrix);
        printGraph(graph);
        return 0;
    }
}