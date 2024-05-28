// Block 0: 1, 2

#include <iostream>
#include <vector>
#include <random>

struct MatrixGraph{
    int vertices;
    bool oriented;
    std::vector<std::vector<int>> graph;

    MatrixGraph(int vertices, bool oriented): vertices{vertices}, oriented(oriented) {
        graph.resize(vertices, std::vector<int>(vertices,0));
    }
    void addEdge(int v1, int v2, int weight=1){
        if(v1>=vertices || v2>=vertices || v1<0 || v2<0){
            std::cout << "inappropriate value" << std::endl;
            return;
        }
        if(graph[v1][v2]!=0){
            std::cout << "there's an edge yet" << std::endl;
            return;
        }
        graph[v1][v2]=weight;
        if (!oriented) graph[v2][v1]=weight;
    }
    void print(){
        for (int i = 0; i < vertices; ++i) {
            for (int j = 0; j < vertices; ++j) {
                std::cout << graph[i][j] << " ";
            }
            std::cout << std::endl;
        }
    }
    void clear(){
        for (int i = 0; i < vertices; ++i) {
            for (int j = 0; j < vertices; ++j) {
                graph[i][j]=0;
            }
        }
    }
    void createRandom(int edges){
        if (edges<0 || edges>2*vertices){
            std::cout << "inappropriate value" << std::endl;
            return;
        }
        this->clear();
        std::random_device rd;
        std::mt19937 gen(rd());
        for (int i = 0; i < edges; ++i) {
            std::uniform_int_distribution<> v1(0, vertices - 1);
            std::uniform_int_distribution<> v2(0, vertices - 1);
            std::uniform_int_distribution<> weightDist(1, 10);
            if (graph[v1(gen)][v2(gen)]!=0){ i--; }
            else{
                this->addEdge(v1(gen), v2(gen), weightDist(gen));
            }
        }
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
    void printEdges(){
        for (int i = 0; i < edges.size(); ++i) {
            std::cout << "(" << edges[i].destination << ", " << edges[i].weight << ") ";
        }
    }
    bool hasEdge(int dest) const {
        for (const Edge& edge : edges) {
            if (edge.destination == dest) {
                return true;
            }
        }
        return false;
    }
    void clear() {
        edges.clear();
    }
};

struct Graph {
    std::vector<Vertex> vertices;
    bool oriented;

    Graph(int size, bool oriented): oriented(oriented){
            vertices.resize(size);
    }

    void addEdge(int v1, int v2, int weight=1) {
        if(v1>=vertices.size() || v2>=vertices.size() || v1<0 || v2<0){
            std::cout << "inappropriate value" << std::endl;
            return;
        }
        if(vertices[v1].hasEdge(v2)){
            std::cout << "there's an edge yet" << std::endl;
            return;
        }
        vertices[v1].addEdge(v2, weight);
        if(!oriented) vertices[v2].addEdge(v1, weight);
    }
    void print(){
        for (int i = 0; i < vertices.size(); ++i) {
            std::cout << "Vertice " << i << ": ";
            vertices[i].printEdges();
            std::cout << std::endl;
        }
    }
    void clear(){
        for (auto& vertex : vertices) {
            vertex.clear();
        }
    }
    void createRandom(int edges){
        if (edges<0 || edges>2*vertices.size()){
            std::cout << "inappropriate value" << std::endl;
            return;
        }
        this->clear();
        std::random_device rd;
        std::mt19937 gen(rd());
        for (int i = 0; i < edges; ++i) {
            std::uniform_int_distribution<> v1(0, vertices.size() - 1);
            std::uniform_int_distribution<> v2(0, vertices.size() - 1);
            std::uniform_int_distribution<> weightDist(1, 10);
            if (vertices[v1(gen)].hasEdge(v2(gen))){ i--; }
            else{
                this->addEdge(v1(gen), v2(gen), weightDist(gen));
            }
        }
    }
};

MatrixGraph fromStructureToMatrix(Graph& graph){
    MatrixGraph matrixGraph(graph.vertices.size(), graph.oriented);
    for (int i = 0; i < graph.vertices.size(); ++i) {
        for (int j = 0; j < graph.vertices[i].edges.size(); ++j) {
            matrixGraph.addEdge(i,graph.vertices[i].edges[j].destination, graph.vertices[i].edges[j].weight);
        }
    }
    return matrixGraph;
}
Graph fromMatrixToStructure(MatrixGraph& matrixGraph){
    Graph graph(matrixGraph.vertices, matrixGraph.oriented);
    for (int i = 0; i < matrixGraph.vertices; ++i) {
        for (int j = (matrixGraph.oriented ? 0 : i); j < matrixGraph.vertices; ++j) {
            if (matrixGraph.graph[i][j]!=0){
                graph.addEdge(i,j,matrixGraph.graph[i][j]);
            }
        }
    }
    return graph;
}
template <typename GraphType>
void interactiveGraph(GraphType& graph) {
    bool running = true;
    while (running) {
        std::cout << "Choose what you want to do:\n"
                     "1. Add an edge\n"
                     "2. Print the graph\n"
                     "3. Create random graph\n"
                     "4. Convert graph and print\n"
                     "5. Exit\n";
        int action;
        std::cin >> action;
        if (std::cin.fail() || action < 1 || action > 5) {
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
                    Graph listGraph = fromMatrixToStructure(graph);
                    listGraph.print();
                    interactiveGraph(listGraph);
                    return;
                } else {
                    MatrixGraph matrixGraph = fromStructureToMatrix(graph);
                    matrixGraph.print();
                    interactiveGraph(matrixGraph);
                    return;
                }
                break;
            }
            default:
                running = false;
                break;
        }
    }
}

void interactive(){
    std::cout << "Enter the number of vertices: ";
    int numVertices;
    std::cin >> numVertices;
    if (std::cin.fail() || numVertices < 1) return ;

    std::cout << "Is the graph oriented? (0 for no, 1 for yes): ";
    bool oriented;
    std::cin >> oriented;
    if (std::cin.fail()) return;

    std::cout << "Choose type of graph's structure: 1 - adjacency matrix; 2 - adjacency list: ";
    int choice;
    std::cin >> choice;

    if (choice == 1) {
        MatrixGraph graph(numVertices, oriented);
        interactiveGraph(graph);
    } else if (choice == 2) {
        Graph graph(numVertices, oriented);
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
