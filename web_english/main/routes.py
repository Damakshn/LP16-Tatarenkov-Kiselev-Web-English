from web_english.main import bp, views


bp.add_url_rule("/", "index", views.index)
bp.add_url_rule("/learning/<text_id>", "learning", views.learning)
