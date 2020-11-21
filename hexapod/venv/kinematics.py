import wx
import numpy as np
from hexapod import Hexapod
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from point import Point
import time
matplotlib.use('WXAgg')


class LegDetailsFrame(wx.Frame):
    def __init__(self, leg):
        self.leg = leg
        super().__init__(parent=None, title=self.leg.name + " leg details")
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(3, 2)

        self.coxa_sizer, self.coxa_l_ctrl, self.coxa_a_ctrl = \
            self.create_leg_joint_details(panel, "Coxa", self.leg.coxa)
        self.femur_sizer, self.femur_l_ctrl, self.femur_a_ctrl = \
            self.create_leg_joint_details(panel, "Femur", self.leg.femur)
        self.tibia_sizer, self.tibia_l_ctrl, self.tibia_a_ctrl = \
            self.create_leg_joint_details(panel, "Tibia", self.leg.tibia)

        self.ctrlBind(wx.EVT_TEXT, self.coxa_l_ctrl, self.onChangeLength, self.leg.coxa)
        self.ctrlBind(wx.EVT_TEXT, self.coxa_a_ctrl, self.onChangeAngle, self.leg.coxa)

        self.ctrlBind(wx.EVT_TEXT, self.femur_l_ctrl, self.onChangeLength, self.leg.femur)
        self.ctrlBind(wx.EVT_TEXT, self.femur_a_ctrl, self.onChangeAngle, self.leg.femur)

        self.ctrlBind(wx.EVT_TEXT, self.tibia_l_ctrl, self.onChangeLength, self.leg.tibia)
        self.ctrlBind(wx.EVT_TEXT, self.tibia_a_ctrl, self.onChangeAngle, self.leg.tibia)

        sizer.Add(self.coxa_sizer, pos=(0, 0), span=(1, 1),
                  flag=wx.EXPAND | wx.TOP, border=10)
        sizer.Add(self.femur_sizer, pos=(1, 0), span=(1, 1),
                  flag=wx.EXPAND, border=10)
        sizer.Add(self.tibia_sizer, pos=(2, 0), span=(1, 1),
                  flag=wx.EXPAND | wx.BOTTOM, border=10)
        sizer.AddGrowableCol(0)
        panel.SetSizer(sizer)
        sizer.Fit(self)
        self.Show()

    def create_leg_joint_details(self, parent, name, joint):
        sb = wx.StaticBox(parent, label=name)
        sbsizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        vbox_l = wx.BoxSizer(wx.VERTICAL)
        vbox_a = wx.BoxSizer(wx.VERTICAL)
        txt_l = wx.StaticText(parent, label="Length")
        ctrl_l = wx.TextCtrl(parent)
        ctrl_l.SetValue(str(joint.length))

        vbox_l.Add(txt_l, 0, wx.ALL | wx.EXPAND, 2)
        vbox_l.Add(ctrl_l, 0, wx.ALL | wx.EXPAND, 2)
        txt_a = wx.StaticText(parent, label="Angle")
        ctrl_a = wx.TextCtrl(parent)
        ctrl_a.SetValue(str(joint.angle))
        vbox_a.Add(txt_a, 0, wx.ALL | wx.EXPAND, 2)
        vbox_a.Add(ctrl_a, 0, wx.ALL | wx.EXPAND, 2)
        sbsizer.Add(vbox_a, flag=wx.LEFT, border=5)
        sbsizer.Add(vbox_l, border=5)
        return sbsizer, ctrl_l, ctrl_a

    def onChangeLength(self, event, *args):
        args[0].length = event.GetEventObject().GetValue()

    def onChangeAngle(self, event, *args):
        args[0].angle = event.GetEventObject().GetValue()

    def ctrlBind(self, t, instance, handler, *args, **kwargs):
        self.Bind(t, lambda event: handler(event, *args, **kwargs), instance)


class MyFrame(wx.Frame):
    def __init__(self, _hexapod):
        self._hexapod = _hexapod
        super().__init__(parent=None, title='Hexapod')
        panel = wx.Panel(self)


        modelFig = Figure(figsize=(4, 3), dpi=100)
        self.modelCanvas = FigureCanvas(panel, -1, modelFig)

        self.a = modelFig.add_subplot(111, projection='3d')
        self.a.set_autoscale_on(False)

        # Create sizer
        Topstaticbox = wx.StaticBox(panel, -1, 'Robot Model')
        Topstaticboxsizer = wx.StaticBoxSizer(Topstaticbox, wx.HORIZONTAL)

        rotvbox = wx.BoxSizer(wx.VERTICAL)

        pitchhbox = wx.BoxSizer(wx.HORIZONTAL)
        pitchPlus = wx.Button(panel, -1, 'P+')
        pitchMinus = wx.Button(panel, -1, 'P-')
        pitchPlus.Bind(wx.EVT_BUTTON, self.pitchButtonPlus)
        pitchMinus.Bind(wx.EVT_BUTTON, self.pitchButtonMinus)
        pitchhbox.Add(pitchPlus, 0, wx.ALL | wx.LEFT, 2)
        pitchhbox.Add(pitchMinus, 0, wx.ALL | wx.RIGHT, 2)

        rollhbox = wx.BoxSizer(wx.HORIZONTAL)
        rollPlus = wx.Button(panel, -1, 'R+')
        rollMinus = wx.Button(panel, -1, 'R-')
        rollPlus.Bind(wx.EVT_BUTTON, self.rollButtonPlus)
        rollMinus.Bind(wx.EVT_BUTTON, self.rollButtonMinus)
        rollhbox.Add(rollPlus, 0, wx.ALL | wx.LEFT, 2)
        rollhbox.Add(rollMinus, 0, wx.ALL | wx.RIGHT, 2)

        yawhbox = wx.BoxSizer(wx.HORIZONTAL)
        yawPlus = wx.Button(panel, -1, 'Y+')
        yawMinus = wx.Button(panel, -1, 'Y-')
        yawPlus.Bind(wx.EVT_BUTTON, self.yawButtonPlus)
        yawMinus.Bind(wx.EVT_BUTTON, self.yawButtonMinus)
        yawhbox.Add(yawPlus, 0, wx.ALL | wx.LEFT, 2)
        yawhbox.Add(yawMinus, 0, wx.ALL | wx.RIGHT, 2)

        transxhbox = wx.BoxSizer(wx.HORIZONTAL)
        transxPlus = wx.Button(panel, -1, 'X+')
        transxMinus = wx.Button(panel, -1, 'X-')
        transxPlus.Bind(wx.EVT_BUTTON, self.transxButtonPlus)
        transxMinus.Bind(wx.EVT_BUTTON, self.transxButtonMinus)
        transxhbox.Add(transxPlus, 0, wx.ALL | wx.LEFT, 2)
        transxhbox.Add(transxMinus, 0, wx.ALL | wx.RIGHT, 2)

        transyhbox = wx.BoxSizer(wx.HORIZONTAL)
        transyPlus = wx.Button(panel, -1, 'Y+')
        transyMinus = wx.Button(panel, -1, 'Y-')
        transyPlus.Bind(wx.EVT_BUTTON, self.transyButtonPlus)
        transyMinus.Bind(wx.EVT_BUTTON, self.transyButtonMinus)
        transyhbox.Add(transyPlus, 0, wx.ALL | wx.LEFT, 2)
        transyhbox.Add(transyMinus, 0, wx.ALL | wx.RIGHT, 2)

        transzhbox = wx.BoxSizer(wx.HORIZONTAL)
        transzPlus = wx.Button(panel, -1, 'Z+')
        transzMinus = wx.Button(panel, -1, 'Z-')
        transzPlus.Bind(wx.EVT_BUTTON, self.transzButtonPlus)
        transzMinus.Bind(wx.EVT_BUTTON, self.transzButtonMinus)
        transzhbox.Add(transzPlus, 0, wx.ALL | wx.LEFT, 2)
        transzhbox.Add(transzMinus, 0, wx.ALL | wx.RIGHT, 2)

        # Add canvas to static box sizer
        Topstaticboxsizer.Add(self.modelCanvas, 0, wx.EXPAND)
        #
        rotvbox.Add(rollhbox, 0, wx.ALL | wx.LEFT, 10)
        rotvbox.Add(pitchhbox, 0, wx.ALL | wx.LEFT, 10)
        rotvbox.Add(yawhbox, 0, wx.ALL | wx.LEFT, 10)

        rotvbox.Add(transxhbox, 0, wx.ALL | wx.LEFT, 10)
        rotvbox.Add(transyhbox, 0, wx.ALL | wx.LEFT, 10)
        rotvbox.Add(transzhbox, 0, wx.ALL | wx.LEFT, 10)

        Topstaticboxsizer.Add(rotvbox, 0, wx.ALL | wx.LEFT, 10)
        panel.SetSizer(Topstaticboxsizer)
        Topstaticboxsizer.SetSizeHints(self)


        self.create_menu()
        self.Show()
        self.update_plot()

    def pitchButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dp=1)
        self.update_plot()

    def pitchButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dp=-1)
        self.update_plot()

    def rollButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dr=1)
        self.update_plot()

    def rollButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dr=-1)
        self.update_plot()

    def yawButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dy=1)
        self.update_plot()

    def yawButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(0, 0, 0), dy=-1)
        self.update_plot()

    def transxButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(1, 0, 0))
        self.update_plot()

    def transxButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(-1, 0, 0))
        self.update_plot()

    def transyButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(0, 1, 0))
        self.update_plot()

    def transyButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(0, -1, 0))
        self.update_plot()

    def transzButtonPlus(self, event):
        # self._hexapod.roll += 0.1
        self._hexapod.update_configuration(Point(0, 0, 1))
        self.update_plot()

    def transzButtonMinus(self, event):
        # self._hexapod.roll -= 0.1
        self._hexapod.update_configuration(Point(0, 0, -1))
        self.update_plot()

    def prepare_body_plot(self, body):
        x_list = []
        y_list = []
        z_list = []
        for segment in body.corners:
            x, y, z = segment[0].get_coordinates()
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        # close body
        x_list.append(x_list[0])
        y_list.append(y_list[0])
        z_list.append(z_list[0])
        return x_list, y_list, z_list

    def prepare_leg_plot(self, leg):
        x_list = []
        y_list = []
        z_list = []
        for segment in leg.joints_origin:
            x, y, z = segment.get_coordinates()
            x_list.append(x)
            y_list.append(y)
            z_list.append(z)
        return x_list, y_list, z_list

    def update_plot(self):
        print("update")
        self.a.clear()
        self.a.set_xlim3d(-40, 40)
        self.a.set_ylim3d(-40, 40)
        self.a.set_zlim3d(0, 30)
        self.a.set_autoscale_on(False)
        x_body, y_body, z_body = self.prepare_body_plot(self._hexapod.body)
        self.a.plot(x_body, y_body, z_body, color="red", linewidth=4)
        self.a.scatter(x_body, y_body, z_body, s=20, marker="o")

        for l in self._hexapod.legs:
            x_legs = []
            y_legs = []
            z_legs = []
            x_leg, y_leg, z_leg = self.prepare_leg_plot(l)
            for x, y, z in zip(x_leg, y_leg, z_leg):
                x_legs.append(x)
                y_legs.append(y)
                z_legs.append(z)
            self.a.plot(x_legs, y_legs, z_legs, color="green", linewidth=4)
            self.a.scatter(x_legs, y_legs, z_legs, s=20, marker="o")
        self.modelCanvas.draw()

    def create_menu(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        mechanics_leg_1 = file_menu.Append(
            wx.ID_ANY, 'Leg 1',
            'Show leg 1 details'
        )
        mechanics_leg_2 = file_menu.Append(
            wx.ID_ANY, 'plot1',
            'Show leg 1 details'
        )
        menu_bar.Append(file_menu, 'Mechanics')
        self.Bind(
            event=wx.EVT_MENU,
            handler=lambda event: self.show_details(self._hexapod.legs[0]),
            source=mechanics_leg_1,
        )
        self.Bind(
            event=wx.EVT_MENU,
            handler=lambda event: self.plot(),
            source=mechanics_leg_2,
        )
        self.SetMenuBar(menu_bar)

    def show_details(self, _leg):
        LegDetailsFrame(_leg)

    def plot(self):
        c = CanvasFrame()
        c.Show()


class CanvasFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,
                          'CanvasFrame', size=(550, 350))

        self.figure = Figure(figsize=(5, 4), dpi=100)
        fig = plt.figure()
        self.axes(projection='3d')
        self.axes = self.figure.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)

        self.axes.plot(t, s)

        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)

        # update the axes menu on the toolbar
        self.SetSizer(self.sizer)
        self.Fit()


if __name__ == '__main__':
    _hexapod = Hexapod()
    app = wx.App()
    frame = MyFrame(_hexapod)
    app.MainLoop()



