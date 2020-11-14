from flask import flash, redirect, url_for
from flask_login import current_user
from flask_admin import Admin, AdminIndexView

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_admin:
            return current_user.is_authenticated
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            flash('Denied to access', 'danger') #直接URLに/adminを入れた場合に対応
            return redirect(url_for("main.home"))