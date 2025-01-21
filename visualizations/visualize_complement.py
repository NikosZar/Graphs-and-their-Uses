from manim import *
import json
import numpy as np

class ComplementGraphVisualization(Scene):
    def construct(self):
        # Read the graph data
        with open('graph_data.json', 'r') as f:
            data = json.load(f)

        # Setup positions with more space between graphs
        original_vertices = {}
        complement_vertices = {}
        vertex_labels = {}
        complement_labels = {}
        radius = 1.5
        LEFT_OFFSET = -3.5  # Move original graph more left
        RIGHT_OFFSET = 3.5  # Move complement more right
        VERTEX_BUFFER = 0.4
        LABEL_PADDING = 5  # Increased from 4 to 5 for more space

        # Define fixed positions and label directions for each vertex
        vertex_configs = {
            'A': {'angle': 0,     'label_dir': RIGHT},  # Right
            'B': {'angle': PI/2,   'label_dir': UP},    # Top
            'C': {'angle': PI,     'label_dir': LEFT},  # Left
            'D': {'angle': 3*PI/2, 'label_dir': DOWN}   # Bottom
        }

        # Create vertices with fixed positions and label directions
        for v in data['vertices']:
            config = vertex_configs[v]
            angle = config['angle']
            label_dir = config['label_dir']

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # Original graph vertices (left side)
            orig_dot = Dot(point=np.array([x + LEFT_OFFSET, y, 0]))
            label = Text(str(v))
            label.next_to(orig_dot, label_dir, buff=0.3)
            original_vertices[v] = VGroup(orig_dot)  # Create VGroup for vertex
            vertex_labels[v] = label

            # Complement vertices (right side)
            comp_dot = Dot(point=np.array([x + RIGHT_OFFSET, y, 0]))
            comp_label = Text(str(v))
            comp_label.next_to(comp_dot, label_dir, buff=0.3)
            complement_vertices[v] = VGroup(comp_dot)  # Create VGroup for vertex
            complement_labels[v] = comp_label

            # If this is vertex D, ensure its label stays below
            if v == 'D':
                label.next_to(orig_dot, DOWN, buff=0.3)
                comp_label.next_to(comp_dot, DOWN, buff=0.3)

        # Create original edges with increased buffer
        original_edges = []
        for v1, neighbors in data['edges'].items():
            for v2 in neighbors:
                if v2 > v1:
                    line = Line(
                        original_vertices[v1].get_center(),
                        original_vertices[v2].get_center(),
                        buff=VERTEX_BUFFER,  # Use increased buffer
                        color=BLUE
                    )
                    original_edges.append(line)

        # Create complement edges with increased buffer
        complement_edges = []
        dotted_complement_edges = []
        for i, v1 in enumerate(data['vertices']):
            for v2 in data['vertices'][i+1:]:
                if v2 not in data['edges'].get(v1, []):
                    # Dotted line with increased buffer
                    dotted = DashedLine(
                        original_vertices[v1].get_center(),
                        original_vertices[v2].get_center(),
                        buff=VERTEX_BUFFER,  # Use increased buffer
                        color=RED_A,
                        dash_length=0.1
                    )
                    dotted_complement_edges.append(dotted)

                    # Solid line with increased buffer
                    solid = Line(
                        complement_vertices[v1].get_center(),
                        complement_vertices[v2].get_center(),
                        buff=VERTEX_BUFFER,  # Use increased buffer
                        color=RED
                    )
                    complement_edges.append(solid)

        # Labels with increased padding
        g_label = Text("Graph G").next_to(
            VGroup(*original_vertices.values()),
            DOWN * LABEL_PADDING  # Using increased padding
        )

        # Create G with overline
        g_text = Text("G")
        overline = Line(
            g_text.get_left() + UP * 0.3,
            g_text.get_right() + UP * 0.3,
            color=WHITE
        )
        complement_label = VGroup(g_text, overline).next_to(
            VGroup(*complement_vertices.values()),
            DOWN * LABEL_PADDING  # Using increased padding
        )

        # Animation sequence
        # 1. Show original graph
        self.play(
            *[Create(dot) for dot in original_vertices.values()],
            *[Write(label) for label in vertex_labels.values()]
        )
        self.play(*[Create(edge) for edge in original_edges])
        self.play(Write(g_label))

        # 2. Show dotted complement edges
        self.play(*[Create(edge) for edge in dotted_complement_edges])
        self.wait(1)

        # 3. Create copies and move them right
        vertex_copies = {}
        label_copies = {}
        for v in data['vertices']:
            vertex_copies[v] = original_vertices[v].copy()
            label_copies[v] = vertex_labels[v].copy()
            if v == 'D':  # Force D's label position again
                label_copies[v].next_to(vertex_copies[v], DOWN, buff=0.3)

        # Move everything to the right
        self.play(
            *[vertex_copies[v].animate.move_to(complement_vertices[v]) for v in data['vertices']],
            *[label_copies[v].animate.next_to(complement_vertices[v][0],
                vertex_configs[v]['label_dir'], buff=0.3) for v in data['vertices']],
            *[dotted.animate.become(solid) for dotted, solid in zip(dotted_complement_edges, complement_edges)],
            run_time=2
        )

        # 4. Show complement label
        self.play(Write(complement_label))

        # Final pause
        self.wait(2)