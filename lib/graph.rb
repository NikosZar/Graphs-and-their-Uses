require 'set'
require 'json'

class Graph
  attr_reader :vertices, :edges

  def initialize
    @vertices = Set.new
    @edges = {}
  end

  def add_vertex(vertex)
    vertices.add(vertex)
    edges[vertex] ||= Set.new
  end

  def add_edge(vertex1, vertex2)
    add_vertex(vertex1)
    add_vertex(vertex2)
    edges[vertex1].add(vertex2)
    edges[vertex2].add(vertex1)  # For undirected graph
  end

  def neighbors(vertex)
    edges[vertex]
  end

  def to_json
    {
      vertices: vertices.to_a,
      edges: edges.transform_values(&:to_a)
    }.to_json
  end
end