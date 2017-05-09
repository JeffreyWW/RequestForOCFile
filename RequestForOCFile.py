import wx
import requests
from OCFileTransforNew import rightWord
from OCFileTransforNew import requestForNet
from OCFileTransforNew import wiriteOcModelTofile
from JsonFile import setRightJsonWithParameter
from JsonFile import getRightJson
from JsonFile import getDataJson
from JsonFile import updateRequestUrl


class preViewFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '头部权限文件预览', size=(480, 400))
        self.panel = wx.Panel(self, -1)


class confirmViewFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '网络请求结果', size=(800, 400))
        self.lbCurrentValue = None
        self.panel = wx.Panel(self, -1)


class selectResponseFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '次级字段', size=(250, 200))
        self.panel = wx.Panel(self, -1)


def warning(title, warn):
    dlg = wx.MessageDialog(None, warn,
                           title,
                           wx.YES_DEFAULT | wx.ICON_ERROR)
    retCode = dlg.ShowModal()
    if retCode == wx.ID_YES:
        print('确定')
    dlg.Destroy()


    # basicText.SetInsertionPoint(0)

    # self.pwdLabel = wx.StaticText(panel, -1, "Password:")
    # self.pwdText = wx.TextCtrl(panel, -1, "password", size=(175, -1),
    #                            style=wx.TE_PASSWORD)
    # sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
    # sizer.AddMany([basicLabel, basicText, pwdLabel, pwdText])
    # panel.SetSizer(sizer)


class AppFrame(wx.Frame):

    def Preview(self, event):
        pFrame = preViewFrame()
        self.rightText = rightWord(self.txtClassName.GetValue(), self.txtProjectName.GetValue(),
                                   self.txtCreator.GetValue(), self.txtRightOwner.GetValue())
        setRightJsonWithParameter(self.txtClassName.GetValue(), self.txtProjectName.GetValue(),
                                  self.txtCreator.GetValue(), self.txtRightOwner.GetValue())
        pFrame.lbRight = wx.StaticText(pFrame.panel, -1, self.rightText, pos=(10, 40))
        pFrame.Show()

    # 确认开始请求按钮点击
    def requestConfirm(self, event):
        # 请求之前先存储下权限到json文件里，下次读取从数据库里读'
        setRightJsonWithParameter(self.txtClassName.GetValue(), self.txtProjectName.GetValue(),
                                  self.txtCreator.GetValue(), self.txtRightOwner.GetValue())
        self.confirmView = confirmViewFrame()
        self.confirmView.lbCurrentValue = wx.StaticText(self.confirmView.panel, -1, '', pos=(300, 152))
        try:
            self.responseJson = requestForNet(self.txtRequestUrl.GetValue(), self.reViewParameter)
            updateRequestUrl(self.txtRequestUrl.GetValue())
            self.confirmView.lbResponse = wx.StaticText(self.confirmView.panel, -1, '返回结果为:', pos=(50, 30))
            self.confirmView.txtResponse = wx.TextCtrl(self.confirmView.panel, -1, str(self.responseJson), pos=(50, 60),
                                                       size=(600, 80),
                                                       style=wx.TE_MULTILINE | wx.TE_READONLY)
            responseDic = dict(eval(str(self.responseJson)))
            self.responseParameter = list(responseDic.keys())

            # 选择次级字段按钮
            self.confirmView.btSelectResponse = wx.Button(self.confirmView.panel, -1, '选择返回的子字段用来生成h和m文件:',
                                                          pos=(50, 150))
            self.confirmView.Bind(wx.EVT_BUTTON, self.selectResponse, self.confirmView.btSelectResponse)

            self.confirmView.btSelectDirect = wx.Button(self.confirmView.panel, -1, '直接使用返回的json生成h和m文件', pos=(50, 180))
            self.confirmView.Bind(wx.EVT_BUTTON, self.selectDirect, self.confirmView.btSelectDirect)

            self.confirmView.Show()
        except requests.exceptions.MissingSchema:
            warning('错误', '请求错误')



    # 添加新的参数点击
    def addParameter(self, event):
        if self.reViewParameter is None:
            self.reViewParameter = {}
        key = self.txtKey.GetValue()
        if key == '':
            return

        value = self.txtValue.GetValue()
        self.reViewParameter[key] = value
        self.txtKey.SetValue('')
        self.txtValue.SetValue('')
        self.txtParameterReview.SetValue(str(self.reViewParameter))

    # 清空请求参数
    def clearParameter(self, envent):
        self.reViewParameter = None
        self.txtParameterReview.SetValue('')

    # 点击选择结果字段按钮
    def selectResponse(self, event):
        self.selectResponseView = selectResponseFrame()
        self.listBox = wx.ListBox(self.selectResponseView.panel, -1, pos=(20, 20), size=(100, 120),
                                  choices=self.responseParameter)
        self.listBox.SetSelection(0)

        self.selectResponseView.btConfirmSelect = wx.Button(self.selectResponseView.panel, -1, '确定', pos=(140, 20),
                                                            size=(100, 120))
        self.selectResponseView.Bind(wx.EVT_BUTTON, self.confirmSubWord, self.selectResponseView.btConfirmSelect)

        self.selectResponseView.Show()

    def selectDirect(self, event):
        self.writeOCFile(writeJson=self.responseJson)

    def writeOCFile(self, writeJson):
        try:
            wiriteOcModelTofile(self.txtClassName.GetValue(), self.txtProjectName.GetValue(),
                                self.txtCreator.GetValue(),
                                self.txtRightOwner.GetValue(), writeJson)
        except ValueError:
            warning('参数错误ValueError', '没有次级字段')
            self.confirmView.lbCurrentValue.SetLabel('')
        except TypeError:
            self.confirmView.lbCurrentValue.SetLabel('')
            warning('参数错误TypeError', '没有次级字段')

    # 确定选择子字段
    def confirmSubWord(self, event):
        index = self.listBox.GetSelection()
        currentKey = self.responseParameter[index]
        self.confirmView.lbCurrentValue.SetLabel(currentKey)
        currentJson = self.responseJson[currentKey]
        self.writeOCFile(writeJson=currentJson)
        self.selectResponseView.Show(False)



    def __init__(self):
        wx.Frame.__init__(self, None, -1, '网络请求OC文件写入工具',
                          size=(600, 800))
        self.reViewParameter = None
        self.rightText = '默认文字'
        panel = wx.Panel(self, -1)
        firstLabelX = 50
        firstLabelY = 50
        firstTextX = 130
        firstTextY = 48
        i = 0
        self.lbClassName = wx.StaticText(panel, -1, "类名:", pos=(firstLabelX, firstLabelY + i * 40))
        self.txtClassName = wx.TextCtrl(panel, -1, getRightJson()['className'], pos=(firstTextX, firstTextY + i * 40),
                                        size=(300, -1))
        i = i + 1
        self.lbProjectName = wx.StaticText(panel, -1, "项目名:", pos=(firstLabelX, firstLabelY + i * 40))
        self.txtProjectName = wx.TextCtrl(panel, -1, getRightJson()['projectName'],
                                          pos=(firstTextX, firstTextY + i * 40), size=(300, -1))
        i = i + 1
        self.lbCreator = wx.StaticText(panel, -1, "作者:", pos=(firstLabelX, firstLabelY + i * 40))
        self.txtCreator = wx.TextCtrl(panel, -1, getRightJson()['creator'], pos=(firstTextX, firstTextY + i * 40),
                                      size=(300, -1))
        i = i + 1
        self.lbRightOwner = wx.StaticText(panel, -1, "所有权:", pos=(firstLabelX, firstLabelY + i * 40))
        self.txtRightOwner = wx.TextCtrl(panel, -1, getRightJson()['rightOwner'], pos=(firstTextX, firstTextY + i * 40),
                                         size=(300, -1))

        self.rightText = rightWord(self.txtClassName.GetValue(), self.txtProjectName.GetValue(),
                                   self.txtCreator.GetValue(), self.txtRightOwner.GetValue())
        self.btPreview = wx.Button(panel, -1, '预览头部权限文件', pos=(firstLabelX, firstLabelX + i * 40 + 30))
        self.Bind(wx.EVT_BUTTON, self.Preview, self.btPreview)
        self.btPreview.SetDefault()

        i = i + 1
        self.lbRequestUrl = wx.StaticText(panel, -1, "请求地址:", pos=(firstLabelX, firstLabelY + i * 40 + 50))
        self.txtRequestUrl = wx.TextCtrl(panel, -1, getDataJson()['requestUrl'],
                                         pos=(firstTextX, firstTextY + i * 40 + 50), size=(300, -1))
        i = i + 1
        self.lbKey = wx.StaticText(panel, -1, "请求参数:", pos=(firstLabelX, firstLabelY + i * 40 + 50))
        self.txtKey = wx.TextCtrl(panel, -1, "", pos=(firstTextX, firstTextY + i * 40 + 50),
                                  size=(100, -1))
        self.lbColon = wx.StaticText(panel, -1, ":", pos=(firstTextX + 120, firstTextY + i * 40 + 50),
                                     size=(10, -1))
        self.txtValue = wx.TextCtrl(panel, -1, "", pos=(firstTextX + 150, firstTextY + i * 40 + 50),
                                    size=(100, -1))
        # 添加参数按钮
        self.btAddParameter = wx.Button(panel, -1, '添加', pos=(firstTextX + 260, firstLabelY + i * 40 + 50 - 1))
        self.Bind(wx.EVT_BUTTON, self.addParameter, self.btAddParameter)

        # 清空
        self.btClear = wx.Button(panel, -1, '清空', pos=(firstTextX + 350, firstLabelY + i * 40 + 50 - 1))
        self.Bind(wx.EVT_BUTTON, self.clearParameter, self.btClear)

        i = i + 1
        self.lbParameterReview = wx.StaticText(panel, -1, '参数预览:',
                                               pos=(firstLabelX, firstLabelY + i * 40 + 50))
        self.txtParameterReview = wx.TextCtrl(panel, -1, '',
                                              pos=(firstTextX - 15, firstLabelY + i * 40 + 50 - 1),
                                              size=(350, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # 确认请求按钮
        self.btConfirm = wx.Button(panel, -1, '开始请求', pos=(200, 700))
        self.Bind(wx.EVT_BUTTON, self.requestConfirm, self.btConfirm)
        self.btConfirm.SetDefault()


class writeOCFileApp(wx.App):
    def OnInit(self):
        self.frame = AppFrame()
        self.frame.Show()
        return True

    def OnExit(self):
        print('退出')
        return True

if __name__ == '__main__':
    app = writeOCFileApp()
    app.MainLoop()
