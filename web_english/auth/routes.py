from web_english.auth import bp
from web_english.auth import views


bp.add_url_rule("/login", "login", views.login)
bp.add_url_rule("/process-login", "process_login", views.process_login, methods=["POST"])
bp.add_url_rule("/register", "register", views.register)
bp.add_url_rule("/process-register", "process_register", views.process_register, methods=["POST"])
bp.add_url_rule("/logout", "logout", views.logout)
