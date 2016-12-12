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
import urllib, re, time,traceback;
from ui import *;


class Source(object):
  def __init__(self, gui):
    self.gui = gui;
    
    ##setup regular expressions
    self.regexVideoObject = re.compile("<a href=\"(/videos/.*?,\\d*?\\.html)\" title=\"(.*?)\">\\s*<img src=\"(.*?)\"");
    self.regexLink = re.compile("/videos/media,\\d+?(,(\\d)){0,1}\\.html");
    ##end setup
    
  def getCategories(self):
    categories={};
    for key in self.categories.keys():
      categories[key]=self.categories[key].pictureLink;
    return categories;
  
  def getVideoLinkObjects(self, categorie):
    videoObjects = [];
    if categorie in self.categories:
      categorie = self.categories[categorie];
      self.gui.log(categorie.url);
      rootDocument = self.loadPage(categorie.url);

      videoIds = set();

      for match in self.regexVideoObject.finditer(rootDocument):
        
        title = match.group(2);
        thumbnailLink = match.group(3);
        if(not thumbnailLink.startswith('http://')):
          thumbnailLink = thumbnailLink.replace("//",'http://');
        videoPageLink = self.rootLink+match.group(1);
        self.gui.log(videoPageLink);
        videoPage=self.loadPage(videoPageLink);
        matches= list(self.regexLink.finditer(videoPage));
        if len(matches) == 0:
          continue;
        if len(matches) == 1:
          link = self.rootLink+matches[0].group(0);
        else:
          links = {}
          for match in self.regexLink.finditer(videoPage):
            quality = match.group(1);
            link = self.rootLink+match.group(0);
            self.gui.log("Quality %s: %s"%(quality,link));
            links[quality]=link
          qualitiy = sorted(links.keys(),reverse = True)[0];
          link=links[qualitiy]
        videoObjects.append(VideoObject(title, link, thumbnailLink, self.shortName));
    return videoObjects;


  def loadVideoObject(self, videoID):
    link = self.configPage%videoID;
    self.gui.log(link);
    configDoc = self.loadPage(link).decode('utf-8');
    videoLink = self._regEx_extractVideoLink.search(configDoc).group();
    videoLink = self.replaceXmlEntities(videoLink);
    thumbnailLink = self._regEx_extractPictureLink.search(configDoc).group();
    title = self._regEx_extractTitle.search(configDoc).group(1);
    title = self.transformHtmlCodes(title);
    
    if(not thumbnailLink.startswith('http://')):
      thumbnailLink = thumbnailLink.replace("//",'http://');
    thumbnailLink = thumbnailLink;
    
    return VideoObject(title, videoLink, thumbnailLink, self.shortName)

  @classmethod
  def replaceXmlEntities(self, link):
    entities = (
        ("%3A",":"),("%2F","/"),("%3D","="),("%3F","?"),("%26","&")
      );
    for entity in entities:
       link = link.replace(entity[0],entity[1]);
    return link;

  @classmethod
  def transformHtmlCodes(self,string):
    replacements = (
      (u'Ä', u'&Auml;'),
      (u'Ü', u'&Uuml;'),
      (u'Ö', u'&Ouml;'),
      (u'ä', u'&auml;'),
      (u'ü', u'&uuml;'),
      (u'ö', u'&ouml;'),
      (u'ß', u'&szlig;'),
      (u'\"',u'&#034;'),
      (u'\"',u'&quot;'),
      (u'\'',u'&#039;'),
      (u'&', u'&amp;'),
      (u' ', u'&nbsp;')
    )
    for replacement in replacements:
      string = string.replace(replacement[1],replacement[0]);
    return string;

  @classmethod
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
