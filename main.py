import wx
import wx.grid
from gestProd import gestProd
def getProduct():
    return 'soy un prouducto'

class appGestion(wx.Frame):
    def __init__(self,*args,**kw):
        super().__init__(*args,**kw)
        self.mainPanel = wx.Panel(self)
        #Menu Bar
        self.init_menu_bar()
        #Grid
        self.init_grid_data()

        #Add Product
        self.add_product_button = wx.Button(self, label='Agregar Producto')
        self.add_product_button.Bind(wx.EVT_BUTTON, self.on_add_product)

        #Delete Product
        self.delete_product_button = wx.Button(self, label='Quitar Producto')
        self.delete_product_button.Bind(wx.EVT_BUTTON, self.on_delete_product)

        #View
        self.main_sizer_horz = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer_horz.Add(self.add_product_button, 0, wx.ALL, 10)
        self.main_sizer_horz.Add(self.delete_product_button, 0, wx.ALL, 10)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.mainGrid, 1, wx.EXPAND)
        self.mainSizer.Add(self.main_sizer_horz,0,wx.EXPAND|wx.ALL,5)
        self.SetSizerAndFit(self.mainSizer)

        #View Size
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_add_product(self,event):
        #Abrir ventana que busque productos
        prod=getProduct()
        self.mainGrid.AppendRows(1)
        for i in range(self.mainGrid.GetNumberCols()):
            self.mainGrid.SetCellValue(self.mainGrid.GetNumberRows()-1,i,prod[i])

    def on_delete_product(self,event):
        selected_rows=self.mainGrid.GetSelectedRows()
        if selected_rows:
            selected_row= selected_rows[0]
            self.mainGrid.DeleteRows(selected_row)
        else:
            print('SELECCIONA UNA FILA')
    def on_size(self,event):
        new_size = self.GetSize().GetWidth()
        num_columns = self.mainGrid.GetNumberCols()
        
        font = wx.Font(int(new_size*0.015), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        row_height = font.GetPixelSize()[1]+4
        column_width = new_size // (num_columns+1)

        self.mainGrid.SetDefaultCellFont(font)
        self.mainGrid.SetDefaultRowSize(row_height)
        self.mainGrid.SetDefaultColSize(column_width)
        self.mainGrid.Refresh()

        event.Skip()

    def init_grid_data(self):

        self.mainGrid=wx.grid.Grid(self)

        self.mainGrid.CreateGrid(0, 5)
        self.mainGrid.SetColLabelValue(0, 'ID')
        self.mainGrid.SetColLabelValue(1, 'NOMBRE')
        self.mainGrid.SetColLabelValue(2, 'PRECIO')
        self.mainGrid.SetColLabelValue(3, 'CANTIDAD')
        self.mainGrid.SetColLabelValue(4, 'SUBTOTAL')


    def init_menu_bar(self):
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        
        open_menu_item = file_menu.Append(wx.ID_OPEN, 'Open\tCtrl+F', 'Open a file')
        self.Bind(wx.EVT_MENU, self.on_open, open_menu_item)
        
        menubar.Append(file_menu, 'File')
        self.SetMenuBar(menubar)
    
    def on_open(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', '', '', '*.*', wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = dlg.GetPath()
            grid_frame = gestProd(self, "Product Data", file_path)
            grid_frame.Center()
            grid_frame.Show()
        dlg.Destroy()

    

    

if __name__=='__main__':
    app=wx.App()
    gestion=appGestion(None,title="Sistema de Gestion",size=(500,600), style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX)
    gestion.Center()
    gestion.Show()
    app.MainLoop()






# app = wx.App(False)
# frame = wx.Frame(None,title="Sistema de Gestion",size=(800,600), style=wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX)

# Template_ID= wx.Window.NewControlId()

# barra_menu = wx.MenuBar()
# menu_archivo=wx.Menu()
# #\tCtrl+G sirve para crear un Shortcut
# menu_archivo.Append(Template_ID,'Template Menu\tCtrl+G','Descripcion')
# menu_archivo.AppendSeparator()
# menu_archivo.Append(wx.ID_SAVE)
# #& sirve para establecer un acceso directo para cuando presionamos Alt, el & puede estar ubicado antes de la letra que queremos sea el acceso directo.
# barra_menu.Append(menu_archivo,'&Template')
# frame.SetMenuBar(barra_menu)
# # toolbar=wx.ToolBar()
# # toolbar.AddTool()

# panel = wx.Panel(frame)
# panel.SetBackgroundColour((255,155,100))

# #Control Text
# static_text = wx.StaticText(panel,label ='Hola')

# frame.SetIcon(wx.Icon('icono.ico'))
# frame.Center()
# frame.Show(True)
# app.MainLoop()