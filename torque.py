import math
from manim import *

class TorqueDemo(Scene):


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
        com = Dot(np.array([9/10, 9/10, 0]))
        # f_vec_3 = Arrow(start=np.array([1, 3.429, 0]) + offset,
        #                 end=np.array([0, 3, 0]) + offset,
        #                 max_tip_length_to_length_ratio=0.15,
        #                 buff=0)
        r_3_vec = Arrow(start=center_mass + offset,
                        end=offset + np.array([0, 3, 0]),
                        max_tip_length_to_length_ratio=0.15,
                        color=GOLD,
                        buff=0)
        f_vec_3 = Arrow(start=np.array([1, 3.429, 0]) + offset,
                        end=np.array([0, 3, 0]) + offset,
                        max_tip_length_to_length_ratio=0.15,
                        buff=0)
        r_3_tip = np.array([0, 2 + 0.429/2, 0])

        self.play(Create(f.move_to(center + offset)),
                  Create(r_3_vec),
                  Create(f_vec_3),
                  Create(com.move_to(center_mass + offset)))
        self.bring_to_front(f_vec_3)
        self.wait(1)

        self.play(FadeOut(f, scale=0.3),
                  # f_vec_3.animate.move_to(center_mass + offset + np.array([-0.5, -0.429/2, 0])))
                  f_vec_3.animate.move_to(center_mass + offset + np.array([-1.4, 1.82, 0])))
        vecGroup = Group(com, f_vec_3, r_3_vec)

        angle_tracker = ValueTracker(PI/2)
        f_tracker = ValueTracker(math.sqrt(1+0.429**2))
        base_angle = 2.486

        arc = Arc(radius=1, start_angle=PI/2, 
                  angle=base_angle * f_tracker.get_value(), arc_center=RIGHT, 
                  stroke_width=4, color=GOLD)
        arc.add_tip(tip_length=0.06)
        label = Tex(r"Torque $=r \times F$").move_to(RIGHT + 2*UP)
        self.play(vecGroup.animate.move_to(2*LEFT+DOWN).rotate(math.atan(-0.429), about_point=com.get_center()),
                  Create(arc), 
                  Create(label))
        self.play(Create(Dot(2*LEFT+DOWN + np.array([0.23, 1.77, 0]))))
        self.wait(1)
        arc.add_updater(lambda x: x.become(
                Arc(radius=1, start_angle=PI/2, 
                    angle=base_angle * math.sin(angle_tracker.get_value()) 
                                     * f_tracker.get_value(),
                    arc_center=RIGHT, stroke_width=4, color=GOLD).add_tip(tip_length=0.06)
            )
        )
        f_vec_3.add_updater(lambda x: x.become(
                # Arrow(start=com.get_center(), 
                #       end=com.get_center() + np.array([f_tracker.get_value() 
                #                                   * -math.sin(angle_tracker.get_value()), 
                #                                      f_tracker.get_value() 
                #                                   *  math.cos(angle_tracker.get_value()), 0]), 
                Arrow(start=com.get_center() + r_3_tip, 
                      end=com.get_center() + np.array([f_tracker.get_value() 
                                                  * -math.sin(angle_tracker.get_value()), 
                                                     f_tracker.get_value() 
                                                  *  math.cos(angle_tracker.get_value()), 0])
                                           + r_3_tip, 
                      max_tip_length_to_length_ratio=0.15,
                      buff=0)
            )
        )
        self.bring_to_front(f_vec_3)

        self.play(angle_tracker.animate.set_value(PI/4)),
        self.wait(1)
        self.play(f_tracker.animate.set_value(2)),
        self.wait(2)
        self.play(f_tracker.animate.set_value(1)),
        self.play(angle_tracker.animate.set_value(PI/2), run_time=2)
        self.play(angle_tracker.animate.set_value(PI), run_time=2)
        self.wait(1)
        self.play(angle_tracker.animate.set_value(PI/2), run_time=1.5)
        self.play(angle_tracker.animate.set_value(0), run_time=1.5)
        self.wait(0.5)
        self.play(angle_tracker.animate.set_value(5*PI/6), 
                  f_tracker.animate.set_value(2.5), run_time=5)
        self.wait(3)










