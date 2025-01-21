require_relative '../lib/graph'
require 'json'

# Create and populate your graph
graph = Graph.new
# Example: Create a path graph
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'D')

# Export graph data to visualizations directory
File.write(File.join(__dir__, 'graph_data.json'), graph.to_json)
puts 'JSON file created successfully!'

# Call manim with correct path
script_path = File.join(__dir__, 'visualize_complement.py')
command = "manim -pql #{script_path} ComplementGraphVisualization"
puts "Running command: #{command}"
result = system(command)

if result
  puts 'Manim completed successfully!'
else
  puts "Error running Manim. Exit code: #{$?.exitstatus}"
end
