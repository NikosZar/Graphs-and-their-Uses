from manim import *
import json

class GraphVisualization(Scene):
    def construct(self):
        # Read the graph data
        with open('graph_data.json', 'r') as f:
            data = json.load(f)
            print("Loaded data:", data)

        # Create vertices
        vertices = {}
        radius = 2
        for i, v in enumerate(data['vertices']):
            # Position vertices in a circle
            angle = i * (2 * PI / len(data['vertices']))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # Create dot and label
            dot = Dot(point=[x, y, 0])
            label = Text(str(v)).next_to(dot, DOWN * 0.5)
            vertex_group = VGroup(dot, label)

            # Add to scene with animation
            self.play(
                Create(dot),
                Write(label)
            )
            vertices[v] = dot

        # Create edges
        for v1, neighbors in data['edges'].items():
            for v2 in neighbors:
                if v2 > v1:  # Avoid duplicate edges
                    line = Line(
                        vertices[v1].get_center(),
                        vertices[v2].get_center()
                    )
                    self.play(Create(line))

        # Wait at the end
        self.wait(2)