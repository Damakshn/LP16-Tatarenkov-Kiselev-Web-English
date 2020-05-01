from web_english.text import bp, views

bp.add_url_rule("/create", "create", views.create)
bp.add_url_rule("/process_create", "process_create",
                views.process_create, methods=['POST'])
bp.add_url_rule("/texts_list", "texts_list", views.texts_list)
bp.add_url_rule("/edit_text/<text_id>", "edit_text", views.edit_text)
bp.add_url_rule("/process_edit_text", "process_edit_text",
                views.process_edit_text, methods=['POST'])
bp.add_url_rule("/progress/<text_id>", "progress", views.progress_bar)
bp.add_url_rule('/listen/<int:text_id>', "listen", views.listen)
bp.add_url_rule('/audio/<int:text_id>', "serve_audio", views.serve_audio)
bp.add_url_rule("/learning", "learning_list", views.text_list_for_student)
