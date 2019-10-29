#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale
import os
import re
import sys

# setup done to /home/mobvoi/bing-desktop-wallpaper-changer by BDWC Installer v3.3.1-release
path_to_Bing_Wallpapers="/home/mobvoi/bing-desktop-wallpaper-changer"
get_image_number_one_time = 8

# wait computer internet connection
#os.system("sleep 10")

try:  # try python 3 import
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    from configparser import ConfigParser
except ImportError:  # fall back to python2
    from urllib import urlretrieve
    from urllib2 import urlopen  
    from ConfigParser import ConfigParser

import xml.etree.ElementTree as ET

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Notify
from subprocess import check_output

BING_MARKETS = [u'ar-XA',
                u'bg-BG',
                u'cs-CZ',
                u'da-DK',
                u'de-AT',
                u'de-CH',
                u'de-DE',
                u'el-GR',
                u'en-AU',
                u'en-CA',
                u'en-GB',
                u'en-ID',
                u'en-IE',
                u'en-IN',
                u'en-MY',
                u'en-NZ',
                u'en-PH',
                u'en-SG',
                u'en-US',
                u'en-XA',
                u'en-ZA',
                u'es-AR',
                u'es-CL',
                u'es-ES',
                u'es-MX',
                u'es-US',
                u'es-XL',
                u'et-EE',
                u'fi-FI',
                u'fr-BE',
                u'fr-CA',
                u'fr-CH',
                u'fr-FR',
                u'he-IL',
                u'hr-HR',
                u'hu-HU',
                u'it-IT',
                u'ja-JP',
                u'ko-KR',
                u'lt-LT',
                u'lv-LV',
                u'nb-NO',
                u'nl-BE',
                u'nl-NL',
                u'pl-PL',
                u'pt-BR',
                u'pt-PT',
                u'ro-RO',
                u'ru-RU',
                u'sk-SK',
                u'sl-SL',
                u'sv-SE',
                u'th-TH',
                u'tr-TR',
                u'uk-UA',
                u'zh-CN',
                u'zh-HK',
                u'zh-TW']

config_file_skeleton ="""[market]
# If you want to override the current Bing market dectection,
# set your preferred market here. For a list of markets, see
# https://msdn.microsoft.com/en-us/library/dd251064.aspx
area =
[directory]
# Download directory path. By default images are saved to
# /home/[user]/[Pictures]/BingWallpapers/
dir_path =
# Limit the size of the downloaded image directory
# Size should be specified in bytes. The minimum 
# limit is the size of 1 image (whatever size that image is)
# Set to negative value for unlimit. Default value is 100MiB
dir_max_size = 
"""


def get_file_uri(filename):
    return 'file://%s' % filename


def set_gsetting(schema, key, value):
    gsettings = Gio.Settings.new(schema)
    gsettings.set_string(key, value)
    gsettings.apply()


def change_background_gnome(filename):
    set_gsetting('org.gnome.desktop.background', 'picture-uri',
        get_file_uri(filename))

def change_background_cinnamon(filename):
    set_gsetting('org.cinnamon.desktop.background', 'picture-uri',
        get_file_uri(filename))



def get_current_background_gnome_uri():
    gsettings = Gio.Settings.new('org.gnome.desktop.background')
    path = gsettings.get_string('picture-uri')
    return path[6:]

def get_current_background_cinnamon_uri():
    gsettings = Gio.Settings.new('org.cinnamon.desktop.background')
    path = gsettings.get_string('picture-uri')
    return path[6:]

def get_current_background_uri():
    source = Gio.SettingsSchemaSource.get_default()
    cinnamon_exists = source.lookup('org.cinnamon.desktop.background', True)
    if cinnamon_exists:
        current = get_current_background_cinnamon_uri()
    else:
        current = get_current_background_gnome_uri()
    return current

def change_screensaver(filename):
    set_gsetting('org.gnome.desktop.screensaver', 'picture-uri',
                 get_file_uri(filename))


def get_config_file():
    """
    Get the path to the program's config file.

    :return: Path to the program's config file.
    """
    config_dir = os.path.join(os.path.expanduser('~'), '.config',
                              'bing-desktop-wallpaper-changer')
    init_dir(config_dir)
    config_path = os.path.join(config_dir, 'config.ini')
    if not os.path.isfile(config_path):
        with open(config_path, 'w') as config_file:
            config_file.write(config_file_skeleton)
    return config_path


def get_market():
    """
    Get the desired Bing Market.

    In order of preference, this program will use:
    * Config value market.area from desktop_wallpaper_changer.ini
    * Default locale, in case that's a valid Bing market
    * Fallback value is 'en-US'.

    :return: Bing Market
    :rtype: str
    """
    config = ConfigParser()
    config.read(get_config_file())
    market_area_override = config.get('market', 'area')
    if market_area_override:
        return market_area_override

    default_locale = locale.getdefaultlocale()[0]
    if default_locale in BING_MARKETS:
        return default_locale

    return 'en-US'


def get_download_path():
    # By default images are saved to '/home/[user]/[Pictures]/BingWallpapers/'
    default_path = check_output("xdg-user-dir PICTURES", shell=True).strip().decode("utf-8") + "/BingWallpapers"

    try:
        config = ConfigParser()
        config.read(get_config_file())
        path = config.get('directory', 'dir_path')

        return path or default_path
    except Exception:
        return default_path


def get_directory_limit():
    """
    Get the directory sized limit
    """
    config = ConfigParser()
    config.read(get_config_file())
    try:
        size = config.getint('directory', 'dir_max_size')
        return size
    except Exception:
        return 100 * 1024 * 1024


def get_bing_xml():
    """
    Get BingXML file which contains the URL of the Bing Photo of the day.

    :return: URL with the Bing Photo of the day.
    """
    # idx = Number days previous the present day.
    # 0 means today, 1 means yesterday
    # n = Number of images previous the day given by idx
    # mkt = Bing Market Area, see get_valid_bing_markets.
    market = get_market()
    return "https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=%d&mkt=%s" % (get_image_number_one_time, market)


def get_screen_resolution_str():
    """
    Get a regexp like string with your current screen resolution.

    :return: String with your current screen resolution.
    """
    sizes = [[800, [600]], [1024, [768]], [1280, [720, 768]],
             [1366, [768]], [1920, [1080, 1200]]]
    sizes_mobile = [[768, [1024]], [720, [1280]],
                    [768, [1280, 1366]], [1080, [1920]]]
    default_w = 1920
    default_h = 1080
    default_mobile_w = 1080
    default_mobile_h = 1920
    is_mobile = False
    window = Gtk.Window()
    screen = window.get_screen()
    nmons = screen.get_n_monitors()
    maxw = 0
    maxh = 0
    sizew = 0
    sizeh = 0
    if nmons == 1:
        maxw = screen.get_width()
        maxh = screen.get_height()
    else:
        for m in range(nmons):
            mg = screen.get_monitor_geometry(m)
            if mg.width > maxw or mg.height > maxw:
                maxw = mg.width
                maxh = mg.height
    if maxw > maxh:
        v_array = sizes
    else:
        v_array = sizes_mobile
        is_mobile = True
    for m in v_array:
        if maxw <= m[0]:
            sizew = m[0]
            sizeh = m[1][len(m[1]) - 1]
            for e in m[1]:
                if maxh <= e:
                    sizeh = e
                    break
            break

    if sizew == 0:
        if is_mobile:
            sizew = default_mobile_w
            sizeh = default_mobile_h
        else:
            sizew = default_w
            sizeh = default_h

    return r'%sx%s' % (sizew, sizeh)


def get_image_metadata():
    """
    Get Bing wallpaper metadata.

    :return: XML tag object for the wallpaper image.
    """
    bing_xml_url = get_bing_xml()
    page = urlopen(bing_xml_url)

    bing_xml = ET.parse(page).getroot()

    # For extracting complete URL of the image
    images = bing_xml.findall('image')
    return images


def get_image_url(metadata):
    """
    Get an appropriate Wallpaper URL based on your screen resolution.

    :param metadata: XML tag object with image metadata.
    :return: URL with Bing Wallpaper image.
    """
    base_image = metadata.find("url").text
    # Replace image resolution with the correct resolution
    # from your main monitor
    screen_size = get_screen_resolution_str()
    correct_resolution_image = re.sub(r'\d+x\d+', screen_size, base_image)
    return "https://www.bing.com" + correct_resolution_image


def init_dir(path):
    """
    Create directory if it doesn't exist.

    :param path: Path to a directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)


# def p3_dirscan(path):
#     files = list()
#     size = 0
#     for entry in os.scandir(path):
#         if entry.is_file() and os.path.splitext(entry.name)[1] == "jpg":
#             files.append(entry)
#             size = size + entry.stat.st_size;
#     return files, size

def p2_dirscan(path):
    files = list()
    size = 0

    for e in os.listdir(path):
        entry = path + "/" + e
        if os.path.isfile(entry) and os.path.splitext(entry)[1] == ".jpg":
            s = os.path.getsize(entry)
            files.append((entry, s))
            size = size + s
    files = sorted(files)
    return files, size

def update_image_detail_txt(detial_file_name, text):
    if os.path.isfile(detial_file_name):
        with open(detial_file_name, "r") as fd:
            lines = fd.readlines()
    else:
        lines = []
            
    do_not_need_to_update = False
    index = 0
    for line in lines:
        if text == line:
            do_not_need_to_update = True
        elif text > line:
            index += 1
        else:
            break
    #print('index = %d'%(index))
    #print('do_not_need_to_update = ' + str(do_not_need_to_update))
    lines.insert(index, text)
    
    if not do_not_need_to_update:
        with open(detial_file_name, "w") as fd:
            fd.writelines(lines)

def check_limit():
    download_path = get_download_path()
    (files, size) = p2_dirscan(download_path)
    max_size = get_directory_limit()
    while (max_size > 0 and size > max_size and len(files) > 1):
        os.remove(files[0][0])
        size = size - files[0][1]
        del files[0]


def main():
    """
    Main application entry point.
    """
    app_name = 'Bing Desktop Wallpaper'
    Notify.init(app_name)
    exit_status = 0

    try:
        image_metadatas = get_image_metadata()
        index = 0
        while True:
            image_metadata = image_metadatas[index]
            image_name = image_metadata.find("startdate").text + ".jpg"
            image_url = get_image_url(image_metadata)

            download_path = get_download_path()
            init_dir(download_path)
            image_path = os.path.join(download_path, image_name)
            print('  Current image: ' + image_path)

            if not os.path.isfile(image_path):
                urlretrieve(image_url, image_path)
                try:
                    change_background_gnome(image_path)
                except:
                    change_background_cinnamon(image_path)
                change_screensaver(image_path)
                summary = 'Bing Wallpaper updated successfully'
                body = image_metadata.find("copyright").text.encode('utf-8')

                text = str(image_name) + " -- " + str(body) + "\n"
                update_image_detail_txt(download_path + "/image-details.txt", text)

            else:
                try:
                    change_background_gnome(image_path)
                except:
                    change_background_cinnamon(image_path)
                change_screensaver(image_path)
                summary = 'Wallpaper changed to current Bing wallpaper'
                body = ('%s already exists in Wallpaper directory' %
                        image_metadata.find("copyright").text.encode('utf-8'))
            check_limit()

            is_it_fine = raw_input('  Is this wallpaper ok? [next, previous, ok, quit, exit]: ')
            if len(is_it_fine) > 0 and is_it_fine[0] == 'n':
                print('      -<- next -<-\n')
                if index < get_image_number_one_time - 1:
                    index += 1
                else:
                    index = 0
            elif len(is_it_fine) > 0 and is_it_fine[0] == 'p':
                print('      ->- previous ->-\n')
                if index > 0:
                    index -= 1
                else:
                    index = get_image_number_one_time - 1
            elif len(is_it_fine) == 0 or is_it_fine[0] in ['e', 'q', 'o']:
                break

    except Exception as err:
        summary = 'Error executing %s' % app_name
        body = err
        print(body)
        exit_status = 1
    
    os.chdir(path_to_Bing_Wallpapers)
    icon = os.path.abspath("icon.svg") 
    app_notification = Notify.Notification.new(summary, str(body), icon)
    app_notification.show()
    sys.exit(exit_status)


if __name__ == '__main__':
    main()
