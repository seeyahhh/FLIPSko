import random
import tkinter as tk
from PIL import Image, ImageTk
from ENDSCREEN_module import show_end_screen

def load_difficult_mode(canvas):
    # Store image references
    canvas.image_refs = {}

    # Game setup
    matches = ["Lanyard", "Lanyard", "Kwek-kwek", "Kwek-kwek", "Lagoon", "Lagoon", "Fan", "Fan",
               "Tricycle", "Tricycle", "Ferry", "Ferry", "Lrt", "Lrt", "Obelisk", "Obelisk"]
    random.shuffle(matches)
    flipped = []
    matched = []
    first_click = True
    flipping_disabled = False

    # Timer setup
    remaining_time = 91 # add 1 for loading time
    digit_images = {}
    for i in range(10):
        try:
            img = Image.open(f"digits/{i}.png").resize((77, 77))
            digit_images[i] = ImageTk.PhotoImage(img)
            canvas.image_refs[f'digit_{i}'] = digit_images[i]
        except Exception as e:
            digit_images[i] = None

    # Clear canvas
    canvas.delete("all")

    # Background
    try:
        bg_img = Image.open("background/GAMEPLAY.png").resize((1366, 768))
        canvas.image_refs['bg'] = ImageTk.PhotoImage(bg_img)
        canvas.create_image(0, 0, image=canvas.image_refs['bg'], anchor=tk.NW)
    except:
        canvas.create_rectangle(0, 0, 1366, 768, fill="#444")

    # Load card back image
    try:
        back_img = Image.open("cards/BACK.png").resize((108, 175))
        canvas.image_refs['back'] = ImageTk.PhotoImage(back_img)
    except:
        canvas.image_refs['back'] = None

    # Load front images
    front_images = {}
    for name in set(matches):
        try:
            img = Image.open(f"cards/{name.lower()}.png").resize((108, 175))
            photo = ImageTk.PhotoImage(img)
            canvas.image_refs[name] = photo
            front_images[name] = photo
        except:
            front_images[name] = None

    # Load Digit images for timer and background image
    digit_slots = []
    x_start = 150
    y_pos = 50

    # Load timer background image
    try:
        timer_bg_img = Image.open("background/popupBG.png").resize((105, 95))
        canvas.image_refs['timer_bg'] = ImageTk.PhotoImage(timer_bg_img)
        canvas.create_image(x_start - -10, y_pos - 8, image=canvas.image_refs['timer_bg'], anchor=tk.NW)
    except Exception as e:
        print("Timer background image failed:", e)
        
    # Load digit images and place them
    for i in range(2):
        img = digit_images.get(0)
        item = canvas.create_image(x_start + i * 47, y_pos, image=img, anchor=tk.NW)
        digit_slots.append(item)

    # Timer function
    def update_timer():
        nonlocal remaining_time
        if remaining_time > 0:
            remaining_time -= 1
            digits = list(f"{remaining_time:02}")
            for i, d in enumerate(digits):
                digit_img = digit_images.get(int(d), digit_images[0])
                canvas.itemconfig(digit_slots[i], image=digit_img)
            canvas.after(1000, update_timer)
        else:
            canvas.itemconfig(status_label, text="⏰ Time's up!")
            disable_all_cards()
            show_end_screen(canvas, digit_images, 0, "easy")

    def disable_all_cards():
        for _, rect_id, _ in card_buttons:
            canvas.tag_unbind(rect_id, "<Button-1>")

    # Flip Functions
    def flip_card(card_id, value):
        if front_images.get(value):
            canvas.itemconfig(card_id, image=front_images[value])
        else:
            canvas.itemconfig(card_id, image='', fill='white')
            x1, y1, x2, y2 = canvas.bbox(card_id)
            canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=value, fill="black", font=("Helvetica", 14))

    def flip_back():
        for card_id, _ in flipped:
            if canvas.image_refs['back']:
                canvas.itemconfig(card_id, image=canvas.image_refs['back'])
            else:
                canvas.itemconfig(card_id, fill="#888")
        flipped.clear()
        nonlocal flipping_disabled
        flipping_disabled = False

    def check_match():
        nonlocal flipping_disabled
        c1, v1 = flipped[0]
        c2, v2 = flipped[1]
        if v1 == v2:
            matched.extend([c1, c2])
            for card_id in [c1, c2]:
                x1, y1, x2, y2 = canvas.bbox(card_id)
                canvas.create_rectangle(x1, y1, x2, y2, outline="lime", width=5)
            flipped.clear()
            flipping_disabled = False
            if len(matched) == len(matches):
                canvas.itemconfig(status_label, text="🎉 You matched everything!")
                show_end_screen(canvas, digit_images, remaining_time, "difficult")
        else:
            canvas.after(200, flip_back)

    def handle_click(idx):
        nonlocal first_click, flipping_disabled

        if flipping_disabled:
            return

        if first_click:
            for card_id, _, _ in card_buttons:
                if canvas.image_refs['back']:
                    canvas.itemconfig(card_id, image=canvas.image_refs['back'])
            first_click = False
            return

        card_id, _, value = card_buttons[idx]
        if card_id in matched or any(card_id == c[0] for c in flipped):
            return

        flip_card(card_id, value)
        flipped.append((card_id, value))

        if len(flipped) == 2:
            flipping_disabled = True
            canvas.after(300, check_match)

    # Card positions
    positions = [(30, 218), (200, 218), (370, 218), (540, 218), (710, 218), (880, 218), (1050, 218), (1220, 218),
                 (30, 480), (200, 480), (370, 480), (540, 480), (710, 480), (880, 480), (1050, 480), (1220, 480)]

    card_buttons = []
    for i, (x, y) in enumerate(positions):
        card_id = canvas.create_image(x, y, image=canvas.image_refs['back'], anchor=tk.NW)
        rect_id = canvas.create_rectangle(x, y, x + 108, y + 175, fill='', outline='')
        canvas.tag_bind(rect_id, "<Button-1>", lambda e, idx=i: handle_click(idx))
        card_buttons.append((card_id, rect_id, matches[i]))

    # Status text
    status_label = canvas.create_text(683, 750, text="Click any card to start",
                                      font=("Helvetica", 16), fill="white")

    # Popup Logic
    popup_elements = []
    popup_open = False

    def close_popup():
        nonlocal popup_open
        for item in popup_elements:
            canvas.delete(item)
        popup_elements.clear()
        popup_open = False

    def on_end_click(event=None):
        close_popup()
        canvas.event_generate("<<ToDifficultyPage>>")  

    def on_play_again_click(event=None):
        close_popup()
        load_difficult_mode(canvas)  # Restart difficult mode

    #def on_next_level_click(event=None):
        #close_popup()
        # Define next step here if any
        #pass

    def open_settings_popup(event=None):
        nonlocal popup_open
        if popup_open:
            close_popup()
            return
        popup_open = True

        overlay = canvas.create_rectangle(0, 0, 1366, 768, fill='black', stipple='gray50', tags="popup_overlay")
        popup_elements.append(overlay)

        try:
            triangle_img = Image.open("background/popupBG.png").resize((991, 369))
            canvas.image_refs['popup_triangle'] = ImageTk.PhotoImage(triangle_img)
            popup_triangle = canvas.create_image(683, 384, image=canvas.image_refs['popup_triangle'], anchor=tk.CENTER)
            popup_elements.append(popup_triangle)
        except Exception as e:
            print("Failed to load popup triangle image:", e)
            popup_bg = canvas.create_rectangle(450, 250, 916, 518, fill="#222", outline="white", width=3)
            popup_elements.append(popup_bg)

        try:
            popup_title_img = Image.open("label/flipskoTitle.png")
            canvas.image_refs['popup_title'] = ImageTk.PhotoImage(popup_title_img)
            popup_title = canvas.create_image(683, 320, image=canvas.image_refs['popup_title'], anchor=tk.CENTER)
            popup_elements.append(popup_title)
        except Exception as e:
            print("Title image failed:", e)

        try:
            end_img = Image.open("buttons/endB.png").resize((272, 124))
            end_photo = ImageTk.PhotoImage(end_img)
            canvas.image_refs['end_btn'] = end_photo
            end_btn = canvas.create_image(527, 450, image=end_photo)
            popup_elements.append(end_btn)
            canvas.tag_bind(end_btn, "<Button-1>", on_end_click)
        except Exception as e:
            print("Failed to load End button image:", e)

        try:
            play_again_img = Image.open("buttons/playAgainB.png").resize((312, 122))
            play_again_photo = ImageTk.PhotoImage(play_again_img)
            canvas.image_refs['play_again_btn'] = play_again_photo
            play_again_btn = canvas.create_image(839, 450, image=play_again_photo)
            popup_elements.append(play_again_btn)
            canvas.tag_bind(play_again_btn, "<Button-1>", on_play_again_click)
        except Exception as e:
            print("Failed to load Play Again button image:", e)

        #try:
            #next_level_img = Image.open("buttons/nextlvlB.png").resize((292, 126))
            #next_level_photo = ImageTk.PhotoImage(next_level_img)
            #canvas.image_refs['next_level_btn'] = next_level_photo
            #next_level_btn = canvas.create_image(990, 450, image=next_level_photo)
            #popup_elements.append(next_level_btn)
            #canvas.tag_bind(next_level_btn, "<Button-1>", on_next_level_click)
        #except Exception as e:
            #print("Failed to load Next Level button image:", e)

        # Make sure the settings button stays above the popup overlay
        canvas.tag_raise(setting_btn)

    def toggle_settings_popup(event=None):
        if popup_open:
            close_popup()
        else:
            open_settings_popup()

    # Header UI elements (Settings button, Title, Difficulty Label)
    try:
        setting_img = Image.open("buttons/settingB.png").resize((96, 101))
        canvas.image_refs['setting'] = ImageTk.PhotoImage(setting_img)
        setting_btn = canvas.create_image(100, 90, image=canvas.image_refs['setting'], anchor=tk.CENTER)
        canvas.tag_bind(setting_btn, "<Button-1>", toggle_settings_popup)
    except Exception as e:
        print("Setting button failed:", e)
        setting_btn = None

    try:
        title_img = Image.open("label/flipskoTitle.png")
        canvas.image_refs['title'] = ImageTk.PhotoImage(title_img)
        canvas.create_image(683, 90, image=canvas.image_refs['title'], anchor=tk.CENTER)
    except Exception as e:
        print("Title image failed:", e)

    try:
        label_img = Image.open("label/difficultL.png").resize((237, 98))
        canvas.image_refs['difficult_label'] = ImageTk.PhotoImage(label_img)
        canvas.create_image(1200, 90, image=canvas.image_refs['difficult_label'], anchor=tk.CENTER)
    except Exception as e:
        print("Difficult label failed:", e)

    # Start the timer
    update_timer()