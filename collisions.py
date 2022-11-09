from manim import *

class Collisions(Scene):
    

    def construct(self):
        slide = Tex(r"Rigid Body \\ Collisions", font_size=72)
        self.play(Create(slide))
        self.wait(3)
        self.play(FadeOut(slide, scale=0.3))
