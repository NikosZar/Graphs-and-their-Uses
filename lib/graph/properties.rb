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

  # if two graphs have the same number of vertices and their corresponding vertices are connected by an edge then isomorphic
  # this implies they also need to have the same number of edges if they have the same number of vertices
  def isomorphic?
  end
end
