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
        vertex_groups = {}
        radius = 2
        for i, v in enumerate(data['vertices']):
            # Position vertices in a circle
            angle = i * (2 * PI / len(data['vertices']))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # Create dot
            dot = Dot(point=[x, y, 0])

            # Determine label position based on angle
            if -PI/4 <= angle <= PI/4:  # Right side
                label_direction = RIGHT
            elif PI/4 < angle < 3*PI/4:  # Top
                label_direction = UP
            elif -3*PI/4 <= angle <= -PI/4:  # Bottom
                label_direction = DOWN
            else:  # Left side
                label_direction = LEFT

            # Position label with direction-based padding
            label = Text(str(v)).next_to(dot, label_direction * 0.5)
            vertex_group = VGroup(dot, label)

            # Add to scene with animation
            self.play(
                Create(dot),
                Write(label)
            )
            vertices[v] = dot
            vertex_groups[v] = vertex_group

        # Create edges with padding
        for v1, neighbors in data['edges'].items():
            for v2 in neighbors:
                if v2 > v1:  # Avoid duplicate edges
                    start_dot = vertices[v1]
                    end_dot = vertices[v2]

                    line = Line(
                        start_dot.get_center(),
                        end_dot.get_center(),
                        buff=0.2
                    )
                    self.play(Create(line))

        # Wait at the end
        self.wait(2)