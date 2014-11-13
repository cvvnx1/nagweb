#encoding=UTF8

from flask import session, request, redirect, url_for
from flask.ext.classy import FlaskView, route
from __header__ import AdminView
from www.lib.host import *
from www.form import Form, FormElementField, FormValidatorAbstract

class View(FlaskView):
    route_base = "/host"
    def before_request(self, name):
        self._view = AdminView()

class ListView(View):
    '''
    List hosts and hostgroup
    '''
    @route("/list", endpoint="host_list")
    def get(self):
        self._view.assign("getHostgroupMember", getHostgroupMember)
        return self._view.render("host_list", hosts=getHosts(), hostgroups=getHostgroups())

#--- Edit框架基础类

class EditDetailView(View):
    '''
    Base class for EditHostView and EditHostgroupView
    '''
    def before_request(self, name):
        super(EditDetailView, self).before_request(name)
        self._id = request.args.get("id")

#--- EditHost类

class HostValidator(FormValidatorAbstract):
    def rules(self):
        return {
            "host_name":{"required":True},
            "alias":{"required":True},
            "address":{"required":True},
            "hostgroups":{"required":True}
        }

class EditHostView(EditDetailView):
    def before_request(self, name):
        super(EditHostView, self).before_request(name)
        if self._id is None:
            return self._view.error("No id input!")
        self._host = getHostById(self._id)
        self._host.hostgroup_name = []

    def _initForm(self, data=None):
        self._form = Form("edit_host", request, session)
        self._form.add_field("hidden", "id", "id")
        self._form.add_field("text", "名称", "host_name", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "别名", "alias", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "地址", "address", data={"attributes":{"class":"m-wrap large"}})
        _templateList = []
        for _hosttemplate in getHosttemplates():
            _templateList.append((_hosttemplate.name, _hosttemplate.name))
        self._form.add_field("select", "模板", "use", data={"attributes":{"class":"m-wrap large"}, "option":_templateList, "value":self._host.use})
        self._form.add_field("text", "注释", "notes", data={"attributes":{"class":"m-wrap large"}})
        _hostgroupList = []
        for _hostgroup in getHostgroups():
            _hostgroupList.append((_hostgroup.hostgroup_name, _hostgroup.hostgroup_name))
        self._form.add_field("checkbox", "所属组", "hostgroups", data={"option": _hostgroupList})
        self._form.set_value(data)
        self._form.add_validator(HostValidator)

    @route("/edithost", methods=["GET", "POST"], endpoint="host_edit")
    def editHost(self):
        if request.method != "POST":
            try:
                self._initForm(self._host)
            except Exception, e:
                return self._view.error(str(e))
            return self._view.render("host_edit", form=self._form)

        try:
            self._initForm(dict(request.form))
        except Exception, e:
            return self._view.error(str(e))

        if self._form.validate():
            data = {
                "host_name":request.form["host_name"],
                "alias":request.form["alias"],
                "address":request.form["address"],
                "use":request.form["use"],
                "notes":request.form["notes"],
                "hostgroups":request.form.getlist("hostgroups")
            }
            if updateHost(request.form["id"], data):
                return redirect(url_for("host_list"))
            else:
                return self._view.error("'{}'更新出错，请手动检查".format(request.form["host_name"]))

#--- EditHostgroup类

class HostgroupValidator(FormValidatorAbstract):
    def rules(self):
        return {
            "host_name":{"required":True},
            "alias":{"required":True},
            "address":{"required":True},
        }

class EditHostgroupView(EditDetailView):
    def before_request(self, name):
        super(EditHostgroupView, self).before_request(name)
        if self._id is None:
            return self._view.error("No id input!")
        self._hostgroup = getHostgroupById(self._id)

    def _initForm(self, data=None):
        self._form = Form("edit_hostgroup", request, session)
        self._form.add_field("hidden", "id", "id")
        self._form.add_field("text", "名称", "hostgroup_name", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "别名", "alias", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "注释", "notes", data={"attributes":{"class":"m-wrap large"}})
        self._form.set_value(data)
        self._form.add_validator(HostgroupValidator)

    @route("/edithostgroup", methods=["GET", "POST"], endpoint="hostgroup_edit")
    def editHostgroup(self):
        if request.method != "POST":
            try:
                self._initForm(self._hostgroup)
            except Exception, e:
                return self._view.error(str(e))
            return self._view.render("hostgroup_edit", form=self._form)

        try:
            self._initForm(dict(request.form))
        except Exception, e:
            return self._view.error(str(e))

        if self._form.validate():
            data = {
                "hostgroup_name":request.form["hostgroup_name"],
                "alias":request.form["alias"],
                "notes":request.form["notes"]
            }
            if updateHostgroup(request.form["id"], data):
                return redirect(url_for("host_list"))
            else:
                return self._view.error("'{}'更新出错，请手动检查".format(request.form["hostgroup_name"]))

#--- AddHost类

class AddHostView(View):
    def _initForm(self, data=None):
        self._form = Form("add_host", request, session)
        self._form.add_field("text", "名称", "host_name", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "别名", "alias", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "地址", "address", data={"attributes":{"class":"m-wrap large"}})
        _templateList = []
        for _hosttemplate in getHosttemplates():
            _templateList.append((_hosttemplate.name, _hosttemplate.name))
        self._form.add_field("select", "模板", "use", data={"attributes":{"class":"m-wrap large"}, "option":_templateList})
        self._form.add_field("select", "模板", "use", data={"attributes":{"class":"m-wrap large"}, "option":_templateList})
        self._form.add_field("text", "注释", "notes", data={"attributes":{"class":"m-wrap large"}})
        _hostgroupList = []
        for _hostgroup in getHostgroups():
            _hostgroupList.append((_hostgroup.hostgroup_name, _hostgroup.hostgroup_name))
        self._form.add_field("checkbox", "所属组", "hostgroups", data={"value": "", "option": _hostgroupList})
        self._form.set_value(data)
        self._form.add_validator(HostValidator)

    @route("/addhost", methods=["GET", "POST"], endpoint="host_add")
    def addHost(self):
        try:
            self._initForm()
        except Exception, e:
            return self._view.error(str(e))

        if request.method == "POST":
            if self._form.validate():
                data = {
                    "host_name":request.form["host_name"],
                    "alias":request.form["alias"],
                    "address":request.form["address"],
                    "use":request.form["use"],
                    "notes":request.form["notes"],
                    "hostgroups":request.form.getlist("hostgroups")
                }
                if updateHost("", data):
                    return redirect(url_for("host_list"))
                else:
                    return self._view.error("'{}'添加出错，请手动检查".format(request.form["host_name"]))
        return self._view.render("host_edit", form=self._form)

#--- AddHostgroup类

class AddHostgroupView(View):
    def _initForm(self, data=None):
        self._form = Form("edit_hostgroup", request, session)
        self._form.add_field("text", "名称", "hostgroup_name", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "别名", "alias", data={"attributes":{"class":"m-wrap large"}})
        self._form.add_field("text", "注释", "notes", data={"attributes":{"class":"m-wrap large"}})
        self._form.set_value(data)
        self._form.add_validator(HostgroupValidator)

    @route("/addhostgroup", methods=["GET", "POST"], endpoint="hostgroup_add")
    def addHostgroup(self):
        try:
            self._initForm()
        except Exception, e:
            return self._view.error(str(e))

        if request.method == "POST":
            if self._form.validate():
                data = {
                    "hostgroup_name":request.form["hostgroup_name"],
                    "alias":request.form["alias"],
                    "notes":request.form["notes"]
                }
                if updateHostgroup("", data):
                    return redirect(url_for("host_list"))
                else:
                    return self._view.error("'{}'添加出错，请手动检查".format(request.form["hostgroup_name"]))
        return self._view.render("hostgroup_edit", form=self._form)
