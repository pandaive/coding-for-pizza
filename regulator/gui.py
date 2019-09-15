import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Bosch App')
        panel = wx.Panel(self)

        self.dig_ctrl_trun = wx.TextCtrl(panel, pos=(5, 5))
        my_btn = wx.Button(panel, label='TURN', pos=(5, 40))


        my_btn = wx.Button(panel, label='STOP', pos=(5, 65))

        self.dig_ctrl_speed = wx.TextCtrl(panel, pos=(5, 100))
        my_btn = wx.Button(panel, label='SPEED', pos=(5, 140))

        self.dig_ctrl_pause = wx.TextCtrl(panel, pos=(5, 180))
        my_btn = wx.Button(panel, label='PAUSE', pos=(5, 220))

        my_btn = wx.Button(panel, label='BASE', pos=(5, 255))

        self.Show()
        #if int(self.dig_ctrl.GetValue())
        '''
        def on_press(self, event):
            value = int(self.dig_ctrl.GetValue())
                if not value:
                    print("You didn't enter anything!")
                else:
                    print(f'You typed: "{value}"')
        '''


    def read(self, event):
        try:
            var = int(self.dig_ctrl.GetValue())
            wx.MessageDialog(self, "You entered %s" % var, "Number entered", wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            wx.MessageDialog(self, "Enter a number", "Warning!", wx.OK | wx.ICON_WARNING).ShowModal()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()