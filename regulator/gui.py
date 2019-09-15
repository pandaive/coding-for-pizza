import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Bosch App')
        panel = wx.Panel(self)

        self.dig_ctrl_turn = wx.TextCtrl(panel, pos=(5, 5))
        x = int(self.dig_ctrl_turn.GetValue())
            if x >= 0:
                subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "right"])
            elif x == 0:
                subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "zero"])
            else : 
                    subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "left"])
                  
        my_btn = wx.Button(panel, label='TURN', pos=(5, 40))

        my_btn = wx.Button(panel, label='STOP', pos=(5, 65))
            subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "move", "-m", "zero"])

        self.dig_ctrl_speed = wx.TextCtrl(panel, pos=(5, 100))
        y = self.dig_ctrl_speed
        while y in range(0,50):
            subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "freq", "-m", y])
        my_btn = wx.Button(panel, label='SPEED', pos=(5, 140))

        self.dig_ctrl_pause = wx.TextCtrl(panel, pos=(5, 180))
        z = self.dig_ctrl_speed
        while z in range(0,50):
            subprocess.run(["mosquitto_pub", "-h", "192.168.0.1", "-t", "freq", "-m", "stop"])
            time.sleep(z/1000)
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
