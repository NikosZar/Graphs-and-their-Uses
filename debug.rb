require_relative 'lib/graph'

# Create test graphs
g1 = Graph.new
g2 = Graph.new

# Add some edges
g1.add_edge('A', 'B')
g1.add_edge('B', 'C')

g2.add_edge('X', 'Y')
g2.add_edge('Y', 'Z')

# Check isomorphism (this will print the debug info)
puts 'Testing isomorphism between graphs:'
g1.isomorphic?(g2)
