import wx
import wx.grid
import csv
import copy
from gestProd import gestProd

def getProducts(file_path):
    prodDict=list()
    with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                prodDict.append({
                    'id':row[0],
                    'precio':row[1],
                    'nombre':row[2]
                })
    return prodDict

def saveDetailsCSV(filpath,details):
         with open(filpath, 'a', newline='') as file:
            writer = csv.writer(file)
            for i,detail in enumerate(details):
                writer.writerow([detail['id'],detail['cantidad'],detail['subtotal'],detail['producto'],detail['venta']])

            file.close()
    



##########################################################################
### Nota importante, el -1 en todos los contadores de las filas es la  ###
### solucion magica para la siempre fila vacia que se usa como         ###
### auxiliar a la hora de ingresar productos, se cambiara en un futuro ###
###                          (lejano)                                  ###
##########################################################################


class appGestion(wx.Frame):
    def __init__(self,parent,title):
        super().__init__(parent,title=title)
        self.mainPanel = wx.Panel(self)
        self.products=getProducts("productos.csv")
        self.salesDetail=list()
        self.numberDetails=0
        self.numberSells=0
        #Menu Bar
        self.init_menu_bar()
        #Grid
        self.mainGrid=wx.grid.Grid(self.mainPanel)
        self.init_grid_data()

        #Text Total
        self.totalAmmount=0
        self.totalText= wx.StaticText(self.mainPanel,label=f'Total {self.totalAmmount}')
        

        #Pay
        self.pay_button=wx.Button(self.mainPanel, label='Pagar')
        self.pay_button.Bind(wx.EVT_BUTTON, self.on_pay)

        #Editing Cell
        self.mainGrid.Bind(wx.grid.EVT_GRID_CELL_CHANGING, self.on_cell_change)

        #Delete Product
        self.delete_text_ctrl = wx.TextCtrl(self.mainPanel)
        self.delete_product_button = wx.Button(self.mainPanel, label='Quitar Producto')
        self.delete_product_button.Bind(wx.EVT_BUTTON, self.on_delete_product)

        #View
        self.horSizer=wx.BoxSizer()
        self.horSizer.Add(self.delete_text_ctrl,10,flag=wx.EXPAND)
        self.horSizer.Add(self.delete_product_button,2,flag=wx.ALIGN_BOTTOM)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.mainGrid,20,flag=wx.EXPAND)
        self.mainSizer.Add(self.totalText,3,flag=wx.RIGHT|wx.EXPAND)
        self.mainSizer.Add(self.pay_button,3,flag=wx.EXPAND)
        self.mainSizer.Add(self.horSizer,1,flag=wx.ALIGN_CENTER)
        self.mainPanel.SetSizerAndFit(self.mainSizer)
        #View Size
        self.Bind(wx.EVT_SIZE, self.on_size)

        #Close Event
        self.Bind(wx.EVT_CLOSE,self.on_close)

    def totalTextRefresh(self):
        self.totalAmmount=0
        for row in range(self.mainGrid.GetNumberRows()-1):
            subtotal=self.mainGrid.GetCellValue(row,4)
            if subtotal=='':
                continue
            subtotal=float(subtotal)
            self.totalAmmount+=subtotal
        self.totalText.SetLabel(f'Total {self.totalAmmount}')

    def on_pay(self,event):
        #NumberEntryDialog solo admite enteros como entrada, por el momento se mantendra asi. Cambiar en el futuro(cercano)
        entryPayDialog = wx.NumberEntryDialog(self.mainPanel, 'Ingresa un monto:', 'Pago', "Abonado por el Cliente",0,0,99999999)
        entryPayDialog.SetSize((400,200))
        if entryPayDialog.ShowModal() == wx.ID_OK and entryPayDialog.GetValue()>= self.totalAmmount:
            payment = entryPayDialog.GetValue()
        else:
            dialogError=wx.MessageDialog(self.mainPanel,'El pago no puede ser menor al total','Ingrese un monto valido')
            dialogError.ShowModal()
            dialogError.Destroy()
            entryPayDialog.Destroy()
            return
        entryPayDialog.Destroy()

        change=payment-self.totalAmmount
        dialogChange=wx.MessageDialog(self.mainPanel,f'El vuelto es de ${change}','Vuelto')
        dialogChange.ShowModal()
        dialogChange.Destroy()
        self.saveSalesDetail()
        self.mainGrid.ClearGrid()
        self.mainGrid.DeleteRows(numRows=self.mainGrid.GetNumberRows()-1)
        self.totalTextRefresh()


    def saveSalesDetail(self):
        self.numberSells+=1
        for row in range(self.mainGrid.GetNumberRows()-1):
            self.numberDetails+=1
            self.salesDetail.append({
                'id':self.numberDetails,
                'cantidad':self.mainGrid.GetCellValue(row,3),
                'subtotal':self.mainGrid.GetCellValue(row,4),
                'producto':self.mainGrid.GetCellValue(row,0),
                'venta':self.numberSells
            })

    def on_close(self,event):
        if wx.MessageBox("Se cerrara el programa", "desea guardar los datos?",wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
            event.Veto()
            return
        saveDetailsCSV('detalles.csv',self.salesDetail)
        event.Skip()

    def on_cell_change(self,event):
        row = event.GetRow()
        col = event.GetCol()
        match col:
            case 0:
                prodAdd = self.getProduct(event.GetString(),'id')
            case 1:
                prodAdd = self.getProduct(event.GetString(),'nombre')
            case 3:
                prodAdd='invalido'
                self.mainGrid.SetCellValue(row,3,event.GetString())
                self.mainGrid.SetCellValue(row,4,str(float(self.mainGrid.GetCellValue(row,2))*float(event.GetString())))
                self.totalTextRefresh()
                #descubrir porque no se selecciona la primera columna de la ultima fila,
                #posibles causas: mal manejo de eventos, Vetos, Skips
                self.mainGrid.SetGridCursor(row+1,0)
        
        if prodAdd=='invalido':
            return
        prodAdd['precio']=prodAdd['precio'].replace('.','')
        prodAdd['precio']=prodAdd['precio'].replace(',','.')
        self.mainGrid.SetCellValue(row,0,prodAdd['id'])
        self.mainGrid.SetCellValue(row,1,prodAdd['nombre'])
        self.mainGrid.SetCellValue(row,2,prodAdd['precio'])
        self.mainGrid.SetGridCursor(row,3)
        self.mainGrid.AppendRows(1)

    def getRowById(self,rowId):
        for i in range(self.mainGrid.GetNumberRows()):
            if self.mainGrid.GetCellValue(i,0) == rowId:
                return i
            
        return -1
    
    def on_delete_product(self,event):
        rowId=self.delete_text_ctrl.GetValue() 
        selected_row=self.getRowById(rowId) if rowId != '' else -1
        if selected_row!=-1:
            self.mainGrid.DeleteRows(selected_row)
            self.totalTextRefresh()
        else:
            print('SELECCIONA UNA FILA')
    
    def on_size(self,event):
        new_size = self.GetSize().GetWidth()
        num_columns = self.mainGrid.GetNumberCols()

        font = wx.Font(int(new_size*0.015), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        row_height = font.GetPixelSize()[1]+4
        column_width = new_size // (num_columns)

        self.totalText.SetFont(font)
        self.delete_text_ctrl.SetFont(font)

        self.pay_button.SetFont(font)

        self.mainGrid.SetDefaultCellFont(font)
        self.mainGrid.SetDefaultRowSize(row_height)
        self.mainGrid.SetDefaultColSize(column_width)
        self.mainGrid.Refresh()

        event.Skip()

    def getProduct(self,prod,nameColumn):
        for producto in self.products:
            if producto[nameColumn]==prod:
                prod=copy.copy(producto)
                return prod
        return 'invalido'




    def init_grid_data(self):

        self.mainGrid.ClearGrid()
        self.mainGrid.CreateGrid(1, 5)
        self.mainGrid.SetRowLabelSize(0)
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
        dlgFile = wx.FileDialog(self, 'Choose a file', '', '', '*.*', wx.FD_OPEN)
        if dlgFile.ShowModal() == wx.ID_OK:
            file_path = dlgFile.GetPath()
            grid_frame = gestProd(self, "Product Data", file_path)
            grid_frame.Center()
            grid_frame.Show()
        dlgFile.Destroy()
    

    

if __name__=='__main__':
    app=wx.App()
    gestion=appGestion(None,title="Sistema de Gestion")
    gestion.Centre()
    gestion.Show()
    app.MainLoop()
