#-*- coding:utf-8 -*-
import json

from django.shortcuts import get_object_or_404, render
from django.http import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,datetime
from django.db.models import Q
from django.db import connection
from django.template import RequestContext 
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from UUBlog.core.ubasetemplateView import UBaseTemplateView
from UUBlog.common import pub,utility

from UUBlog.models import *
from UUBlog.uu.ubaseblog import *

from UUBlog.uu.ubaseadmin import UBaseAdminView


class BaseView(UBaseAdminView):
    def GetContext(self, **kwargs):

        self.template_name="admin/setting/base.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        if self.HasPostData("ok"):
            self.UpdateOption("title",self.GetPostData("title"))
            self.UpdateOption("description",self.GetPostData("description"))
            self.UpdateOption("announcement",self.GetPostData("announcement"))

            
            self.UpdateOption("timezone",self.GetPostData("timezone"))
            
            datetimeformat_custom=self.GetPostData("datetimeformat_custom")

            if datetimeformat_custom!="":
                self.UpdateOption("datetimeformat",datetimeformat_custom)
            else:
                self.UpdateOption("datetimeformat",self.GetPostData("datetimeformat"))

            self.UpdateOption("email",self.GetPostData("email"))

            self.UpdateOption("close_site",self.GetPostData("close_site",False))
            self.UpdateOption("close_info",self.GetPostData("close_info"))

            self.UpdateOption("icp",self.GetPostData("icp"))
            self.UpdateOption("copyright",self.GetPostData("copyright"))
         


        return locals()

class AvatarView(UBaseAdminView):
    def GetContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        self.template_name="admin/setting/avatar.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        #000/00/01
        if self.HasPostData("ok") and self.request.FILES['avatar']:
            avatarPath=("%d" %self.currentBlog.id).rjust(7,"0")
            dir1=avatarPath[0:3]
            dir2=avatarPath[3:5]
            fileName=avatarPath[5:7]
            path="%s/%s/%s/" %("blog/avatar",dir1,dir2)

            self.currentBlog.avatar=pub.SaveFile(self.request.FILES['avatar'],path,fileName)[0]
      
            self.currentBlog.save()


        return locals()

class TemplateView(UBaseAdminView):
    def GetContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))
        skins=["default","temp1"]
        self.template_name="admin/template.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        if self.HasPostData("ok"):
            self.currentBlog.template=self.GetPostData("template")
           
            self.currentBlog.save()

        return locals()

class ContentView(UBaseAdminView):
    def GetContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        self.template_name="admin/setting/content.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        if self.HasPostData("ok"):
            
            self.UpdateOption("index_pagesize",utility.ToInt(self.GetPostData("index_pagesize"),20))
            self.UpdateOption("cat_pagesize",utility.ToInt(self.GetPostData("cat_pagesize"),20))
            self.UpdateOption("tag_pagesize",utility.ToInt(self.GetPostData("tag_pagesize"),20))
            self.UpdateOption("search_pagesize",utility.ToInt(self.GetPostData("search_pagesize"),20))

            self.UpdateOption("admin_pagesize",utility.ToInt(self.GetPostData("admin_pagesize"),20))


            self.UpdateOption("index_template",self.GetPostData("index_template"))
            self.UpdateOption("index_sidebar",self.GetPostData("index_sidebar"))

            self.UpdateOption("cat_template",self.GetPostData("cat_template"))
            self.UpdateOption("cat_sidebar",self.GetPostData("cat_sidebar"))

            self.UpdateOption("tag_template",self.GetPostData("tag_template"))
            self.UpdateOption("tag_sidebar",self.GetPostData("tag_sidebar"))

            self.UpdateOption("search_template",self.GetPostData("search_template"))
            self.UpdateOption("search_sidebar",self.GetPostData("search_sidebar"))

            #文章页模板、文章页侧边栏
            self.UpdateOption("post_template",self.GetPostData("post_template"))
            self.UpdateOption("post_sidebar",self.GetPostData("post_sidebar"))

            #page页模板、page页侧边栏
            self.UpdateOption("page_template",self.GetPostData("page_template"))
            self.UpdateOption("page_sidebar",self.GetPostData("page_sidebar"))

            self.UpdateOption("sidebar_float",self.GetPostData("sidebar_float","right"))


        return locals()

class CommentView(UBaseAdminView):
    def GetContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        self.template_name="admin/setting/comment.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        if self.HasPostData("ok"):
            self.UpdateOption("comment_open",self.GetPostData("comment_open",False))
            self.UpdateOption("comment_interval",self.GetPostData("comment_interval",30))
            self.UpdateOption("comment_check",self.GetPostData("comment_check",False))
            self.UpdateOption("comment_code",self.GetPostData("comment_code",False))
            self.UpdateOption("comment_paging",self.GetPostData("comment_paging",False))
            self.UpdateOption("comment_pagesize",self.GetPostData("comment_pagesize",20))
            self.UpdateOption("comment_order",self.GetPostData("comment_order",True))
           


        return locals()


class AttachmentView(UBaseAdminView):
    def GetContext(self, **kwargs):

        self.template_name="admin/setting/attach.html"

        return locals()

    def PostContext(self, **kwargs):
        if self.HasPostData("ok"):
           
          
            self.UpdateOption("filetype_image",self.GetPostData("filetype_image"))
            self.UpdateOption("filetype_media",self.GetPostData("filetype_media"))
            self.UpdateOption("filetype_file",self.GetPostData("filetype_file"))
            self.UpdateOption("filetype_other",self.GetPostData("filetype_other"))

           
        return locals()




class OtherView(UBaseAdminView):
    def GetContext(self, **kwargs):

        self.template_name="admin/setting/other.html"

        return locals()

    def PostContext(self, **kwargs):
        uid=int(kwargs.get("uid",0))

        if self.HasPostData("ok"):
           
          
            self.UpdateOption("site_title",self.GetPostData("site_title"))
            self.UpdateOption("site_keywords",self.GetPostData("site_keywords"))
            self.UpdateOption("site_description",self.GetPostData("site_description"))

            self.UpdateOption("header_html",self.GetPostData("header_html"))
            self.UpdateOption("footer_html",self.GetPostData("footer_html"))

           
        return locals()






























