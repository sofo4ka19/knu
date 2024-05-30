//Block 0: 1, 2
//Block 1: 5
//Block 2: 13
//Block 3: 14
//Block 4: 17
//Block 5: 20
//Block 6: 21

#include <iostream>
#include <vector>
#include <random>
#include <stack>
#include <queue>
#include <cmath>
#include <algorithm>
#include <xmath.h>
#include <cassert>

struct KruskalEdge{
    int v1;
    int v2;
    int weight;
    KruskalEdge(int v1, int v2, int weight) : v1(v1), v2(v2), weight(weight) {}
};

template <typename EdgeType>
static bool compareEdges(const EdgeType& a, const EdgeType& b) {
    return a.weight < b.weight;
}
int findSet(int u, std::vector<int>& parent) {
    if (parent[u] != u)
        parent[u] = findSet(parent[u], parent);
    return parent[u];
}

void unionSets(int u, int v, std::vector<int>& parent, std::vector<int>& rank) {
    int rootU = findSet(u, parent);
    int rootV = findSet(v, parent);
    if (rootU != rootV) {
        if (rank[rootU] < rank[rootV])
            parent[rootU] = rootV;
        else if (rank[rootU] > rank[rootV])
            parent[rootV] = rootU;
        else {
            parent[rootV] = rootU;
            rank[rootU]++;
        }
    }
}

struct MatrixGraph {
    int vertices;
    bool oriented;
    std::vector<std::vector<int>> graph;

    MatrixGraph(int vertices, bool oriented) : vertices{vertices}, oriented(oriented) {
        graph.resize(vertices, std::vector<int>(vertices, 0));
    }

    void addEdge(int v1, int v2, int weight = 1) {
        if (v1 >= vertices || v2 >= vertices || v1 < 0 || v2 < 0 || v1 == v2) {
            std::cout << "Inappropriate value" << std::endl;
            return;
        }
        if (graph[v1][v2] != 0) {
            std::cout << "Edge already exists" << std::endl;
            return;
        }
        graph[v1][v2] = weight;
        if (!oriented) graph[v2][v1] = weight;
    }

    void print() const {
        for (const auto& row : graph) {
            for (int val : row) {
                std::cout << val << " ";
            }
            std::cout << std::endl;
        }
    }

    void clear() {
        for (auto& row : graph) {
            std::fill(row.begin(), row.end(), 0);
        }
    }

    void createRandom(int edges) {
        if (edges < 0 || edges > vertices * (vertices - 1) / 2) {
            std::cout << "Inappropriate value" << std::endl;
            return;
        }
        clear();
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dist(0, vertices - 1);
        std::uniform_int_distribution<> weightDist(1, 10);

        int count = 0;
        while (count < edges) {
            int v1 = dist(gen);
            int v2 = dist(gen);
            if (graph[v1][v2] == 0 && v1 != v2) {
                addEdge(v1, v2, weightDist(gen));
                count++;
            }
        }
    }

    bool isConnectedOne(int vertice) const {
        std::vector<bool> visited(vertices, false);
        std::stack<int> stack;
        stack.push(vertice);
        visited[vertice] = true;
        int visitedCount = 1;

        while (!stack.empty()) {
            int vertex = stack.top();
            stack.pop();
            for (int i = 0; i < vertices; i++) {
                if (graph[vertex][i] && !visited[i]) {
                    stack.push(i);
                    visited[i] = true;
                    visitedCount++;
                }
            }
        }
        return visitedCount == vertices;
    }
    bool isConnected(){
        if (!oriented) return isConnectedOne(0);
        for (int i = 0; i < vertices; ++i) {
            if (!isConnectedOne(i)) return false;
        }
        return true;
    }
    void BFS(int start) const {
        std::vector<bool> visited(graph.size(), false);
        std::queue<int> queue;
        queue.push(start);
        visited[start] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            std::cout << vertex << " ";

            for (int i = 0; i < graph.size(); ++i) {
                if (graph[vertex][i] != 0 && !visited[i]) {
                    queue.push(i);
                    visited[i] = true;
                }
            }
        }
    }
    void BFS_Weight(int start) const {
        std::vector<bool> visited(graph.size(), false);
        std::queue<int> queue;
        queue.push(start);
        visited[start] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            std::cout << vertex << " ";

            std::vector<std::pair<int, int>> neighbors;
            for (int i = 0; i < graph.size(); ++i) {
                if (graph[vertex][i] != 0 && !visited[i]) {
                    neighbors.push_back({i,graph[vertex][i]} );
                    visited[i] = true;
                }
            }

            std::sort(neighbors.begin(), neighbors.end(), [](const std::pair<int, int>& a, const std::pair<int, int>& b) {
                return a.second < b.second;
            });
            for (std::pair<int, int> neighbor : neighbors) {
                queue.push(neighbor.first);
            }
        }
    }
    std::vector<int> dijkstra(int start) const {
        assert(start<vertices);
        std::vector<int> distance(vertices, std::numeric_limits<int>::max());
        std::vector<bool> visited(vertices, false);
        distance[start] = 0;

        for (int i = 0; i < vertices; ++i) {
            int minDistance = std::numeric_limits<int>::max();
            int u = -1;
            for (int j = 0; j < vertices; ++j) {
                if (!visited[j] && distance[j] < minDistance) {
                    minDistance = distance[j];
                    u = j;
                }
            }
            if (u == -1) break;
            visited[u] = true;

            for (int v = 0; v < vertices; ++v) {
                if (graph[u][v] != 0 && !visited[v]) {
                    int newDist = distance[u] + graph[u][v];
                    if (newDist < distance[v]) {
                        distance[v] = newDist;
                    }
                }
            }
        }

        return distance;
    }
    int size(){
        return vertices;
    }

    /*void topologySort(std::vector<bool>& visited, std::vector<int>& sorted,int n){
            visited[n]=true;
            for (int i = 0; i < vertices; ++i) {
                if (graph[n][i] != 0 && !visited[i]) topologySort(visited,sorted,i);
            }
            sorted.push_back(n);
    }*/
    void topologySortKan(){
        std::vector<int> inDegree(vertices, 0);

        for (int u = 0; u < vertices; ++u) {
            for (int v = 0; v < vertices; ++v) {
                if (graph[u][v] != 0) {
                    inDegree[v]++;
                }
            }
        }

        std::queue<int> q;
        for (int i = 0; i < vertices; ++i) {
            if (inDegree[i] == 0) {
                q.push(i);
            }
        }

        int count = 0;
        std::vector<int> topOrder;

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            topOrder.push_back(u);

            for (int v = 0; v < vertices; ++v) {
                if (graph[u][v] != 0 && --inDegree[v] == 0) {
                    q.push(v);
                }
            }
            count++;
        }

        if (count != vertices) {
            std::cout << "Cycle detected in the graph." << std::endl;
            return;
        }

        for (int i : topOrder) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
    MatrixGraph buildSpanningTree(){
        std::vector<bool> visited(vertices, false);
        MatrixGraph spanningTree(vertices, oriented);
        std::queue<int> queue;

        queue.push(0);
        visited[0] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();

            for (int i = 0; i < vertices; ++i) {
                if (graph[vertex][i] != 0 && !visited[i]) {
                    queue.push(i);
                    visited[i] = true;
                    spanningTree.graph[vertex][i]=graph[vertex][i];
                    if(!oriented) spanningTree.graph[i][vertex]=graph[vertex][i];
                }
            }
        }

        return spanningTree;
    }
    int weight(){
        int sumWeight=0;
        for(int i=0; i<vertices; i++){
            for (int j = (oriented)?(0):(i); j < vertices; ++j) {
                sumWeight+=graph[i][j];
            }
        }
        return sumWeight;
    }
    MatrixGraph kruskalMST() {
        std::vector<KruskalEdge> edges;
        for (int i = 0; i < vertices; i++) {
            for (int j = 0; j < vertices; j++) {
                if (graph[i][j] != 0) {
                    edges.emplace_back(i, j, graph[i][j]);
                }
            }
        }

        std::sort(edges.begin(), edges.end(), compareEdges<KruskalEdge>);

        MatrixGraph mst(vertices, oriented);
        std::vector<int> parent(vertices);
        std::vector<int> rank(vertices, 0);

        for (int i = 0; i < vertices; i++)
            parent[i] = i;

        for (const auto& edge : edges) {
            if (findSet(edge.v1, parent) != findSet(edge.v2, parent)) {
                mst.addEdge(edge.v1, edge.v2, edge.weight);
                unionSets(edge.v1, edge.v2, parent, rank);
            }
        }

        return mst;
    }
};

struct Edge {
    int destination;
    int weight;

    Edge(int dest, int w) : destination(dest), weight(w) {}
};
struct Vertex {
    std::vector<Edge> edges;

    void addEdge(int dest, int weight) {
        edges.emplace_back(dest, weight);
    }

    void printEdges() const {
        for (const auto& edge : edges) {
            std::cout << "(" << edge.destination << ", " << edge.weight << ") ";
        }
    }

    bool hasEdge(int dest) const {
        return std::any_of(edges.begin(), edges.end(), [dest](const Edge& edge) {
            return edge.destination == dest;
        });
    }

    void clear() {
        edges.clear();
    }

    void sortEdgesByWeight() {
        std::sort(edges.begin(), edges.end(), compareEdges<Edge>);
    }
};

struct ListGraph {
    std::vector<Vertex> vertices;
    bool oriented;

    ListGraph(int size, bool oriented) : oriented(oriented) {
        vertices.resize(size);
    }

    void addEdge(int v1, int v2, int weight = 1) {
        if (v1 >= vertices.size() || v2 >= vertices.size() || v1 < 0 || v2 < 0 || v1 == v2) {
            std::cout << "Inappropriate value" << std::endl;
            return;
        }
        if (vertices[v1].hasEdge(v2)) {
            std::cout << "Edge already exists" << std::endl;
            return;
        }
        vertices[v1].addEdge(v2, weight);
        if (!oriented) vertices[v2].addEdge(v1, weight);
    }

    void print() const {
        for (int i = 0; i < vertices.size(); ++i) {
            std::cout << "Vertex " << i << ": ";
            vertices[i].printEdges();
            std::cout << std::endl;
        }
    }

    void clear() {
        for (auto& vertex : vertices) {
            vertex.clear();
        }
    }

    void createRandom(int edges) {
        if (edges < 0 || (edges > floor(vertices.size() * (vertices.size()-1) / 2) && !oriented) || edges > vertices.size() * (vertices.size()-1)) {
            std::cout << "Inappropriate value" << std::endl;
            return;
        }
        clear();
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dist(0, vertices.size() - 1);
        std::uniform_int_distribution<> weightDist(1, 10);

        int count = 0;
        while (count < edges) {
            int v1 = dist(gen);
            int v2 = dist(gen);
            if (!vertices[v1].hasEdge(v2) && v1 != v2) {
                addEdge(v1, v2, weightDist(gen));
                count++;
            }
        }
    }

    bool isConnectedOne(int vertice) const { //needs updating for oriented graph
        std::vector<bool> visited(vertices.size(), false);
        std::queue<int> queue;
        queue.push(vertice);
        visited[vertice] = true;
        int visitedCount = 1;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            for (const auto& edge : vertices[vertex].edges) {
                if (!visited[edge.destination]) {
                    queue.push(edge.destination);
                    visited[edge.destination] = true;
                    visitedCount++;
                }
            }
        }
        return visitedCount == vertices.size();
    }
    bool isConnected(){
        if(!oriented) return isConnectedOne(0);
        for (int i = 0; i < vertices.size(); ++i) {
            if(!isConnectedOne(i)) return false;
        }
        return true;
    }
    void BFS(int start) const {
        std::vector<bool> visited(vertices.size(), false);
        std::queue<int> queue;
        queue.push(start);
        visited[start] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            std::cout << vertex << " ";

            for (const auto& neighbor : vertices[vertex].edges) {
                int dest = neighbor.destination;
                if (!visited[dest]) {
                    queue.push(dest);
                    visited[dest] = true;
                }
            }
        }
    }
    void BFS_Weight(int start){
        std::vector<bool> visited(vertices.size(), false);
        std::queue<int> queue;
        queue.push(start);
        visited[start] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            std::cout << vertex << " ";

            vertices[vertex].sortEdgesByWeight();

            for (const auto& neighbor : vertices[vertex].edges) {
                int dest = neighbor.destination;
                if (!visited[dest]) {
                    queue.push(dest);
                    visited[dest] = true;
                }
            }
        }
    }
    std::vector<int> dijkstra(int start) const {
        assert(start<vertices.size());
        std::vector<int> distance(vertices.size(), std::numeric_limits<int>::max());
        std::vector<bool> visited(vertices.size(), false);
        distance[start] = 0;

        for (int i = 0; i < vertices.size(); ++i) {
            int u = -1;
            for (int j = 0; j < vertices.size(); ++j) {
                if (!visited[j] && (u == -1 || distance[j] < distance[u])) {
                    u = j;
                }
            }

            if (distance[u] == std::numeric_limits<int>::max())
                break;

            visited[u] = true;
            for (const auto& edge : vertices[u].edges) {
                int v = edge.destination;
                if (!visited[v] && distance[u] + edge.weight < distance[v]) {
                    distance[v] = distance[u] + edge.weight;
                }
            }
        }

        return distance;
    }
    int size(){
        return vertices.size();
    }
    void topologySortKan(){
        std::vector<int> inDegree(vertices.size(), 0);

        for (int u = 0; u < vertices.size(); ++u) {
            for (int v = 0; v < vertices.size(); ++v) {
                if (vertices[u].hasEdge(v)) {
                    inDegree[v]++;
                }
            }
        }

        std::queue<int> q;
        for (int i = 0; i < vertices.size(); ++i) {
            if (inDegree[i] == 0) {
                q.push(i);
            }
        }

        int count = 0;
        std::vector<int> topOrder;

        while (!q.empty()) {
            int u = q.front();
            q.pop();
            topOrder.push_back(u);

            for (int v = 0; v < vertices.size(); ++v) {
                if (vertices[u].hasEdge(v) && --inDegree[v] == 0) {
                    q.push(v);
                }
            }
            count++;
        }

        if (count != vertices.size()) {
            std::cout << "Cycle detected in the graph." << std::endl;
            return;
        }

        for (int i : topOrder) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
    }
    /*void topologySort(std::vector<bool>& visited, std::vector<int>& sorted,int n){
        visited[n]=true;
        for (int i = 0; i < vertices.size(); ++i) {
            if (vertices[n].hasEdge(i) && !visited[i]) topologySort(visited,sorted,i);
        }
        sorted.push_back(n);
    }*/
    ListGraph buildSpanningTree(){
        std::vector<bool> visited(vertices.size(), false);
        ListGraph spanningTree(vertices.size(), oriented);
        std::queue<int> queue;

        queue.push(0);
        visited[0] = true;

        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();

                for (Edge& edge : vertices[vertex].edges) {
                int dest = edge.destination;
                if (!visited[dest]) {
                    queue.push(dest);
                    visited[dest] = true;
                    spanningTree.addEdge(vertex, dest, edge.weight);
                }
            }
        }

        return spanningTree;
    }
    int weight(){
        int sumWeight=0;
        for (Vertex& vertex:vertices) {
            for (Edge& edge:vertex.edges) {
                sumWeight+=edge.weight;
            }
        }
        if(oriented){
            return sumWeight;
        }
        return sumWeight/2;
    }
    ListGraph kruskalMST() {
        std::vector<KruskalEdge> edges;
        for (int i = 0; i < vertices.size(); i++) {
            for (const auto& edge : vertices[i].edges) {
                edges.emplace_back(i, edge.destination, edge.weight);
            }
        }

        std::sort(edges.begin(), edges.end(), compareEdges<KruskalEdge>);

        ListGraph mst(vertices.size(), oriented);
        std::vector<int> parent(vertices.size());
        std::vector<int> rank(vertices.size(), 0);

        for (int i = 0; i < vertices.size(); i++)
            parent[i] = i;

        for (const auto& edge : edges) {
            if (findSet(edge.v1, parent) != findSet(edge.v2, parent)) {
                mst.addEdge(edge.v1, edge.v2, edge.weight);
                unionSets(edge.v1, edge.v2, parent, rank);
            }
        }

        return mst;
    }
};

MatrixGraph fromStructureToMatrix(const ListGraph& graph) {
    MatrixGraph matrixGraph(graph.vertices.size(), graph.oriented);
    for (int i = 0; i < graph.vertices.size(); ++i) {
        for (const auto& edge : graph.vertices[i].edges) {
            matrixGraph.addEdge(i, edge.destination, edge.weight);
        }
    }
    return matrixGraph;
}

ListGraph fromMatrixToStructure(const MatrixGraph& matrixGraph) {
    ListGraph graph(matrixGraph.vertices, matrixGraph.oriented);
    for (int i = 0; i < matrixGraph.vertices; ++i) {
        for (int j = (matrixGraph.oriented ? 0 : i); j < matrixGraph.vertices; ++j) {
            if (matrixGraph.graph[i][j] != 0) {
                graph.addEdge(i, j, matrixGraph.graph[i][j]);
            }
        }
    }
    return graph;
}

/*template <typename GraphType>
void topologySortMain(GraphType& graph){
    std::vector<int> sorted;
    std::vector<bool> visited(graph.size(), false);
    for (int i = 0; i < graph.size(); ++i) {
        if(!visited[i]){
            graph.topologySort(visited, sorted, i);
        }
    }
    while (!sorted.empty()){
        std::cout << sorted[sorted.size()-1] << " ";
    }
    std::cout << std::endl;
}*/ //needs checking if there is a cycle before

template <typename GraphType>
void interactiveGraph(GraphType& graph) {
    bool running = true;
    while (running) {
        std::cout << "Choose an action:\n"
                     "1. Add an edge\n"
                     "2. Print the graph\n"
                     "3. Create a random graph\n"
                     "4. Convert graph and print\n"
                     "5. Check if the graph is connected\n"
                     "6. BFS\n"
                     "7. Find the shortest way (Dijkstra algorithm)\n"
                     "8. Topology sort\n"
                     "9. Build spanning tree\n"
                     "10. Build minimal spanning tree by Kruskal algorithm\n"
                     "11. Exit\n";
        int action;
        std::cin >> action;
        if (std::cin.fail() || action < 1 || action > 11) {
            std::cout << "Error" << std::endl;
            return;
        }
        switch (action) {
            case 1: {
                int v1, v2, weight;
                std::cout << "Enter vertices (v1 v2) and weight: ";
                std::cin >> v1 >> v2 >> weight;
                if (std::cin.fail()) return;
                graph.addEdge(v1, v2, weight);
                break;
            }
            case 2:
                graph.print();
                break;
            case 3: {
                int edges;
                std::cout << "Enter number of edges: ";
                std::cin >> edges;
                if (std::cin.fail()) return;
                graph.createRandom(edges);
                break;
            }
            case 4: {
                if constexpr (std::is_same<GraphType, MatrixGraph>::value) {
                    ListGraph listGraph = fromMatrixToStructure(graph);
                    listGraph.print();
                    interactiveGraph(listGraph);
                } else {
                    MatrixGraph matrixGraph = fromStructureToMatrix(graph);
                    matrixGraph.print();
                    interactiveGraph(matrixGraph);
                }
                return;
            }
            case 5:
                std::cout << (graph.isConnected() ? "Graph is connected" : "Graph is not connected") << std::endl;
                break;
            case 6:
                int vertex;
                bool isWeight;
                std::cout << "choose the start vertex" << std::endl;
                std::cin >> vertex;
                std::cout << "it should be according to the weight (1) or ordinary (0)" << std::endl;
                std::cin >> isWeight;
                if (std::cin.fail()) return;
                (isWeight)?(graph.BFS_Weight(vertex)):(graph.BFS(vertex));
                break;
            case 7:
                int choose;
                std::cout << "which way you want to find:\n"
                             "1. Between 2 vertices\n"
                             "2. From the vertex to the everyone\n"
                             "3. From everyone to everyone"
                             << std::endl;
                std::cin >> choose;
                if(std::cin.fail() || choose<1 || choose>3) return;
                switch (choose) {
                    case 1:
                        int v1, v2;
                        std::cout << "enter 2 vertices" << std::endl;
                        std::cin >> v1 >> v2;
                        if (std::cin.fail() || v1<0 || v2<0 || v2>=graph.size() || v1>=graph.size()){
                            std::cout << "error";
                            return;
                        }
                        if(graph.dijkstra(v1)[v2]!=std::numeric_limits<int>::max()){
                            std::cout << graph.dijkstra(v1)[v2] << std::endl;
                        }
                        else{
                            std::cout << "There is no way" << std::endl;
                        }
                        break;
                    case 2:
                        std::cout << "enter vertex" << std::endl;
                        std::cin >> v1;
                        if (std::cin.fail() || v1<0 || v1>=graph.size()){
                            std::cout << "error";
                            return;
                        }
                        int i;
                        i=0;
                        std::cout << "From vertex " << v1 << " to vertex:\n";
                        for(int way : graph.dijkstra(v1)){
                            if (way!=std::numeric_limits<int>::max()){
                                 std::cout << i << " - " << way << std::endl;
                            }
                            i++;
                        }
                        break;
                    case 3:
                        for (int j = 0; j < graph.size(); ++j) {
                            std::cout << "From vertex " << j << " to vertex:" << std::endl;
                            i=0;
                            for(int way : graph.dijkstra(j)){
                                if (way!=std::numeric_limits<int>::max()){
                                    std::cout << i << " - " << way << std::endl;
                                }
                                i++;
                            }
                        }
                        break;
                    default:
                        return;
                }
                break;
            case 8:
                if (!graph.oriented){
                    std::cout << "Graph is not oriented, you can't do a topology sort" << std::endl;
                } else{
                    graph.topologySortKan();
                }
                break;
            case 9:
                if(graph.isConnected()) {
                    graph.buildSpanningTree().print();
                    std::cout << "Weight: " << graph.buildSpanningTree().weight() << std::endl;
                }
                else{
                    std::cout << "Sorry, you can't to make spanning tree, because your graph is not connected" << std::endl;
                }
                break;
            case 10:
                if (graph.isConnected() && !graph.oriented){
                    graph.kruskalMST().print();
                    std::cout << "Weight: " << graph.kruskalMST().weight() << std::endl;
                }
                else{
                    std::cout << "Sorry, for building minimal spanning tree your graph is required to be connected and no-oriented" << std::endl;
                }
                break;
            case 11:
                running = false;
                break;
            default:
                return;
        }
    }
}

void interactive() {
    std::cout << "Enter the number of vertices: ";
    int numVertices;
    std::cin >> numVertices;
    if (std::cin.fail() || numVertices < 1) return;

    std::cout << "Is the graph oriented? (0 for no, 1 for yes): ";
    bool oriented;
    std::cin >> oriented;
    if (std::cin.fail()) return;

    std::cout << "Choose the type of graph structure: 1 - adjacency matrix; 2 - adjacency list: ";
    int choice;
    std::cin >> choice;

    if (choice == 1) {
        MatrixGraph graph(numVertices, oriented);
        interactiveGraph(graph);
    } else if (choice == 2) {
        ListGraph graph(numVertices, oriented);
        interactiveGraph(graph);
    } else {
        std::cout << "Invalid choice" << std::endl;
        return;
    }
}

int main() {
    interactive();
    return 0;
}