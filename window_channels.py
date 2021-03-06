# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# streamondemand-pureita
# Copyright 2015 tvalacarta@gmail.com
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of streamondemand-pureita.
#
# streamondemand-pureita is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# streamondemand-pureita is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with streamondemand-pureita. If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------

import os
import sys
import urlparse, urllib, urllib2

import xbmc
import xbmcgui
import xbmcaddon

from windowtools import *

import plugintools
import navigation
from core.item import Item


class ChannelWindow(xbmcgui.WindowXML):

    def __init__(self, xml_name, fallback_path, *args, **kwargs):
        plugintools.log("ChannelWindow.__init__ xml_name=" + xml_name + " fallback_path=" + fallback_path)

        if self.getResolution() > 0:
             self.setCoordinateResolution(0)

        self.first_time = False
        self.itemlist = []

    def setParentItem(self, item):
        self.parent_item = item

    def setItemlist(self, itemlist):
        plugintools.log("ChannelWindow.setItemlist")

        for item in itemlist:
            plugintools.log("ChannelWindow.setItemlist item=" + item.tostring())
            self.itemlist.append(item)

    def onInit(self):
        plugintools.log("ChannelWindow.onInit")

        if self.first_time == True:
            return

        self.first_time = True

        self.control_list = self.getControl(100)
        for item in self.itemlist:

            list_item = xbmcgui.ListItem(item.title, iconImage=item.thumbnail, thumbnailImage=item.thumbnail)

            info_labels = {"Title": item.title, "FileName": item.title, "Plot": item.plot}
            list_item.setInfo("video", info_labels)

            if item.fanart != "":
                list_item.setProperty('fanart_image', item.fanart)

            self.control_list.addItem(list_item)

        self.setFocusId(100)

    def onAction(self, action):
        plugintools.log("ChannelWindow.onAction action.id=" + repr(action.getId()) + " action.buttonCode=" + repr(
            action.getButtonCode()))

        ## Botón izquierdo del ratón para las listas del inicio hasta la primera lista de menú de los canales.
        if action == 100: action = ACTION_SELECT_ITEM

        if action == ACTION_PARENT_DIR or action == ACTION_PREVIOUS_MENU or action == ACTION_PREVIOUS_MENU2:
            self.close()

        if action == ACTION_SELECT_ITEM:
            from core import config

            skin_selector = config.get_setting("skin_selector")
            if skin_selector == "":
                skin_selector = "0"

            if skin_selector == "0":
                loader_image = os.path.join(plugintools.get_runtime_path(), 'resources', 'skins', 'Default', 'media',
                                            'loader.gif')
            if skin_selector == "1":
                loader_image = os.path.join(plugintools.get_runtime_path(), 'resources', 'skins', 'Default', 'media',
                                            'loader-1.gif')

            loader = xbmcgui.ControlImage(1830, 26, 64, 64, loader_image)
            self.addControl(loader)

            pos = self.control_list.getSelectedPosition()
            item = self.itemlist[pos]
            if item.action.startswith("play_"):
                play_items = navigation.get_next_items(item)
                loader.setVisible(False)

                media_url = play_items[0].url
                plugintools.direct_play(media_url)
            else:
                next_items = navigation.get_next_items(item)
                loader.setVisible(False)

                # Si no hay nada, no muestra la pantalla vacía
                if len(next_items) > 0:
                    next_window = navigation.get_window_for_item(item)
                    next_window.setItemlist(next_items)
                    next_window.setParentItem(item)

                    next_window.doModal()
                    del next_window

    def onFocus(self, control_id):
        plugintools.log("ChannelWindow.onFocus " + repr(control_id))
        pass

    def onClick(self, control_id):
        plugintools.log("ChannelWindow.onClick " + repr(control_id))
        pass

    def onControl(self, control):
        plugintools.log("ChannelWindow.onClick " + repr(control))
        pass
