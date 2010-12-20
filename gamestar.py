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
import urllib, re
from ui import *;

class GamestarWeb(object):
  def __init__(self, gui):
    self.gui = gui;
    self.rootLink = "http://www.gamestar.de";
    
    ##setup regular expressions
    self.imageRegex = "<img src=\".*\" width=\"\\d*\" height=\"\\d*\" alt=\".*\" title=\".*\" />"
    self.linkRegex =  "/index.cfm\\?pid=\\d*&amp;pk=\\d*"
    self.hrefRegex = "<a href=\""+self.linkRegex+"\">"
    self.headerRegex ="<strong>.+</strong>\\s*.*\\s*</a>"
    self._regEx_extractVideoThumbnail = re.compile("<div class=\"videoPreview\">\\s*"+self.hrefRegex+"\\s*"+self.imageRegex+"\\s*</a>\\s*<span>\\s*"+self.hrefRegex+"\\s*"+self.headerRegex)
    self._regEx_extractTargetLink = re.compile(self.linkRegex);
    self._regEx_extractVideoID = re.compile("pk=\\d*");
    self._regEx_extractVideoLink = re.compile("http://.*.(mp4|flv)");
    self._regEx_extractPictureLink = re.compile("http://.*.jpg");
    self._regEx_extractHeader = re.compile(self.headerRegex);
    ##end setup
    
    ##setup categories
    self.categories = (
      GalleryObject(0,"Neuste Videos","http://www.gamestar.de/index.cfm?pid=1589&ci=latest","http://images.gamestar.de/images/idgwpgsgp/bdb/2018270/b144x81.jpg"),
      GalleryObject(1,"Test-Videos","http://www.gamestar.de/index.cfm?pid=1589&ci=17","http://images.gamestar.de/images/idgwpgsgp/bdb/2018272/b144x81.jpg"),
      GalleryObject(2,"Preview-Videos","http://www.gamestar.de/index.cfm?pid=1589&ci=18","http://images.gamestar.de/images/idgwpgsgp/bdb/2018269/b144x81.jpg"),
      GalleryObject(3,"Video-Specials","http://www.gamestar.de/index.cfm?pid=1589&ci=20","http://images.gamestar.de/images/idgwpgsgp/bdb/2018270/b144x81.jpg"),
      GalleryObject(4,"Quickplay","http://www.gamestar.de/index.cfm?pid=1589&ci=19","http://images.gamestar.de/images/idgwpgsgp/bdb/2016676/b144x81.jpg"),
      GalleryObject(5,"Multiplayer-Duelle","http://www.gamestar.de/index.cfm?pid=1589&ci=22","http://images.gamestar.de/images/idgwpgsgp/bdb/2016431/b144x81.jpg"),
      GalleryObject(6,"Server Down Show","http://www.gamestar.de/index.cfm?pid=1589&ci=15","http://images.gamestar.de/images/idgwpgsgp/bdb/2018271/b144x81.jpg"),
      GalleryObject(7,"Public Viewing","http://www.gamestar.de/index.cfm?pid=1589&ci=37","http://images.idgentertainment.de/images/idgwpgsgp/bdb/2121485/b144x81.jpg"),
      GalleryObject(8,"Technik-Checks","http://www.gamestar.de/index.cfm?pid=1589&ci=32","http://images.gamestar.de/images/idgwpgsgp/bdb/2018270/b144x81.jpg"),
      GalleryObject(9,"Boxenstopp","http://www.gamestar.de/index.cfm?pid=1589&ci=2","http://images.gamestar.de/images/idgwpgsgp/bdb/2018274/b144x81.jpg")
      )
    ##endregion
    
  def buildCategoryMenu(self):
    for categorie in self.categories:
      self.gui.buildCategoryLink(categorie);
  
  def builCategoryMenu(self, link, forcePrecaching):
    rootDocument = self.loadPage(link)
    for videoThumbnail in self._regEx_extractVideoThumbnail.findall(rootDocument):
      try:
        videoID = self._regEx_extractVideoID.search(videoThumbnail).group().replace("pk=","");
        header = self._regEx_extractHeader.search(videoThumbnail).group();
        header = re.sub("(<strong>)|(</strong>)|(</a>)", "", header);
        header = re.sub("\\s+", " ", header);
        
        self.gui.log(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
        configDoc = self.loadPage(self.rootLink+"/emb/getVideoData.cfm?vid="+videoID);
        videoLink = unicode(self._regEx_extractVideoLink.search(configDoc).group());
        thumbnailLink =unicode(self._regEx_extractPictureLink.search(configDoc).group());
        
        self.gui.buildVideoLink(VideoObject(header,videoLink,thumbnailLink),forcePrecaching);
      except:
        pass;
    
    
      
  def loadPage(self,url):
    try:
      safe_url = url.replace( " ", "%20" ).replace("&amp;","&")
      sock = urllib.urlopen( safe_url )
      doc = sock.read()
      if doc:
        return doc
      else:
        return ''
    except:
      return ''