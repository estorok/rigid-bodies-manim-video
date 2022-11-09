from manim import *

class Credits(Scene):
    
    
    def construct(self):
        center_mass = np.array([9/10, 9/10, 0])
        offset = LEFT + DOWN
        f = ParametricFunction(
                lambda t: np.array(
               (3 * np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 
                3 * np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0)
            ), t_range = np.array([0, PI]), fill_opacity=0.2
        ).set_color(BLUE)
        center = f.get_center()

        thanks_text = Tex(r"Thank you for watching!", font_size=60).move_to(3*UP)
        text_group = VGroup()
        credit = Tex(r"Original animations and script by", font_size=24).move_to(UP)
        ethan = Tex(r"Ethan Torok", font_size=24)
        jason = Tex(r"Jason Waataja", font_size=24)
        randy = Tex(r"Randy Zhang", font_size=24)
        text_group.add(ethan)
        text_group.add(jason)
        text_group.add(randy)
        text_group.arrange(DOWN, center=False, aligned_edge=LEFT)
        self.play(Create(thanks_text))
        self.wait(2)
        self.play(Create(f.move_to(0.5*DOWN)))
        self.wait(2)
        self.play(f.animate.become(text_group).move_to(0.1*LEFT),
                  Create(credit))
        self.wait(3)
        self.play(FadeOut(thanks_text),
                  FadeOut(f),
                  FadeOut(credit))
        self.wait(3)
