#!/usr/bin/env python
# coding:utf-8


import wx
import sqlite3

class GuangFrame(wx.Frame):
    
    def __init__(self):
        #繪製主窗體
        wx.Frame.__init__(self,None,id=-1,title = u"廣韻查詢系統", size = (500,300),style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        #繪製窗體控件龢按鈕
        panel = wx.Panel(self)
        self.icon = wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.tiptext = wx.StaticText(panel, -1, u"在此處輸入：",pos=(10,15),size=(100,15),style = wx.ALIGN_CENTER)
        tipfont = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.tiptext.SetFont(tipfont)
        self.wordtext = wx.TextCtrl(panel, -1, pos=(120,10), size=(150,30), style = wx.TE_PROCESS_ENTER)
        self.querybutton = wx.Button(panel, -1, label = u"查詢", pos = (275,10), size = (105,30))
        self.quitbutton = wx.Button(panel, -1, label = u"退出", pos = (385,10),size = (105,30))
        self.answertext = wx.TextCtrl(panel, -1, u"\n\n\n***暫時不支持繁簡轉換，請輸入繁體字***\n請在上方輸入框中輸入查詢字。(一次輸入一個)\n查詢結果將在這裏輸出。\n作者個人網站,敬請期待更多作品：\n http://brant.zz.mu \n孔和佳慧  出品\n\n",pos=(10,50), size=(480,215),style = wx.TE_MULTILINE | wx.TE_READONLY)
        answerfont = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.answertext.SetFont(answerfont)
        #綁定 查詢 功能
        self.Bind(wx.EVT_BUTTON, self.OnQuery, self.querybutton)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnQuery, self.wordtext)
        #綁定 退出 按鈕
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.quitbutton)
    #定義 查詢 功能
    def OnQuery(self,event):
        conn = sqlite3.connect('guang.db')
        cursor = conn.cursor()
        keyword = self.wordtext.GetValue()
        key = "%%%s%%" % keyword
        cursor.execute("select cet, miuk, sjeng, xu, tonk, dew, sheng, yun from guang  where glyphs like '%s'" % key)
        values = cursor.fetchall()
        self.answertext.Clear()
        num = len(values)
        if len(keyword) > 1:
            dialog = wx.MessageBox(u"一次只能查詢一個字", u"錯誤", wx.OK)
        elif len(keyword) == 1:
            if num == 0:
                txtcon = u"抱歉，未找到輸入字，該字可能不在《廣韻》中。\n"
                self.answertext.AppendText(txtcon)
            elif num == 1:
                txtcon = u"共找到1條記錄:\n\n%s，%s切，%s聲字。\n\n%s紐%s韻字，%s等韻，%s口字。\n\n擬音（國際音標）：[%s%s]\n" % (keyword, values[0][0], values[0][5], values[0][2], values[0][1], values[0][4], values[0][3], values[0][6], values[0][7])
                self.answertext.AppendText(txtcon)
            elif num > 1:
                txtcon = u"共找到%s條記錄：\n\n" % num
                self.answertext.AppendText(txtcon)
                for n in range(num):
                    txtcon = u"第%s條：\n\n%s，%s切，%s聲字。\n\n%s紐%s韻字，%s等韻，%s口字。\n\n擬音（國際音標）：[%s%s]\n\n" % (n+1, keyword, values[n][0], values[n][5], values[n][2], values[n][1], values[n][4], values[n][3], values[n][6], values[n][7])
                    self.answertext.AppendText(txtcon)
            
    #定義 退出 函數
    def OnCloseMe(self,event):
        self.Close(True)
    
class MyApp(wx.App):
    def OnInit(self):
        self.frame = GuangFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()