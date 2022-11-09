import math
import numpy as np
from manim import *

class PlotRb_Rev(Scene):
    # lima bean curve
    def func(self):
        return lambda t: np.array((np.sin(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), np.cos(t) * (np.sin(t) ** 3 + np.cos(t) ** 3), 0))
    

    # this is used as a static method i.e. bad practice hack incoming
    def getTippedArc(self, radians: float, r: float, center: np.array) -> Mobject:
        arc = Arc(radius=r, start_angle=PI/2, angle=radians, arc_center=center)
        arc.add_tip(tip_length=0.15)
        return arc
        

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
        
        title = Tex(r"Rigid\\Bodies", font_size=48).move_to(3*LEFT)
        # basic 2d rigid body and title
        self.play(Create(title), Create(f))
        self.wait(1)

        # movement

        path1 = Line(start=f.get_center(), end=f.get_center()+np.array([10, 0, 0]), color=BLACK)
        forcev = Arrow(start=center_mass, end=center_mass+np.array([1, 0, 0]), 
                       max_stroke_width_to_length_ratio=10)
        self.play(Create(forcev))
        self.wait(1)
        group = VGroup(f, forcev)
        self.play(MoveAlongPath(group, path1), rate_func=rate_functions.ease_in_quad, run_time=4)

        # approximated as a bunch of point masses
        self.remove(f)
        self.play(Create(f.move_to(center)))
        self.wait(1)
        self.play(Rotate(f, angle=3*PI, 
                         about_point=center_mass), 
                         run_time=3
        )
        self.play(Rotate(f, angle=-1*PI, 
                         about_point=center_mass), 
                         run_time=1
        )
        dotgroup = VGroup()
        for x in range(-10, 10):
            for y in range(-10, 10):
                d = Dot(np.array([x/3, y/3, 0]), color=BLUE).scale(0.5)
                dotgroup.add((Intersection(d, f)))
        self.play(Create(dotgroup))
        # self.play(f.animate.become(dotgroup)) # memory leak during render
        self.wait(2)

        # solid again, rotate
        self.play(Create(g))
        self.wait(2)
        self.remove(dotgroup)
        self.remove(f)

        # velocity and acceleration
        vectors = Tex(r"$\begin{bmatrix} x \\ v \\ \theta \\ \omega \end{bmatrix}$").move_to(3*LEFT + 2*UP)
        self.play(title.animate.become(Tex(r"Vectors \\ $x$: position \\$v$: velocity \\$\theta$: rotation \\ $\omega$: angular velocity")
            .move_to(3*LEFT + DOWN)),
                  Create(vectors))
        self.wait(3)
        self.play(vectors.animate.become(Tex(r"$\begin{bmatrix} x \\ v = \frac{dx}{dt} \\ \theta \\ \omega = \frac{d\theta}{dt} \end{bmatrix}$").move_to(3*LEFT + 2*UP)))
        self.wait(3)

        # rotate around center of mass
        center_of_mass_equation = MathTex(r"\mathbf{C} &= \frac{\sum_{i}^{n}m_i \, x_i}{\sum_{i}^{n}m_i}; \\ m_i &= \text{mass of particle } i \\ x_i &= \text{position of particle } i",
                                          font_size=36).move_to(3*LEFT+DOWN)
        com = Dot(np.array([9/10, 9/10, 0]))
        self.add(com)
        self.play(title.animate.become(Tex(r"Center \\ of mass $\mathbf{C}$").move_to(5*RIGHT + 2*UP)),
                  Create(center_of_mass_equation))
        self.wait(4)

        self.play(Rotate(g, angle=2*PI, 
                         about_point=center_mass), 
                         run_time=4
        )
        self.wait(1)

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
        self.play(g.animate.scale(1/3).move_to(orbit_center_mass), 
                  title.animate.become(Tex(r"$F=ma$").move_to(3*LEFT + UP)), 
                  FadeOut(com),
                  FadeOut(center_of_mass_equation),
                  FadeOut(vectors))
        self.remove(vectors)
        self.wait(1.5)
        self.play(title.animate.become(
                      # Tex(r"$ a=\dfrac{F}{m}$ \\ ${\displaystyle v = \int a \, dt}$").move_to(3*LEFT + UP)))
                      Tex(r"$ a=\dfrac{F}{m}$ \\\vspace{0.2cm} ${\displaystyle a = \frac{dv}{dt}}$").move_to(3*LEFT + UP)))
        self.play(Create(orbit_v_vec),
                  Create(orbit_a_vec),
                  Create(orbit_v_text),
                  Create(orbit_a_text))
        for i in range(3):
            self.play(MoveAlongPath(g, orbit),
                      MoveAlongPath(orbit_v_text, orbit_v),
                      MoveAlongPath(orbit_a_text, orbit_a),
                      Rotate(orbit_v_vec, about_point=RIGHT + UP, angle=2*PI),
                      Rotate(orbit_a_vec, about_point=RIGHT + UP, angle=2*PI), 
                             rate_func=linear, run_time=5)

        # angular acceleration and torque
        self.play(title.animate.become(Tex()),
                  FadeOut(orbit_v_vec),
                  FadeOut(orbit_a_vec),
                  FadeOut(orbit_v_text),
                  FadeOut(orbit_a_text),
                  g.animate.scale(3).move_to(center),
                  Create(com))
        self.wait(3)

        # vector from center of mass to edge of body, force applied etc.
        r_vec = Arrow(start=center_mass, 
                      end=np.array([0, 3, 0]),
                      max_tip_length_to_length_ratio=0.1,
                      buff=0)
        torque_vec = Arrow(start=np.array([1, 3.429, 0]),
                           end=np.array([0, 3, 0]),
                           max_tip_length_to_length_ratio=0.1,
                           buff=0)
        # omega_equation = Tex(r"Angular velocity = ${\displaystyle \int \text{torque} \, dt}$").move_to(2.5*DOWN)
        omega_equation = Tex(r"Torque = ${\displaystyle \frac{d\, \text{(angular velocity)}}{dt}}$").move_to(2.5*DOWN)
        torque_equation = Tex(r"Angular acceleration = $\dfrac{\text{torque}}{\text{moment of inertia}}$", font_size=36).move_to(2.5*DOWN)
        self.play(Create(omega_equation))
        self.wait(2)
        self.play(# Create(r_vec),
                  Create(torque_vec),
                  omega_equation.animate.become(torque_equation))
        self.wait(2)

        self.play(omega_equation.animate.become(
                    # Tex(r"$\omega = {\displaystyle \int \tau \, dt}$ \\ $\alpha = \dfrac{T}{I}$").move_to(2.5*DOWN)))
                    Tex(r"$\tau = {\displaystyle \frac{d\omega}{dt}}$ \\\vspace{0.2cm} $\alpha = \dfrac{T}{I}$").move_to(2.7*DOWN)))
        self.wait(2)
        # spin
        #spinGroup = Group(g, r_vec, torque_vec)
        spinGroup = Group(g, torque_vec, com)
        self.play(Rotate(spinGroup, 
                         about_point=center_mass, 
                         rate_func=rate_functions.ease_in_quad,
                         angle=2*PI,
                         run_time=6))
        self.play(FadeOut(torque_vec),
                  Rotate(g,
                         about_point=center_mass,
                         rate_func=linear,
                         angle=4*PI,
                         run_time=6))

        # Summary 1
        offset = LEFT + DOWN
        f_vec_1 = Arrow(start=np.array([4, 0, 0]) + offset, 
                        end=np.array([3, 0, 0]) + offset,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0)
        f_vec_2 = Arrow(start=np.array([0, -1, 0]) + offset, 
                        end=np.array([0, 0, 0]) + offset,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0)
        f_vec_3 = Arrow(start=np.array([1, 3.429, 0]) + offset,
                        end=np.array([0, 3, 0]) + offset,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0)
        # listen it's a hack, my manim source is not meant to be high art
        f_vec_3_copy = Arrow(start=np.array([1, 3.429, 0]) + offset,
                             end=np.array([0, 3, 0]) + offset,
                             max_tip_length_to_length_ratio=0.15,
                             buff=0) 
        f_vec_1_center = f_vec_1.get_center()
        f_vec_2_center = f_vec_2.get_center()
        f_vec_3_center = f_vec_3.get_center()
        self.play(FadeOut(g, scale=0.5), 
                  FadeOut(com))
        self.play(Create(f.move_to(center + offset)), 
                  # FadeOut(torque_equation))
                  FadeOut(omega_equation))
        self.wait(2)

        self.play(Create(f_vec_1),
                  Create(f_vec_2),
                  Create(f_vec_3))
        
        self.wait(2)
                    
        state_vectors = Tex(r"Body state \\ $\begin{bmatrix} x \\ v \\ \theta \\ \omega \end{bmatrix}$", font_size=36).move_to(4*RIGHT + UP)
        textemplate = TexTemplate()
        textemplate.add_to_preamble(r"\usepackage{scalerel}")
        force_torque = Tex(r"${\displaystyle \sum F_{\scaleto{\text{on body}}{4pt}}}$", 
                           font_size=72, 
                           tex_template=textemplate).move_to(4*LEFT)
        self.play(Create(state_vectors),
                  Create(force_torque))

        self.wait(2)        
        net_force_admits = Tex(r"${\displaystyle \sum F_{\text{on body}}}$ \\ $\Big\downarrow$ \\ $\begin{bmatrix} F_{\text{net}} \\ T_{\text{net}} \end{bmatrix}$"
        ).move_to(4*LEFT)
        self.play(force_torque.animate.become(net_force_admits))
        self.wait(2)

        delta_t_update_state = Tex(r"$\xrightarrow{\qquad \Delta t \qquad}$")
        self.play(FadeOut(f),
                  FadeOut(f_vec_1),
                  FadeOut(f_vec_2),
                  FadeOut(f_vec_3),
                  force_torque.animate.move_to(2.2*LEFT + 0.7*UP),
                  state_vectors.animate.move_to(2*RIGHT),
                  Create(delta_t_update_state))
        self.wait(2)

        # net force
        f_net_vec = Arrow(start=center_mass + offset,
                          end=center_mass + offset + np.array([-2, 1-0.429, 0]),
                          max_tip_length_to_length_ratio=0.15,
                          buff=0)
        force_sum = MathTex(r"&F_{\text{net}} \\ = &\sum F_{\scaleto{\text{on body}}{4pt}}", 
                        font_size=72, 
                        tex_template=textemplate).move_to(4*LEFT + 0.5*UP)
        acc_equation = MathTex(r"a=\frac{F_{\text{net}}}{m}", 
                               font_size=72).move_to(4*LEFT + 0.5*UP)
        self.play(FadeOut(force_torque),
                  FadeOut(state_vectors),
                  FadeOut(delta_t_update_state))
        self.play(Create(f),
                  Create(f_vec_1),
                  Create(f_vec_2),
                  Create(f_vec_3),
                  Create(com.move_to(center_mass + offset)))
        self.wait(2)
        self.play(Create(force_sum),
                  f_vec_1.animate.move_to(center_mass + offset + np.array([-0.5, 0, 0])),
                  f_vec_2.animate.move_to(center_mass + offset + np.array([-1, 0.5, 0])),
                  f_vec_3.animate.move_to(center_mass + offset + np.array([-1.5, 1-0.429/2, 0])))
        self.wait(0.5)
        self.play(FadeOut(f_vec_1, scale=0.3),
                  FadeOut(f_vec_2, scale=0.3),
                  f_vec_3.animate.become(f_net_vec))
        self.wait(2)

        # net torque
        torque_sum = MathTex(r"&T_{\text{net}} \\ = &\sum T \\ = &\sum r \times F_{\scaleto{\text{on body}}{4pt}}", 
                             font_size=48, 
                             tex_template=textemplate).move_to(5*RIGHT + 0.5*UP)
        r_1_vec = Arrow(start=center_mass + offset,
                        end=offset + np.array([3, 0, 0]),
                        max_tip_length_to_length_ratio=0.15,
                        color=GOLD,
                        buff=0)
        r_2_vec = Arrow(start=center_mass + offset,
                        end=offset,
                        max_tip_length_to_length_ratio=0.15,
                        color=GOLD,
                        buff=0)
        r_3_vec = Arrow(start=center_mass + offset,
                        end=offset + np.array([0, 3, 0]),
                        max_tip_length_to_length_ratio=0.15,
                        color=GOLD,
                        buff=0)
        self.play(FadeOut(f_vec_3),
                  Create(torque_sum),
                  Create(r_1_vec),
                  Create(r_2_vec),
                  Create(r_3_vec), 
                  Create(f_vec_1.move_to(f_vec_1_center)), 
                  Create(f_vec_2.move_to(f_vec_2_center)), 
                  Create(f_vec_3_copy))
        self.wait(2)

        arc_1 = self.getTippedArc(-0.9 * 2, 0.2, center_mass + offset).set_color(RED)
        arc_2 = self.getTippedArc(-0.9 * 2, 0.35, center_mass + offset).set_color(RED)
        arc_3 = self.getTippedArc(2.486 * 2, 0.5, center_mass + offset).set_color(RED)
        arc_sum = self.getTippedArc(0.686 * 2, 0.35, center_mass + offset).set_color(RED)
        self.play(FadeOut(r_1_vec, scale=0.3),
                  Create(arc_1))
        self.play(FadeOut(r_2_vec, scale=0.3),
                  Create(arc_2))
        self.play(FadeOut(r_3_vec, scale=0.3),
                  Create(arc_3))
        self.play(FadeOut(arc_1, scale=0.3),
                  FadeOut(arc_2, scale=0.3),
                  FadeOut(arc_3, scale=0.3),
                  Create(arc_sum))
        self.wait(2)

        self.play(FadeOut(f),
                  FadeOut(force_sum),
                  FadeOut(torque_sum),
                  FadeOut(arc_sum),
                  FadeOut(f_vec_1),
                  FadeOut(f_vec_2),
                  FadeOut(f_vec_3_copy))
        self.wait(2)

















