from web_english.text import bp, views

bp.add_url_rule("/create", "create", views.create)
bp.add_url_rule("/process_create", "process_create",
                views.process_create, methods=['POST'])
bp.add_url_rule('/listen/<int:text_id>', "listen", views.listen)
bp.add_url_rule('/audio/<int:text_id>', "serve_audio", views.serve_audio)
