window_class = window.get_active_class().lower()

if "gnome-terminal" not in window_class:
    keyboard.send_keys("<ctrl>+c")
else:
    keyboard.send_keys("<super>+c")
