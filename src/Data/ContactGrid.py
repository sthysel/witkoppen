# bplate


from wx.grid import *
import copy
import Colors

from TMWidgets.TMGrid import TMGrid

colLabels = ["Contact Type", "Number"]

defrow = ["Patient Cell", ""]

class DataTable(PyGridTableBase):
    "Filter Data"
    def __init__(self):

        PyGridTableBase.__init__(self)

        # key str
        self.dataTypes = [
            #GRID_VALUE_CHOICE+':Patient Cell,Spouce Cell,Next of Kin Cell,Father Cell,Mother Cell,Work Land Line, Home Land LIne',
            GRID_VALUE_STRING,
            GRID_VALUE_STRING
            ]
        
        self.data = []

    def GetNumberRows(self):
        if not self.data: return 0
        return len(self.data)

    def GetNumberCols(self):
        return len(colLabels)

    def IsEmptyCell(self, row, col):
        
        if not self.data: return True        
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        """ Get/Set values in the table.  The Python version of these
        methods can handle any data-type, (as long as the Editor and
        Renderer understands the type too,)"""
        
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        try:
            self.data[row][col] = value
        except IndexError:
            # add a new row
            self.data.append([''] * self.GetNumberCols())
            self.SetValue(row, col, value)

            # tell the grid we've added a row
            msg = GridTableMessage(self,                             # The table
                                   GRIDTABLE_NOTIFY_ROWS_APPENDED,   # what we did to it
                                   1)                                # how many
            
            self.GetView().ProcessTableMessage(msg)

    def SetData(self, data):
        """ set the data"""

        self.data = data
        if not data: return
        
        msg = GridTableMessage(self,                             # The table
                               GRIDTABLE_NOTIFY_ROWS_APPENDED,   # what we did to it
                               len(data))                        # how many
        
        self.GetView().ProcessTableMessage(msg)

    def AddData(self, data):
        """ add data to the current list"""

        cnt = 0
        for e in data:
            if e not in self.data:
                self.data.append(e)
                cnt = cnt + 1
                
        msg = GridTableMessage(self, GRIDTABLE_NOTIFY_ROWS_APPENDED, cnt)        
        self.GetView().ProcessTableMessage(msg)



    def GetColLabelValue(self, col):
        """ Called when the grid needs to display labels """
        return colLabels[col]

    def GetTypeName(self, row, col):
        """ Called to determine the kind of editor/renderer to use by
        default, doesn't necessarily have to be the same type used
        natively by the editor/renderer if they know how to convert. """

        return self.dataTypes[col]

    def CanGetValueAs(self, row, col, typeName):
        """ Called to determine how the data can be fetched and stored by the
        editor and renderer.  This allows you to enforce some type-safety
        in the grid. """

        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)

    def DeleteRows(self, row, num=1):
        """ overide """

        try:
            self.data.pop(row)
            msg = GridTableMessage(self,                             
                                   GRIDTABLE_NOTIFY_ROWS_DELETED,
                                   row,
                                   num)                              
            self.GetView().ProcessTableMessage(msg)
        except IndexError:
            pass


    def InsertRows(self, row, num=1):
        """ overide """

        try:
            self.data.insert(row, copy.copy(defrow))
            msg = GridTableMessage(self,                             
                                   GRIDTABLE_NOTIFY_ROWS_INSERTED,
                                   row,
                                   num)                              
            self.GetView().ProcessTableMessage(msg)
        except IndexError:
            pass

    def Clear(self):
        """ clear the data"""
        self.data = []



class ContactGrid(TMGrid):
    def __init__(self, parent, ID):
        TMGrid.__init__(self, parent, ID)

                
        self.table = DataTable()
        self.SetTable(self.table, True)
        self.__columnTune()

        self.SetRowLabelSize(50)

        # some event on the grid
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(EVT_GRID_CELL_RIGHT_CLICK, self.OnRightDown)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        parent.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
    def GetSelectedRows(self):
        """
        Selections in the Grid are kinda wierd.  There are several
        kinds of selections (cell, block, row and col) and there can
        be multiples of each active at the same time.  How a selection
        is made determines what kind of selection it is.  So depending
        on how you select the rows, you may actually be getting a
        block selection and you'll need to use
        GetSelectionBlockTopLeft and GetSelectionBlockBottomRight to
        get the info about it.

        Robin Dunn/Roger Bins
        
        """

        rows=[]
        gcr=self.GetGridCursorRow()
        set1=self.GetSelectionBlockTopLeft()
        set2=self.GetSelectionBlockBottomRight()
        if len(set1):
            assert len(set1)==len(set2)
            for i in range(len(set1)):
                for row in range(set1[i][0], set2[i][0]+1): # range in wx is inclusive of last element
                    if row not in rows:
                        rows.append(row)
        else:
            rows.append(gcr)
        return rows


    def OnRightDown(self, evt):
        """ right click, make menu with folder manupilation functions"""

        
        currentpoint = evt.GetPosition()

        def __InsertNewRowBeforeCurrentRow(evt):
            self.InsertRows(self.GetGridCursorRow())
            self.ForceRefresh()

        def __InsertNewRowAfterCurrentRow(evt):
            self.InsertRows(self.GetGridCursorRow()+1)
            self.ForceRefresh()

        def __Reload(evt):
            """ reload the intercept grid"""

            self.GetParent().reload()

        def __Delete(evt):
            """ delete the selected trigger sets"""

            rows = self.GetSelectedRows()
            for c, row in enumerate(rows):
                 self.DeleteRows(row-c)

            self.ForceRefresh()
            
        if not hasattr(self, "beforeID"):            
            self.beforeID = wx.NewId()
            self.afterID = wx.NewId()
            self.reloadID = wx.NewId()
            self.deleteID = wx.NewId()
            
            self.Bind(wx.EVT_MENU, __InsertNewRowBeforeCurrentRow, id=self.beforeID)
            self.Bind(wx.EVT_MENU, __InsertNewRowAfterCurrentRow, id=self.afterID)
            self.Bind(wx.EVT_MENU, __Reload, id=self.reloadID)
            self.Bind(wx.EVT_MENU, __Delete, id=self.deleteID)
            
        menu = wx.Menu("Contact List")
        menu.Append(self.beforeID, "Insert Before")
        menu.Append(self.afterID, "Insert After")
        menu.AppendSeparator()
        menu.Append(self.deleteID, "Delete")
        menu.AppendSeparator()
        menu.Append(self.reloadID, "Reload Contact List")
        
        self.PopupMenu(menu, currentpoint)
        menu.Destroy()


        
    def addNewRow(self):
        """ add a new row"""
        
        self.InsertRows(self.GetGridCursorRow()+1)
        self.ForceRefresh()

        
    def OnKeyDown(self, evt):
        """ create when enter is hit """
        
        def __addNewRowXXX():
            """ add a new contact"""

            self.InsertRows(self.GetGridCursorRow()+1)
            self.ForceRefresh()
        
        key = evt.GetKeyCode()
        if key == wx.WXK_RETURN:
            self.addNewRow()
        else:            
            evt.Skip()



    def __clearGrid(self, evt=None):
        """ clear the grid """

        self.DeleteRows(0, self.GetNumberRows(), True)
        self.ClearGrid()


    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

        
    def __dataArrived(self, data):
        """ the data arrived from the DB"""

        self.setData(copy.copy(data))

    def setData(self, data):
        """ the list is being updated from afar"""

        self.__clearGrid()
        self.table.SetData(copy.copy(data))

        self.SetMargins(0,0)
        #self.AutoSizeColumns(True)
        self.AutoSizeRows(True)

    def getData(self):
        """ returns grid's data dict"""
        return copy.copy(self.GetTable().data)



    def __columnTune(self):
        """ format colums """

        self.SetRowLabelSize(50)
        self.SetMargins(0,0)        

        for i, label in enumerate(colLabels):
            if label in ['Contact Type']:
                self.SetColSize(i, 250)
                atr = GridCellAttr()
                atr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
                atr.SetBackgroundColour(Colors.INFOCOL)
                self.SetColAttr(i, atr)

            if label in ['Number']:
                self.SetColSize(i, 600)

                atr = GridCellAttr()
                atr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)                
                self.SetColAttr(i, atr)

