from manim import *

class TitleSequence(Scene):

    def construct(self):
        title = Tex("Rigid body modeling", font_size=72).move_to(2.5*UP)
        rigid_img = ImageMobject("images/sphere.png").scale(0.7).move_to(0.75*DOWN)
        non_rigid_img = ImageMobject("images/Cyprinus_carpio.jpeg")

        self.play(FadeIn(rigid_img),
                  Create(title))
        self.wait(2)
        self.play(title.animate.become(Tex("Rigid body", font_size=60).move_to(2.5*UP + 3*LEFT)),
                  Create(Tex("Non-rigid body", font_size=60).move_to(2.5*UP + 3*RIGHT)),
                  rigid_img.animate.scale(0.7).move_to(3*LEFT + 0.75*DOWN),
                  FadeIn(non_rigid_img.scale(0.25).move_to(3*RIGHT + 0.75*DOWN)))
        self.wait(3)
        # https://commons.wikimedia.org/wiki/File:Cyprinus_carpio.jpeg 
