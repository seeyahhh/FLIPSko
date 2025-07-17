import tkinter as tk
from tkinter import CENTER
from PIL import Image, ImageTk

def show_end_screen(canvas, digit_images, remaining_time, difficulty):
    canvas.delete("all")

    canvas.image_refs = {}

    # Background
    try:
        bg_img = Image.open("background/difficultyBG1.png").resize((1366, 768))
        canvas.image_refs["end_bg"] = ImageTk.PhotoImage(bg_img)
        canvas.create_image(0, 0, image=canvas.image_refs["end_bg"], anchor=tk.NW)
    except Exception as e:
        print("End screen background failed:", e)

    # Timer and StarsBackground

    try:
        popup_bg_img = Image.open("background/popupBG.png").resize((500, 300))  # size may be adjusted
        canvas.image_refs['popup_bg'] = ImageTk.PhotoImage(popup_bg_img)
        canvas.create_image(433, 240, image=canvas.image_refs['popup_bg'], anchor=tk.NW)
    except Exception as e:
        print("Timer background image failed:", e)

    # Title
    try:
        title_img = Image.open("label/flipskoTitle.png").resize((600, 150))
        canvas.image_refs["title"] = ImageTk.PhotoImage(title_img)
        canvas.create_image(683, 170, image=canvas.image_refs["title"], anchor=tk.CENTER)
    except Exception as e:
        print("End screen title failed:", e)

    # Timer label
    digits = list(f"{remaining_time:02}")
    x_start = 660
    for i, d in enumerate(digits):
        digit_img = digit_images.get(int(d))
        if digit_img:
            canvas.create_image(x_start + i * 50, 320, image=digit_img, anchor=CENTER)

    # Stars
    if remaining_time > 59:
        star_count = 3
    elif remaining_time > 29:
        star_count = 2
    elif remaining_time > 0:
        star_count = 1
    else:
        star_count = 0

    star_positions = [835, 685, 535]

    for i in range(star_count):
        try:
            star = Image.open("label/star.png").resize((200, 140))
            canvas.image_refs[f'star_{i}'] = ImageTk.PhotoImage(star)
            canvas.create_image(star_positions[i], 440, image=canvas.image_refs[f'star_{i}'], anchor=CENTER)
        except Exception as e:
            print(f"Star image {i} failed:", e)

    # Button Functions
    def close_popup():
        canvas.delete("all")  

    def on_end_click(event=None):
        close_popup()
        canvas.event_generate("<<ToDifficultyPage>>")

    def on_play_again_click(event=None):
        close_popup()
        if difficulty == "easy":
            from EASYMODE_module import load_easy_mode
            load_easy_mode(canvas, show_end_screen)
        elif difficulty == "normal":
            from NORMALMODE_module import load_normal_mode
            load_normal_mode(canvas, show_end_screen)
        elif difficulty == "difficult":
            from DIFFICULTMODE_module import load_difficult_mode
            load_difficult_mode(canvas, show_end_screen)

    def on_next_level_click(event=None):
        close_popup()
        if difficulty == "easy":
            from NORMALMODE_module import load_normal_mode
            load_normal_mode(canvas, show_end_screen)
        elif difficulty == "normal":
            from DIFFICULTMODE_module import load_difficult_mode
            load_difficult_mode(canvas)
        elif difficulty == "difficult":
            canvas.event_generate("<<ToDifficultyPage>>")  

    # Buttons
    button_functions = [on_end_click, on_play_again_click, on_next_level_click]
    btn_names = ['endB', 'playAgainB', 'nextlvlB']
    for i, name in enumerate(btn_names):
        try:
            btn_img = Image.open(f"buttons/{name}.png").resize((250, 100))
            canvas.image_refs[name] = ImageTk.PhotoImage(btn_img)
            x = 442 + i * 250
            btn_id = canvas.create_image(x, 600, image=canvas.image_refs[name], anchor=CENTER)
            canvas.tag_bind(btn_id, "<Button-1>", button_functions[i])
        except Exception as e:
            print(f"Button {name} failed:", e)
