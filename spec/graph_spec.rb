require 'spec_helper'
require_relative '../lib/graph'

RSpec.describe Graph do
  describe '#null?' do
    it 'returns true for a new graph' do
      graph = Graph.new
      expect(graph.null?).to be true
    end

    it 'returns false after adding a vertex' do
      graph = Graph.new
      graph.add_vertex('A')
      expect(graph.null?).to be false
    end
  end
end
