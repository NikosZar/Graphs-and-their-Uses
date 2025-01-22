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
    # 1. quick check to see if self has the same number of vertices as other
    false unless vertices.size == other.vertices.size
    false unless (edges.values.sum(&:size) / 2) == (other.edges.values.sum(&:size) / 2)

    # now need to check corresponding edges for vertice pairs
    # get all possible ways to arrange the vertices of the second graph -> permutation doc
    all_possible = other.vertices.to_a.permutation(vertices.size)

    # Return true if ANY mapping works
    all_possible.any? do |perm|
      paired_vertices = vertices.zip(perm).to_h

      # Check if edge relationships are preserved
      edges.all? do |vertex, neighbors|
        # Get mapped vertex and its neighbors in other graph
        mapped_vertex = paired_vertices[vertex]
        mapped_neighbors = neighbors.map { |n| paired_vertices[n] }.to_set

        # Check if mapped neighbors match in other graph
        other.edges[mapped_vertex] == mapped_neighbors
      end
    end
  end
end
