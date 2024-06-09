//
// Created by User on 09.06.2024.
//
#include <iostream>

namespace var_22{
    //1--------------------------------------------------------------------------------------------------------
    struct OneNode{
        int value;
        OneNode* next;

        OneNode(int value): value(value), next(nullptr) {}
    };
    struct TwoNode{
        int value;
        TwoNode* next;
        TwoNode* prev;

        TwoNode(int value, TwoNode* prev= nullptr, TwoNode* next= nullptr): value(value), next(nullptr), prev(prev) {}
    };
    template<typename Node>
    struct LinkedList{
        Node* start;
        Node* end;

        LinkedList(): start(nullptr), end(nullptr) {}
    };
    LinkedList<TwoNode> convert(LinkedList<OneNode> list){
        LinkedList<TwoNode> result;
        OneNode* current1 = list.start;
        while (current1!= nullptr){
            if (current1==list.start){
                TwoNode* current2=new TwoNode(current1->value);
                result.start=result.end = current2;
                current2->prev = current2;
                current2->next = current2;
            } else{
                TwoNode* current2=new TwoNode(current1->value, result.end, result.start);
                result.start->prev = current2;
                result.end->next = current2;
                result.end=result.end->next;
            }
            current1=current1->next;
        }
        return result;
    }
    //---------------------------------------------------------------------------------------------------------

    void print(TwoNode *&root) {
        TwoNode *current = root;
        while (current != nullptr) {
            std::cout << current->value << " ";
            current = current->next;
        }
        std::cout << std::endl;
    }
    //2-------------------------------------------------------------------------------------------------------
    struct TreeNode{
        int value;
        TreeNode* left;
        TreeNode* middle;
        TreeNode* right;

        TreeNode(int value): value(value), left(nullptr), middle(nullptr), right(nullptr) {}
    };
    int max(int v1, int v2, int v3){
        if (v1>v2){
            if (v1>v3) return v1;
            return v3;
        }
        if (v2>v3) return v2;
        return v3;
    }
    int deep(TreeNode* root){
        if (root== nullptr || (root->left== nullptr && root->right== nullptr && root->middle== nullptr)) return 0;
        return max(deep(root->left), deep(root->middle), deep(root->right))+1;
    }
    //3---------------------------------------------------------------------------------------------------------
    struct GraphNode{
        int vertex;
        GraphNode* next;

        GraphNode(int vertex): vertex(vertex), next(nullptr) {}
    };
    struct Graph{
        int numVertices;
        GraphNode** graph;

        Graph(int numVertices): numVertices(numVertices) {
            graph = new GraphNode*[numVertices];
            for (int i = 0; i < numVertices; ++i) {
                graph[i]= nullptr;
            }
        }
        void addEdge(int v1, int v2){
            GraphNode* node = new GraphNode(v2);
            node->next=graph[v1];
            graph[v1]=node;
        }
    };
    void findVerticesAtDistanceUtil(int current, int currentDistance, int distance, bool* result, bool* visited,
                                    Graph graph){
        if (currentDistance == distance){

            result[current] = true; // mark as reachable
            return;
        }
        visited[current] = true;
        GraphNode* neighbor = graph.graph[current];
        while (neighbor){
            if (!visited[neighbor->vertex]){
                findVerticesAtDistanceUtil(neighbor->vertex, currentDistance + 1,
                                           distance, result, visited, graph);
            }
            neighbor = neighbor->next;
        }
        visited[current] = false; // backtrack to allow other paths
    }

    void task3(int startVertex, int distance, Graph graph){
        if (distance < 0 || startVertex < 0 || startVertex >= graph.numVertices)
            return;
        bool result[graph.numVertices];
        bool visited[graph.numVertices];
        for (int i = 0; i < graph.numVertices; ++i) {
            visited[i]= false;
            result[i] = false;
        }

        findVerticesAtDistanceUtil(startVertex, 0, distance, result, visited, graph);

        std::cout << "Vertices at distance " << distance << " from vertex " << startVertex + 1 << " are: ";
        for (int i = 0; i < graph.numVertices; i++){
            if (result[i]) {
                std::cout << i + 1 << " ";
            }
        }
        std::cout << '\n';
    }
    //-------------------------------------------------------------------------------------------------------
    int main(){
        TreeNode* root = new TreeNode(1);
        root->left = new TreeNode(2);
        root->left->left = new TreeNode(3);
        root->left->middle = new TreeNode(4);
        root->left->middle->left = new TreeNode(5);
        root->left->middle->middle = new TreeNode(4);
        root->left->middle->middle->right = new TreeNode(4);
        root->middle = new TreeNode(2);
        root->right = new TreeNode(2);
        root->right->right = new TreeNode(2);
        root->right->middle = new TreeNode(2);
        root->right->middle->right = new TreeNode(2);
        std::cout << deep(root) << std::endl;

        Graph graph(7);
        graph.addEdge(0,1);
        graph.addEdge(1,5);
        graph.addEdge(1,6);
        graph.addEdge(1,0);
        graph.addEdge(2,6);
        graph.addEdge(3,6);
        graph.addEdge(3,4);
        graph.addEdge(4,3);
        graph.addEdge(4,5);
        graph.addEdge(5,1);
        graph.addEdge(5,4);
        graph.addEdge(6,1);
        graph.addEdge(6,2);
        graph.addEdge(6,3);
        task3(0,8,graph);
        return 0;
    }
}