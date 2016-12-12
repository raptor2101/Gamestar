# -*- coding: utf-8 -*-
#-------------LicenseHeader--------------
# plugin.video.gamestar - Downloads/view videos from gamestar.de
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
from source import Source
from ui import *;

class GameproWeb(Source):
  def __init__(self, gui):
    super(GameproWeb, self).__init__(gui);
    
    self.rootLink = "http://www.gamepro.de/";
    self.shortName = "GP";
    
    linkRoot = self.rootLink+"videos/";
    imageRoot = "http://images.gamepro.de/images/idgwpgsgp/bdb/";    
    ##setup categories
    self.categories = {
      30001:GalleryObject(linkRoot+"alle-videos,9200,newest/", imageRoot+"/2018270/b144x81.jpg"),
      30002:GalleryObject(linkRoot+"tests,17/",imageRoot+"2018272/b144x81.jpg"),
      30003:GalleryObject(linkRoot+"previews,18/",imageRoot+"bdb/2018269/b144x81.jpg"),
      30004:GalleryObject(linkRoot+"specials,20/",imageRoot+"2018270/b144x81.jpg"),
      30011:GalleryObject(linkRoot+"trailer,3","http://images.cgames.de/images/idgwpgsgp/bdb/2017073/b144x81.jpg"),
      30009:GalleryObject(linkRoot+"candyland,102/","http://images.cgames.de/images/idgwpgsgp/bdb/2557236/b144x81.jpg"),
      30104:GalleryObject(linkRoot+"was-ist-,96/","http://2images.cgames.de/images/idgwpgsgp/bdb/2764163/446x251.jpg"),
      30010:GalleryObject(linkRoot+"boxenstop,2",imageRoot+"2018274/b144x81.jpg"),
      30105:GalleryObject(linkRoot+"frisch-gestrichen,104/","http://1images.cgames.de/images/idgwpgsgp/bdb/2740413/446x251.jpg"),
      30106:GalleryObject(linkRoot+"news,100/","http://4images.cgames.de/images/idgwpgsgp/bdb/2764165/446x251.jpg"),
      }
    ##endregion
