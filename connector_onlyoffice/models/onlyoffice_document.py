#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class OnlyofficeDocument(models.Model):
    _inherit = "onlyoffice.document"

    name = fields.Char("Name", required=True)

    @property
    def document_server_url(self):
        url = self.env["ir.property"].search([("name", "=", "onlyoffice_url")])
        if not url:
            raise ValidationError(_("Couldn't find a callback URL for Onlyoffice DS server"))

    def button_edit_document(self):
        js_src = """
        var docEditor;

        var innerAlert = function (message) {
            if (console && console.log)
            console.log(message);
        };

        var onAppReady = function () {
            innerAlert("Document editor ready");
        };

        var onDocumentStateChange = function (event) {
        var title = document.title.replace(/\*$/g, "");
            document.title = title + (event.data ? "*" : "");
        };

        var onRequestEditRights = function () {
            location.href = location.href.replace(RegExp("mode=view\&?", "i"), "");
        };

        var onError = function (event) {
            if (event)
                innerAlert(event.data);
        };

        var onOutdatedVersion = function (event) {
            location.reload(true);
        };

        var connectEditor = function () {

        config = {{ cfg | safe }}
        config.width = "100%";
        config.height = "100%";
        config.events = {
            'onAppReady': onAppReady,
            'onDocumentStateChange': onDocumentStateChange,
            'onRequestEditRights': onRequestEditRights,
            'onError': onError,
            'onOutdatedVersion': onOutdatedVersion,
        };

        {% if history and historyData %}

        config.events['onRequestHistory'] = function () {
            docEditor.refreshHistory({{ history | safe }});
        };
        config.events['onRequestHistoryData'] = function (event) {
            var ver = event.data;
            var histData = {{ historyData | safe }};
            docEditor.setHistoryData(histData[ver]);
        };
        config.events['onRequestHistoryClose'] = function () {
            document.location.reload();
        };

        {% endif %}

        docEditor = new DocsAPI.DocEditor("iframeEditor", config);

        fixSize();
        };

        var fixSize = function () {
            var wrapEl = document.getElementsByClassName("form");
            if (wrapEl.length) {
                wrapEl[0].style.height = screen.availHeight + "px";
                window.scrollTo(0, -1);
                wrapEl[0].style.height = window.innerHeight + "px";
            }
        };

        if (window.addEventListener) {
            window.addEventListener("load", connectEditor);
            window.addEventListener("resize", fixSize);
        } else if (window.attachEvent) {
            window.attachEvent("onload", connectEditor);
            window.attachEvent("onresize", fixSize);
        }
        """

        return self.env.todo_template.render({
            "onlyoffice_editor", {
                "documentserver_url": self.url,
            }
        })