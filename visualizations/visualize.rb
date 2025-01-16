require_relative '../lib/graph'
require 'json'

# Create and populate your graph
graph = Graph.new
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')
graph.add_vertex('D')
graph.add_vertex('E')
# graph.add_edge('B', 'C')
# graph.add_edge('C', 'A')

# Export graph data
File.write('graph_data.json', graph.to_json)
puts 'JSON file created successfully!'

# Call manim with high quality (1080p) and preview
# command = 'manim -pqh visualize_graph.py GraphVisualization'
# no save
command = 'manim render -p -ql visualize_graph.py GraphVisualization'
puts "Running command: #{command}"
result = system(command)

if result
  puts 'Manim completed successfully!'
else
  puts "Error running Manim. Exit code: #{$?.exitstatus}"
end
