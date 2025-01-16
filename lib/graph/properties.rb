require_relative '../graph'

# Class for analyzing properties of graphs
module GraphProperties
  def null?
    edges.empty?
  end

  def complete?
    edges.length == (vertices.length * (vertices.length - 1)) / 2
  end
end
