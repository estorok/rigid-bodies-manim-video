import math
from manim import *

class Euler_Update(Scene):

    def construct(self):
        center_mass = np.array([9/10, 9/10, 0])
        g = ParametricFunction(
                lambda t: np.array(
               (3 * np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 
                3 * np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0)
            ), t_range = np.array([0, PI]), fill_opacity=1
        ).set_color(RED)
        com = Dot(np.array([9/10, 9/10, 0]))

        # force / velocity
        orbit_center_mass = 3*RIGHT + UP
        orbit = Circle(radius=2).move_to(RIGHT + UP)
        v_radius = math.sqrt(4+1.2**2)
        orbit_v = Circle(radius=v_radius).rotate(math.asin(1.2/v_radius)).move_to(RIGHT + UP)
        orbit_a = Circle(radius=0.8).move_to(RIGHT + UP)
        orbit_v_vec = Arrow(start=orbit_center_mass, 
                            end=orbit_center_mass+np.array([0, 1, 0]),
                            max_tip_length_to_length_ratio=0.2,
                            buff=0)
        orbit_v_text = Tex(r"$v$", font_size=36).move_to(orbit_center_mass 
                                                       + np.array([0, 1.2, 0]))
        orbit_a_vec = Arrow(start=orbit_center_mass, 
                            end=orbit_center_mass+np.array([-1, 0, 0]),
                            max_tip_length_to_length_ratio=0.2,
                            buff=0)
        # choosing to label the centripetal acceleration vector as F instead of A 
        # (they point in the same direction but we want to show that the force is causing motion)
        orbit_a_text = Tex(r"$F$", font_size=36).move_to(orbit_center_mass 
                                                       + np.array([-1.2, 0, 0]))

        # euler_text = MathTex(r"\begin{bmatrix} x \\ v \\ \theta \\ \omega \end{bmatrix} \gets \begin{bmatrix} x + \frac{dx}{dt} \Delta t \\ v + \frac{dv}{dt} \Delta t \\ \theta + \frac{d\theta}{dt} \Delta t \\ \omega + \frac{d\omega}{dt} \Delta t\end{bmatrix}").move_to(2*LEFT)
        # euler_text = MathTex(r"x &\gets x + \frac{dx}{dt} \Delta t \\ v &\gets v + \frac{dv}{dt} \Delta t \\ \theta &\gets \theta + \frac{d\theta}{dt} \Delta t \\ \omega &\gets \omega + \frac{d\omega}{dt} \Delta t").move_to(4*LEFT)
        euler_text_x = MathTex(r"x_{n+1} &\gets x_{n} + \frac{dx}{dt} \Delta t").move_to(4*LEFT)
        euler_text_v = MathTex(r"v_{n+1} &\gets v_{n} + \frac{dv}{dt} \Delta t ").move_to(4*LEFT)
        euler_text_theta = MathTex(r"\theta_{n+1} &\gets \theta_{n} + \frac{d\theta}{dt} \Delta t").move_to(4*LEFT)
        euler_text_omega = MathTex(r"\omega_{n+1} &\gets \omega_{n} + \frac{d\omega}{dt} \Delta t").move_to(4*LEFT)
        # euler_text_2 = MathTex(r"x &\gets x + v \Delta t \\ v &\gets v + \frac{F_{\text{net}}}{m} \Delta t \\ \theta &\gets \theta + \omega \Delta t \\ \omega &\gets \omega + \frac{\tau_{\text{net}}}{I} \Delta t").move_to(4*LEFT)
        euler_text_2_x = MathTex(r"x_{n+1} &\gets x_{n} + v_{n} \Delta t").move_to(4*LEFT)
        euler_text_2_v = MathTex(r"v_{n+1} &\gets v_{n} + \frac{F_{\text{net}}}{m} \Delta t ").move_to(4*LEFT)
        euler_text_2_theta = MathTex(r"\theta_{n+1} &\gets \theta_{n} + \omega{n} \Delta t").move_to(4*LEFT)
        euler_text_2_omega = MathTex(r"\omega_{n+1} &\gets \omega_{n} + \frac{\tau_{\text{net}}}{I} \Delta t").move_to(4*LEFT)
        euler_equations = VGroup()
        euler_equations.add(euler_text_x)
        euler_equations.add(euler_text_v)
        euler_equations.add(euler_text_theta)
        euler_equations.add(euler_text_omega)
        euler_equations.arrange_in_grid(4, 1, col_alignments="l", row_heights=[1.5, 1.5, 1.5, 1.5])
        euler_equations_2 = VGroup()
        euler_equations_2.add(euler_text_2_x)
        euler_equations_2.add(euler_text_2_v)
        euler_equations_2.add(euler_text_2_theta)
        euler_equations_2.add(euler_text_2_omega)
        euler_equations_2.arrange_in_grid(4, 1, col_alignments="l", row_heights=[1.5, 1.5, 1.5, 1.5]).shift(np.array([0.1, -0.15, 0]))


        self.play(g.animate.scale(1/3).move_to(orbit_center_mass), 
                  FadeOut(com, target_position=orbit_center_mass), 
                  Create(euler_equations))
        self.wait(1.5)
        self.play(Create(orbit_v_vec),
                  Create(orbit_a_vec),
                  Create(orbit_v_text),
                  Create(orbit_a_text))
        for i in range(3):
            if (i == 1):
                self.play(FadeOut(euler_equations, run_time=0.2), 
                          Create(euler_equations_2),
                          MoveAlongPath(g, orbit, rate_func=linear, run_time=5),
                          MoveAlongPath(orbit_v_text, orbit_v, rate_func=linear, run_time=5),
                          MoveAlongPath(orbit_a_text, orbit_a, rate_func=linear, run_time=5),
                          Rotate(orbit_v_vec, about_point=RIGHT + UP, angle=2*PI, rate_func=linear, run_time=5),
                          Rotate(orbit_a_vec, about_point=RIGHT + UP, angle=2*PI, rate_func=linear, run_time=5))
            else:
                self.play(MoveAlongPath(g, orbit),
                          MoveAlongPath(orbit_v_text, orbit_v),
                          MoveAlongPath(orbit_a_text, orbit_a),
                          Rotate(orbit_v_vec, about_point=RIGHT + UP, angle=2*PI),
                          Rotate(orbit_a_vec, about_point=RIGHT + UP, angle=2*PI), 
                                 rate_func=linear, run_time=5)
        self.wait(2)


