#-*- coding: UTF-8 -*-
import os,sys,gtk
import gettext
from configobj import ConfigObj

from Translation import Translation

VERSION = "0.9.7.2"
APP_NAME = "gmediafinder"
exec_path =  os.path.dirname(os.path.abspath(__file__))

## LOCALISATION
source_lang = "en"
rep_trad = "/usr/share/locale"


## gui
if ('/usr/local' in exec_path):
    data_path = os.path.join('/usr/local/share/gmediafinder')
elif ('/usr' in exec_path):
	data_path = os.path.join('/usr/share/gmediafinder')
else:
    data_path =  os.path.join(exec_path,"../data")

if sys.platform == "win32" and not ('config.py' in os.listdir(os.path.abspath('.'))):
    data_path= "data"
    rep_trad = "po"
if sys.platform == "win32" and ('config.py' in os.listdir(os.path.abspath('.'))):
    rep_trad = os.path.join(os.path.abspath('..'),'po')
    data_path= os.path.join(os.path.abspath('..'),'data')

img_path = os.path.join(data_path,"img")
glade_path = os.path.join(data_path,"glade")
glade_file = os.path.join(glade_path,"mainGui.glade")

##localisation end
traduction = Translation(APP_NAME, source_lang, rep_trad)
gettext.install(APP_NAME)
gtk.glade.bindtextdomain(APP_NAME, rep_trad)
gettext.textdomain(APP_NAME)
_ = traduction.gettext

## gui config
vis="jess"
width = gtk.gdk.screen_width()
height = gtk.gdk.screen_height()
window_state = "%s,%s,%s,%s" % (width-200,height-80,0,0)
show_thumbs_opt = "True"
downloads = False
convert = False
max_history = 50

if sys.platform == "win32":
    from win32com.shell import shell, shellcon
    df = shell.SHGetDesktopFolder()
    pidl = df.ParseDisplayName(0, None,"::{450d8fba-ad25-11d0-98a8-0800361b1103}")[1]
    mydocs = shell.SHGetPathFromIDList(pidl)
    down_dir = os.path.join(mydocs,"gmediafinder-downloads")
    settings_folder = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0),"gmediafinder")
else:
    down_dir = os.path.join(os.getenv('HOME'),"gmediafinder-downloads")
    settings_folder = os.path.join(os.getenv('HOME'),".config/gmediafinder")
## small config dir for downloads...
if not os.path.exists(down_dir):
    os.mkdir(down_dir)
## Get Icons shown on buttons
settings = gtk.settings_get_default()
gtk.Settings.set_long_property(settings, "gtk-button-images", 1, "main")

## conf file
conf_file = os.path.join(settings_folder, 'gmediafinder_config')
## systray
systray = False
    
if not os.path.exists(settings_folder):
    os.mkdir(settings_folder)
    fd = os.open(conf_file, os.O_RDWR|os.O_CREAT)
    os.write(fd,"download_path=%s\n" % down_dir)
    os.write(fd,"window_state=%s\n" % window_state)
    os.write(fd,"show_thumbs=%s\n" % show_thumbs_opt)
    os.write(fd,"visualisation=%s\n" % vis)
    os.write(fd,"downloads=%s\n" % downloads)
    os.write(fd,"convert=%s\n" % downloads)
    os.close(fd)
conf = ConfigObj(conf_file,write_empty_values=True)

## history file
history_file = os.path.join(settings_folder, 'history')
if not os.path.exists(history_file):
    f = open(history_file,'w')
    f.write(' ')
    f.close()
## down dir
try:
    down_dir = conf["download_path"]
except:
    conf["download_path"] = down_dir
    conf.write()
## get saved window position ans size
try:
    window_state = conf["window_state"]
except:
    conf["window_state"] = window_state
    conf.write()
## gui options
try:
    show_thumbs_opt = conf["show_thumbs"]
except:
    conf["show_thumbs"] = True
    conf.write()

## extras options
try:
    downloads = conf["downloads"]
except:
    conf["downloads"] = downloads
    conf.write()
try:
    convert = conf["convert"]
except:
    conf["convert"] = convert
    conf.write()
    
## history
try:
    max_history = conf["max_history"]
except:
    conf["max_history"] = max_history
    conf.write()

## systray
try:
    systray = conf["systray"]
except:
    conf["systray"] = systray
    conf.write()
