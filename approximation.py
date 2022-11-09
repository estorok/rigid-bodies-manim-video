from manim import *

class Approximation(Scene):
    

    def construct(self):
        slide = Tex(r"?????", font_size=72)
        eq = MathTex(r"\frac{d^2x}{dt^2} = \bigstar \lozenge \spadesuit \circlearrowright \dag \dag", font_size=60).move_to(DOWN)
        self.play(Create(slide))
        self.wait(3)
        self.play(slide.animate.become(Tex(r"Exact Solution?", font_size=60).move_to(UP)))
        self.play(Create(eq))
        self.wait(3)
