# Class for analyzing properties of graphs
module GraphProperties
  def null?
    edges.values.all?(&:empty?)
  end

  def complete?
    total_edges = edges.values.sum(&:size) / 2 # Each edge is counted twice
    total_edges == (vertices.length * (vertices.length - 1)) / 2
  end

  # for complement graph
  def missing_edges
    # Step 1: collect all the possible edges
    all_possible = vertices.to_a.combination(2).to_set
    # Step 2: Collect all the current edges
    current_edges = Set.new
    edges.each do |vertex, neighbors|
      neighbors.each do |neighbor|
        current_edges.add([vertex, neighbor].sort)
      end
    end
    # Step 3: Return the difference
    all_possible - current_edges
  end

  # if two graphs have the same number of vertices
  # and their corresponding vertices are connected by an edge then isomorphic
  # this implies they also need to have the same number of edges if they have the same number of vertices
  # graph1 is self and graph2 is the other graph
  def isomorphic?(other)
    return false unless same_basic_properties?(other)

    check_possible_mappings(other)
  end

  private

  def same_basic_properties?(other)
    vertices.size == other.vertices.size &&
      edge_count == other.edge_count
  end

  def edge_count
    edges.values.sum(&:size) / 2
  end

  def check_possible_mappings(other)
    other.vertices.to_a.permutation(vertices.size).any? do |perm|
      valid_mapping?(other, vertices.zip(perm).to_h)
    end
  end

  def valid_mapping?(other, paired_vertices)
    edges.all? do |vertex, neighbors|
      mapped_vertex = paired_vertices[vertex]
      mapped_neighbors = neighbors.map { |n| paired_vertices[n] }.to_set
      other.edges[mapped_vertex] == mapped_neighbors
    end
  end
end
