import numpy as np
from manim import *

class Moment_Inertia(Scene):

    def construct(self):
        center_mass = np.array([9/10, 9/10, 0])
        f = ParametricFunction(
                lambda t: np.array(
               (3 * np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 
                3 * np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0)
            ), t_range = np.array([0, PI]), fill_opacity=0.2
        ).set_color(BLUE)
        g = ParametricFunction(
                lambda t: np.array(
               (3 * np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 
                3 * np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0)
            ), t_range = np.array([0, PI]), fill_opacity=1
        ).set_color(RED)
        center = f.get_center()

        self.add(g)
        com = Dot(np.array([9/10, 9/10, 0]))
        self.add_foreground_mobject(com)
        omega_equation = Tex(r"Torque = ${\displaystyle \frac{d\, \text{(angular velocity)}}{dt}}$").move_to(2.5*DOWN)
        self.add(omega_equation)
        self.wait(1)
        self.play(FadeOut(g), 
                  # FadeOut(com),
                  FadeOut(omega_equation),
                  Create(f))
        dotgroup = VGroup()
        for x in range(-10, 10):
            for y in range(-10, 10):
                d = Dot(np.array([x/3, y/3, 0]), color=BLUE).scale(0.5)
                dotgroup.add((Intersection(d, f)))
        self.play(Create(dotgroup))
        self.wait(2)

        example_mass = Dot(np.array([1/3, 6/3, 0]))
        example_r = Arrow(start=center_mass,
                        end=np.array([1/3, 6/3, 0]),
                        max_tip_length_to_length_ratio=0.15,
                        color=GOLD,
                        buff=0)
        r_label = Tex(r"$|r|$", color=GOLD).move_to(np.array([0, 1.2, 0]))

        inertia_equation = Tex(r"(Moment of inertia)$_{\text{point mass}}$ = $m|r|^2$").move_to(2.5*DOWN)
        inertia_equation_2 = Tex(r"${\displaystyle I_{\text{body}} = \sum_i m_i |r|^2}$").move_to(2.5*DOWN)

        self.play(Create(inertia_equation), 
                  FadeOut(dotgroup), 
                  Create(example_mass), 
                  Create(example_r), 
                  Create(r_label))
        self.wait(2)
        self.play(inertia_equation.animate.become(inertia_equation_2), 
                  FadeIn(dotgroup), 
                  FadeOut(example_mass), 
                  FadeOut(example_r), 
                  FadeOut(r_label))
        self.wait(2)

        self.play(FadeIn(g),
                  FadeOut(dotgroup),
                  FadeIn(omega_equation),
                  FadeOut(f), 
                  FadeOut(inertia_equation))
        self.wait(2)

