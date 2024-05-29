//Block 0: 1, 2
//Block 1: 5
//Block 2: 11

#include <iostream>
#include <vector>
#include <random>
#include <stack>
#include <queue>
#include <cmath>
#include <algorithm>

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
        if (edges < 0 || (edges > floor(vertices.size() * vertices.size() / 2) && !oriented) || edges > vertices.size() * vertices.size()) {
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
                     "6. Exit\n";
        int action;
        std::cin >> action;
        if (std::cin.fail() || action < 1 || action > 6) {
            std::cout << "Error" << std::endl;
            return;
        }
        switch (action) {
            case 1: {
                int v1, v2, weight;
                std::cout << "Enter vertices (v1 v2) and weight: ";
                std::cin >> v1 >> v2 >> weight;
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