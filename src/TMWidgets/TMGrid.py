# bplate

import wx
import wx.grid as gridlib


class TMGrid(gridlib.Grid):
    def __init__(self, parent, ID,
                 size=wx.DefaultSize,
                 name="TMGrid",
                 style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_HRULES|wx.LC_VRULES,
                 notifies=[]):
        gridlib.Grid.__init__(self, parent, ID, name=name, size=size, style=style)
        
        self.parent = parent        
        if len(notifies) > 0:
            for notify in notifies: REGISTAR.addPanel(notify, self)                

        gridlib.EVT_GRID_EDITOR_CREATED(self, self.OnGridEditorCreated) 
        wx.EVT_MENU_OPEN(self, self.OnMenuOpen) 
   
    def OnGridEditorCreated(self, event): 
        """ Bind the kill focus event to the newly instantiated cell editor """ 

        editor = event.GetControl() 
        wx.EVT_KILL_FOCUS(editor, self.OnKillFocus) 
        event.Skip() 
 
    def OnKillFocus(self, event): 
        #Cell editor's grandparent, the grid GridWindow's parent, is the grid. 
        grid = event.GetEventObject().GetGrandParent()        
        grid.SaveEditControlValue() 
        grid.HideCellEditControl() 
        event.Skip() 
 
    def OnMenuOpen(self, event): 
        self.grid.HideCellEditControl()

        
    def getHTML(self, addbody=True, tableHeaders=True, cellpadding=0,cellspacing=0,align='left',valign='top'):
        """ Get HTML suitable for printing out the data in this grid via
        wx.HtmlEasyPrinting. """
        
        cols = self.GetNumberCols()
        rows = self.GetNumberRows()
        width = self.GetSize()[0]
        
        if addbody:
            html = ["<HTML><BODY>"]
        else:
            html = []
            
        html.append("<TABLE BORDER=1 CELLPADDING=%i CELLSPACING=%i width=75%%>" % (cellpadding,cellspacing))
        
        if tableHeaders:
            html.append("<TR>")
            for col in range(cols):
                html.append("<TD ALIGN='center' VALIGN='top' WIDTH=%s%%><B><pre>%s</pre></B></TD>"
                                % (float(self.GetColSize(col))/float(width)*100.0, self.GetColLabelValue(col)))
            html.append("</TR>")
        
        for row in range(rows):
            html.append("<TR>")
            for col in range(cols):
                html.append("<TD ALIGN='%s' VALIGN='%s'><pre>%s</pre></TD>"
                                % (align,valign,self.GetCellValue(row,col)))
            html.append("</TR>")
        
        html.append("</TABLE>")
        return "\n".join(html)

    def addcell(s):
        return "<TD>%s</TD>"%s

    def addrow(ls):
        # adds a list of strings as a row
        return "<TR>%s</TR>"%"\n\t".join([addcell(x) for x in ls])

    def GetClassName(self):
        """ the class name """
        return "TMGrid"



