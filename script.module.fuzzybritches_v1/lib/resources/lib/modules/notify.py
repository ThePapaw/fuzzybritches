# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v1
# Addon id: script.module.fuzzybritches_v1
# Addon Provider: The Papaw

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import time
from datetime import date, datetime, timedelta
ADDON_ID            = 'plugin.video.fuzzybritches_v1'
AddonTitle          = 'The Papaw'
fanart              = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.gif'))
setting             = xbmcaddon.Addon().getSetting
addonInfo           = xbmcaddon.Addon().getAddonInfo
HOME                = xbmc.translatePath('special://home/')
XXX_SETTINGS        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'settings.xml'))
PARENTAL_FOLDER     = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID , 'parental'))
DATA_FOLDER         = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID))
ADDON_FOLDER        = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID))
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
ART            = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'resources', 'art'))
TERMS          = "\n[COLOR aqua]Fuzzy Britches Disclaimer[/COLOR] \n\n[COLOR ff4cff4c]This Addon does not host, provide, archive, store, or distribute media of any kind, and acts merely as an index (or directory) of media posted by others that are hosted on the internet. Whereas we do not filter such references, we cannot and do not attempt to control, censor, or block any indexed material that may be considered offensive, abusive, libellous, obnoxious, inaccurate, deceptive, unlawful or otherwise distressing neither do we accept responsibility for this content or the consequences of such content being made available. \n\nAll users are advised to use caution, discretion, common sense and personal judgment when using addons such as this or any references detailed within the directory and to respect the wishes of others who may value freedom from censorship, as consenting adults equal to (or possibly superior to) your own personal preferences. \n\nEnjoy![/COLOR]\n\n[COLOR crimson]By agreeing, you are accepting that you are legally bound to these Terms and Conditions[/COLOR]"
I_AGREE        = xbmc.translatePath(os.path.join(DATA_FOLDER , 'agreed.txt'))
BACKGROUND     = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'resources', 'art', 'ContentPanel.png'))
FONTHEADER     = 'Font14'
HEADERIMAGE    = ''
FONTSETTINGS   = 'Font12'
HEADERTYPE     = 'Text'

############################

ACTION_PREVIOUS_MENU            =  10   ## ESC action
ACTION_NAV_BACK                 =  92   ## Backspace action
ACTION_MOVE_LEFT                =   1   ## Left arrow key
ACTION_MOVE_RIGHT               =   2   ## Right arrow key
ACTION_MOVE_UP                  =   3   ## Up arrow key
ACTION_MOVE_DOWN                =   4   ## Down arrow key
ACTION_MOUSE_WHEEL_UP           = 104   ## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN         = 105   ## Mouse wheel down
ACTION_MOVE_MOUSE               = 107   ## Down arrow key
ACTION_SELECT_ITEM              =   7   ## Number Pad Enter
ACTION_BACKSPACE                = 110   ## ?
ACTION_MOUSE_LEFT_CLICK         = 100
ACTION_MOUSE_LONG_CLICK         = 108

def artwork(file):
    if   file == 'button': return os.path.join(ART, 'Button', 'button-focus_lightblue.png'), os.path.join(ART, 'Button', 'button-focus_grey.png')
    
def AgreeFirst(msg=TERMS, resize=False, L=0 ,T=0 ,W=1280 ,H=720 , TxtColor='0xFFFFFFFF', Font=FONTSETTINGS, BorderWidth=15):

    class MyWindow(xbmcgui.WindowDialog):
        scr={};
        def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font14',BorderWidth=10):
            image_path = os.path.join(ART, 'ContentPanel.png')
            self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
            self.addControl(self.border); 
            self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), BACKGROUND, aspectRatio=0, colorDiffuse='0x9FFFFFFF')
            self.addControl(self.BG)
            #title
            if HEADERTYPE == 'Image':
                iLogoW=164; iLogoH=68
                self.iLogo=xbmcgui.ControlImage((L+(W/2))-(iLogoW/2),T+10,iLogoW,iLogoH,HEADERIMAGE,aspectRatio=0)
                self.addControl(self.iLogo)
            else:
                title = '[COLOR yellow]Disclaimer[/COLOR]'
                times = int(float(FONTHEADER[-2:]))
                temp = title.replace('[', '<').replace(']', '>')
                temp = re.sub('<[^<]+?>', '', temp)
                title_width = len(str(temp))*(times - 1)
                title = title
                self.title=xbmcgui.ControlTextBox(L+(W-title_width)/2,T+BorderWidth,title_width,30,font=FONTHEADER,textColor='0xFF1E90FF')
                self.addControl(self.title)
                self.title.setText(title)
            #body
            msg = TERMS
            self.TxtMessage=xbmcgui.ControlTextBox(L+BorderWidth+10,T+30+BorderWidth,W-(BorderWidth*2)-20,H-(BorderWidth*2)-75,font=Font,textColor=TxtColor)
            self.addControl(self.TxtMessage)
            self.TxtMessage.setText(msg)
            #buttons
            
            focus, nofocus = artwork('button')
            w1      = int((W-(BorderWidth*5))/3); h1 = 35
            t       = int(T+H-h1-(BorderWidth*1.5))
            space   = int(L+(BorderWidth*1.5))
            dismiss = int(space+w1+BorderWidth)
            
            self.buttonDismiss=xbmcgui.ControlButton(dismiss,t,w1,h1,"I Agree",textColor="0xFF000000",focusedColor="0xFF000000",alignment=2,focusTexture=focus,noFocusTexture=nofocus)
            self.addControl(self.buttonDismiss)
            self.setFocus(self.buttonDismiss)


        def doDismiss(self):
            try:    
                open(I_AGREE, 'w')
                self.CloseWindow()
            except: pass
            self.CloseWindow()

        def onAction(self,action):
            try: F=self.getFocus()
            except: F=False
            if   action == ACTION_PREVIOUS_MENU: self.doDismiss()
            elif action == ACTION_NAV_BACK: self.doDismiss()

        def onControl(self,control):
            try:
                if control== self.buttonDismiss: self.doDismiss()
            except: pass
        
        def CloseWindow(self): self.close()
        def exit(self): sys.exit(0)
    if resize==False: maxW=1280; maxH=720; W=int(maxW/1.5); H=int(maxH/1.5); L=int((maxW-W)/2); T=int((maxH-H)/2); 
    TempWindow=MyWindow(msg=msg,L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth)
    TempWindow.doModal()
    del TempWindow