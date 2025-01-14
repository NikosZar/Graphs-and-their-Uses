from manim import *
import json

class GraphVisualization(Scene):
    def construct(self):
        # Read the graph data from Ruby output
        with open('graph_data.json', 'r') as f:
            data = json.load(f)

        # Create vertices
        vertices = {}
        for v in data['vertices']:
            vertices[v] = Dot(point=self.get_vertex_position(v))
            self.add(vertices[v])
            # Add label
            label = Text(str(v)).next_to(vertices[v], DOWN, buff=0.1)
            self.add(label)

        # Create edges
        for v1, neighbors in data['edges'].items():
            for v2 in neighbors:
                line = Line(
                    vertices[v1].get_center(),
                    vertices[v2].get_center()
                )
                self.add(line)

    def get_vertex_position(self, vertex):
        # Simple circular layout
        angle = hash(str(vertex)) % 360
        radius = 2
        x = radius * np.cos(angle * DEGREES)
        y = radius * np.sin(angle * DEGREES)
        return np.array([x, y, 0])