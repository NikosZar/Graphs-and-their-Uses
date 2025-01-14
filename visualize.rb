require_relative 'lib/graph'
require 'json'

def ensure_venv_activated
  venv_path = File.join(Dir.pwd, 'venv', 'bin', 'activate')
  unless ENV['VIRTUAL_ENV']
    puts "Activating virtual environment..."
    exec "source #{venv_path} && ruby #{__FILE__}"
  end
end

# Ensure virtual environment is activated
ensure_venv_activated

# Create and populate your graph
graph = Graph.new
graph.add_edge('A', 'B')
graph.add_edge('B', 'C')
graph.add_edge('C', 'A')

# Export graph data
File.write('graph_data.json', graph.to_json)
puts "JSON file created successfully!"

# Call manim with updated flags
command = 'manim -pql --verbosity DEBUG visualize_graph.py GraphVisualization'
puts "Running command: #{command}"
result = system(command)

if result
  puts "Manim completed successfully!"
else
  puts "Error running Manim. Exit code: #{$?.exitstatus}"
end