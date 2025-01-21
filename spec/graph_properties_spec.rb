# frozen_string_literal: true

require 'spec_helper'
require_relative '../lib/graph'

RSpec.describe GraphProperties do
  let(:graph) { Graph.new }

  describe '#null?' do
    it 'returns true for a new graph' do
      expect(graph.null?).to be true
    end

    it 'returns true for a graph with only vertices' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      expect(graph.null?).to be true
    end

    it 'returns false after adding an edge' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_edge('A', 'B')
      expect(graph.null?).to be false
    end
  end

  describe '#complete?' do
    it 'returns true for K1 (single vertex)' do
      graph.add_vertex('A')
      expect(graph.complete?).to be true
    end

    it 'returns true for K2 (two connected vertices)' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_edge('A', 'B')
      expect(graph.complete?).to be true
    end

    it 'returns false for incomplete graph' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_vertex('C')
      graph.add_edge('A', 'B')
      expect(graph.complete?).to be false
    end

    it 'returns true for K3 (triangle)' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_vertex('C')
      graph.add_edge('A', 'B')
      graph.add_edge('B', 'C')
      graph.add_edge('A', 'C')
      expect(graph.complete?).to be true
    end
  end

  describe '#missing_edges' do
    it 'returns missing edges in a partially connected graph' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_vertex('C')
      graph.add_edge('A', 'B')
      graph.add_edge('B', 'C')

      expected = Set[%w[A C]]
      expect(graph.missing_edges).to eq(expected)
    end

    it 'returns no missing edges for a complete graph' do
      graph.add_vertex('A')
      graph.add_vertex('B')
      graph.add_vertex('C')
      graph.add_edge('A', 'B')
      graph.add_edge('B', 'C')
      graph.add_edge('A', 'C')
      expect(graph.missing_edges).to eq(Set.new)
    end

    it 'returns empty set for empty graph (no vertices)' do
      expect(graph.missing_edges).to eq(Set.new)
    end

    it 'returs empty set for graph with single vertex' do
      graph.add_vertex('A')
      expect(graph.missing_edges).to eq(Set.new)
    end
  end
end
