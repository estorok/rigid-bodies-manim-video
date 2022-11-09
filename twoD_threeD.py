import math
from manim import *

class TwoD_ThreeD(Scene):

    def construct(self):
        s = 1.5
        g = ParametricFunction(
                lambda t: np.array(
               (s * np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 
                s * np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0)
            ), t_range = np.array([0, PI]), fill_opacity=1
        ).set_color(RED).move_to(0.8*UP + 3*LEFT)
        threeD_img = ImageMobject("images/sphere.png").scale(0.4).move_to(0.8*UP + 3 * RIGHT)
        threeD_rhr = ImageMobject("images/sphere-righthandrule.png").scale(0.4).move_to(0.8*UP + 3 * RIGHT)

        twoD_label = Tex(r"2D", font_size=72).move_to(3*LEFT + 3*UP)
        threeD_label = Tex(r"3D", font_size=72).move_to(3*RIGHT + 3*UP)

        self.play(Create(g), 
                  FadeIn(threeD_img), 
                  Create(twoD_label), 
                  Create(threeD_label))
        self.wait(2)

        position = MathTex(r"\begin{bmatrix} x \\ y \end{bmatrix} \to \begin{bmatrix} x \\ y \\ z \end{bmatrix}").move_to(2*DOWN)
        velocity = MathTex(r"\begin{bmatrix} v_x \\ v_y \end{bmatrix} \to \begin{bmatrix} v_x \\ v_y \\ v_z \end{bmatrix}").move_to(2*DOWN)
        acceleration = MathTex(r"\begin{bmatrix} a_x \\ a_y \end{bmatrix} \to \begin{bmatrix} a_x \\ a_y \\ a_z \end{bmatrix}").move_to(2*DOWN)
        omega = MathTex(r"\omega \to \begin{bmatrix} \omega_i \\ \omega_j \\ \omega_k \end{bmatrix}").move_to(2*DOWN)
        alpha = MathTex(r"\tau \to \begin{bmatrix} \tau_i \\ \tau_j \\ \tau_k \end{bmatrix}").move_to(2*DOWN)
        orientation = MathTex(r"\theta \to& a + b\mathbf{i} + c\mathbf{j} + d\mathbf{k} \\ &\text{ (quaternion)} \\ \leftrightarrow& R(x)R(y)R(z) \\ =& \begin{bmatrix} a & b & c \\ d & e & f \\ h & i & j \end{bmatrix}", font_size=36).move_to(2*DOWN)
        orientation_blurb = Tex(r"(combined $3 \times 3$ rotation matrix)", font_size=24).move_to(2.8*DOWN + 3*RIGHT)

        self.play(Create(position))
        self.wait(1)
        self.play(FadeOut(position, run_time=0.4), Create(velocity))
        self.wait(1)
        self.play(FadeOut(velocity, run_time=0.4), Create(acceleration))
        self.wait(1)
        self.play(FadeOut(acceleration, run_time=0.4), Create(omega))
        self.wait(1)
        self.play(FadeIn(threeD_rhr))
        self.wait(1)
        self.play(FadeOut(omega, run_time=0.4), Create(alpha))
        self.wait(1)
        self.play(FadeOut(alpha, run_time=0.4), Create(orientation))
        self.play(Create(orientation_blurb))
        self.wait(1)



