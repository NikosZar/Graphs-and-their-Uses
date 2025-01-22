from manim import *
import json
import numpy as np

class IsomorphismVisualization(Scene):
    def construct(self):
        # Setup positions
        radius = 1.5
        LEFT_OFFSET = -3.5
        RIGHT_OFFSET = 3.5

        # Title
        title = Text("Graph Isomorphism Check", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # Define fixed positions and label directions
        vertex_configs = {
            'A': {'angle': 0,      'label_dir': RIGHT},   # Right
            'B': {'angle': 2*PI/3,  'label_dir': UP},     # Top
            'C': {'angle': 4*PI/3,  'label_dir': LEFT},   # Left (changed from DOWN)
            'X': {'angle': 0,      'label_dir': RIGHT},   # Right
            'Y': {'angle': 2*PI/3,  'label_dir': UP},     # Top
            'Z': {'angle': 4*PI/3,  'label_dir': LEFT}    # Left (changed from DOWN)
        }

        # Create vertices with proper label positioning
        g1_dots, g1_labels = self.create_graph(['A', 'B', 'C'], vertex_configs, LEFT_OFFSET, radius)
        g2_dots, g2_labels = self.create_graph(['X', 'Y', 'Z'], vertex_configs, RIGHT_OFFSET, radius)

        # Create edges
        g1_edges = self.create_edges(g1_dots, [('A','B'), ('B','C')], BLUE)
        g2_edges = self.create_edges(g2_dots, [('X','Y'), ('Y','Z')], BLUE)

        # Labels
        g1_label = Text("Graph G1").next_to(VGroup(*g1_dots.values()), DOWN * 3)
        g2_label = Text("Graph G2").next_to(VGroup(*g2_dots.values()), DOWN * 3)

        # Step 1: Show initial check
        step1 = Text("Step 1: Check vertex and edge counts", font_size=24)
        step1.next_to(title, DOWN)

        vertex_count = Text("|V1| = |V2| = 3", font_size=20, color=GREEN)
        edge_count = Text("|E1| = |E2| = 2", font_size=20, color=GREEN)
        counts = VGroup(vertex_count, edge_count).arrange(DOWN)
        counts.next_to(step1, DOWN)

        # Show graphs and initial checks
        self.play(
            *[Create(dot) for dot in g1_dots.values()],
            *[Write(label) for label in g1_labels.values()],
            *[Create(edge) for edge in g1_edges],
            Write(g1_label)
        )

        self.play(
            *[Create(dot) for dot in g2_dots.values()],
            *[Write(label) for label in g2_labels.values()],
            *[Create(edge) for edge in g2_edges],
            Write(g2_label)
        )

        self.play(Write(step1))
        self.play(Write(counts))
        self.wait(1)

        # Step 2: Try mappings
        self.play(
            FadeOut(step1),
            FadeOut(counts)
        )

        step2 = Text("Step 2: Try possible vertex mappings", font_size=24)
        step2.next_to(title, DOWN)
        self.play(Write(step2))

        # Show all possible permutations
        permutation_text = Text("Possible mappings:", font_size=20).next_to(step2, DOWN)
        self.play(Write(permutation_text))

        mappings = [
            {'A': 'X', 'B': 'Y', 'C': 'Z'},
            {'A': 'X', 'B': 'Z', 'C': 'Y'},
            {'A': 'Y', 'B': 'X', 'C': 'Z'},
            {'A': 'Y', 'B': 'Z', 'C': 'X'},
            {'A': 'Z', 'B': 'X', 'C': 'Y'},
            {'A': 'Z', 'B': 'Y', 'C': 'X'}
        ]

        for mapping in mappings:
            mapping_text = Text(
                f"Testing: {' → '.join([f'{k}-{v}' for k,v in mapping.items()])}",
                font_size=18
            ).next_to(permutation_text, DOWN)

            arrows = []
            for v1, v2 in mapping.items():
                arrow = Arrow(
                    g1_dots[v1].get_center(),
                    g2_dots[v2].get_center(),
                    color=YELLOW,
                    buff=0.2
                )
                arrows.append(arrow)

            self.play(
                Write(mapping_text),
                *[Create(arrow) for arrow in arrows]
            )

            success = self.check_mapping(mapping, [('A','B'), ('B','C')], [('X','Y'), ('Y','Z')])

            # Use simple ASCII if Unicode doesn't display well
            check_symbol = "[✓]" if success else "[x]"  # or use "[+]" and "[-]"
            result_text = Text(
                f"{check_symbol} Edges {'' if success else 'not '}preserved",
                font_size=18,
                color=GREEN if success else RED
            ).next_to(mapping_text, DOWN)

            self.play(
                *[arrow.animate.set_color(GREEN if success else RED) for arrow in arrows],
                Write(result_text)
            )

            self.wait(1)
            self.play(
                *[Uncreate(arrow) for arrow in arrows],
                FadeOut(mapping_text),
                FadeOut(result_text)
            )

        conclusion = Text(
            "Graphs are isomorphic!",
            color=GREEN,
            font_size=30
        ).next_to(step2, DOWN * 2.5)

        self.play(Write(conclusion))
        self.wait(2)

    def create_graph(self, vertices, configs, offset, radius):
        dots = {}
        labels = {}
        for v in vertices:
            config = configs[v]
            angle = config['angle']
            label_dir = config['label_dir']

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            dot = Dot(point=np.array([x + offset, y, 0]))
            label = Text(v).next_to(dot, label_dir, buff=0.3)
            dots[v] = dot
            labels[v] = label
        return dots, labels

    def create_edges(self, dots, edges, color):
        return [
            Line(dots[v1].get_center(), dots[v2].get_center(), color=color)
            for v1, v2 in edges
        ]

    def check_mapping(self, mapping, edges1, edges2):
        mapped_edges = set()
        for v1, v2 in edges1:
            mapped_edges.add(tuple(sorted([mapping[v1], mapping[v2]])))
        return mapped_edges == set(tuple(sorted(e)) for e in edges2)