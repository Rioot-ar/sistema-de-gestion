import wx
import wx.grid

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.grid = wx.grid.Grid(self)  # Crea el grid
        self.grid.CreateGrid(0, 5)  # Crea el grid con 5 columnas
        self.grid.SetColLabelValue(0, "Columna 1")
        self.grid.SetColLabelValue(1, "Columna 2")
        self.grid.SetColLabelValue(2, "Columna 3")
        self.grid.SetColLabelValue(3, "Columna 4")
        self.grid.SetColLabelValue(4, "Columna 5")
        
        self.mainSizer.Add(self.grid, 1, wx.EXPAND)  # Agrega el grid al sizer
        self.SetSizer(self.mainSizer)  # Asocia el sizer con la ventana
        
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None, "Grid con 5 columnas")
    app.MainLoop()