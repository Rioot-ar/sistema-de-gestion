import wx
import wx.grid

import csv

class gestProd(wx.Frame):
    def __init__(self, parent, title, path):
        super(gestProd,self).__init__(parent,title=title, size=(800,600))
        self.panel = wx.Panel(self)
        self.text_ctrl = wx.TextCtrl(self.panel)
        self.path=path

        self.grid=wx.grid.Grid(self.panel)
        self.grid.CreateGrid(0, 0)
        self.grid.SetRowLabelSize(0)

        self.search_button_id = wx.Button(self.panel, label='Buscar ID')
        self.search_button_id.Bind(wx.EVT_BUTTON, self.on_search_id)

        self.search_button_product = wx.Button(self.panel, label='Buscar Producto')
        self.search_button_product.Bind(wx.EVT_BUTTON, self.on_search_product)

        self.save_button_product = wx.Button(self.panel, label='Guardar')
        self.save_button_product.Bind(wx.EVT_BUTTON, self.on_save)

        self.Bind(wx.EVT_SIZE, self.on_size)

        self.load_csv(path)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.grid, 1, wx.EXPAND)
        self.sizer.Add(self.text_ctrl, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self.sizer_horz = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_horz.Add(self.search_button_id, 0, wx.ALL, 10)
        self.sizer_horz.Add(self.search_button_product, 0, wx.ALL, 10)
        self.sizer_horz.Add(self.save_button_product, 0, wx.ALL, 10)

        self.sizer.Add(self.sizer_horz,0,wx.EXPAND|wx.ALL,5)
        self.panel.SetSizerAndFit(self.sizer)

    def on_size(self,event):
        new_size = self.GetSize().GetWidth()
        num_columns = self.grid.GetNumberCols()
        
        font = wx.Font(int(new_size*0.015), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        row_height = font.GetPixelSize()[1]+4
        column_width = new_size // (num_columns+1)

        self.grid.SetDefaultCellFont(font)
        self.grid.SetDefaultRowSize(row_height)
        self.grid.SetDefaultColSize(column_width)
        self.grid.Refresh()

        event.Skip()

    def on_save(self,event):
         with open(self.path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            headers = [self.grid.GetColLabelValue(col) for col in range(self.grid.GetNumberCols())]
            writer.writerow(headers)
            
            for row in range(self.grid.GetNumberRows()):
                row_data = [self.grid.GetCellValue(row, col) for col in range(self.grid.GetNumberCols())]
                if any(value.strip() != '' for value in row_data):
                    writer.writerow(row_data)
                else:
                    break
    
    def on_search_id(self, event):
        search_id = self.text_ctrl.GetValue()
        if search_id.isdigit():
            for row in range(self.grid.GetNumberRows()):
                if(self.grid.GetCellValue(row, 0)==search_id):
                    self.grid.SelectRow(row)
                    break
            else:
                wx.MessageBox('No se encontró el ID {}'.format(search_id), 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Ingrese un ID válido', 'Error', wx.OK | wx.ICON_ERROR)    

    def findRowBy(self,colName):
        for col in range(self.grid.GetNumberCols()):
            if(colName==self.grid.GetColLabelValue(col)):
                return col
        return -1
    
    def on_search_product(self, event):
        search_prod=self.text_ctrl.GetValue()
        column=self.findRowBy('NOMBRE')
        if (search_prod.isalpha() and column!=-1):
            for row in range(self.grid.GetNumberRows()):
                if(self.grid.GetCellValue(row, column)==search_prod):
                    self.grid.SelectRow(row)
                    break
            else:
                wx.MessageBox('No se encontró el Producto {}'.format(search_prod), 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Ingrese un producto válido', 'Error', wx.OK | wx.ICON_ERROR)

        
    def load_csv(self, file_path):

        self.grid.ClearGrid()
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for col_index, col_name in enumerate(header):
                self.grid.AppendCols(1)
                self.grid.SetColLabelValue(col_index, col_name)

            for row_index, row in enumerate(reader):
                for col, value in enumerate(row):
                    self.grid.AppendRows(1)
                    self.grid.SetCellValue(row_index, col, value)
        
                    
                
