from web_english.text import bp, views

bp.add_url_rule("/create", "create", views.create)
bp.add_url_rule("/process_create", "process_create", views.process_create, methods=['POST'])
