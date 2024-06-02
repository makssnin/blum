from pyautogui import *
import pygetwindow as gw
import time
import keyboard
import random
from pynput.mouse import Button, Controller

mouse = Controller()
time.sleep(0.5)

def click(x, y):
    mouse.position = (x, y + random.randint(1, 3))
    mouse.press(Button.left)
    mouse.release(Button.left)

window_name = input('\n[✅] | Crypto Clickers Hub | Нажми 1 ')

if window_name == '1':
    window_name = "TelegramDesktop"

check = gw.getWindowsWithTitle(window_name)
if not check:
    print(f"[❌] | Окно - {window_name} не найдено!")
else:
    print(f"[✅] | Окно найдено - {window_name}\n[✅] | Нажмите 'q' для паузы.")

telegram_window = check[0]
paused = False

# Диапазоны цветов для зеленых бактерий и бомбочек
green_bacteria_range = ((102, 200, 0), (220, 255, 125))  # Задаем точнее диапазон для зеленых бактерий
bomb_range = ((50, 50, 50), (200, 200, 200))  # Примерный диапазон для бомбочек

first_click_time = None

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        if paused:
            print('[✅] | пауза')
        else:
            print('[✅] | ворк')
        time.sleep(0.2)

    if paused:
        continue

    window_rect = (
        telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height
    )

    if telegram_window != []:
        try:
            telegram_window.activate()
        except:
            telegram_window.minimize()
            telegram_window.restore()

    scrn = screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))

    width, height = scrn.size
    pixel_found = False
    if pixel_found == True:
        break

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = scrn.getpixel((x, y))

            # Проверка на зеленые бактерии
            if (b in range(0, 125)) and (r in range(102, 220)) and (g in range(200, 255)):
                screen_x = window_rect[0] + x
                screen_y = window_rect[1] + y

                # Дополнительная проверка, чтобы не кликать по бомбочкам
                # Проверяем небольшую область вокруг пикселя, чтобы убедиться, что это не бомбочка
                is_bomb = False
                try:
                    for bx in range(-5, 6):
                        for by in range(-5, 6):
                            br, bg, bb = scrn.getpixel((x + bx, y + by))
                            if bomb_range[0][0] <= br <= bomb_range[1][0] and bomb_range[0][1] <= bg <= bomb_range[1][1] and bomb_range[0][2] <= bb <= bomb_range[1][2]:
                                is_bomb = True
                                break
                        if is_bomb:
                            break
                except:
                    continue

                if not is_bomb:
                    click(screen_x + 4, screen_y)
                    time.sleep(0.001)
                    pixel_found = True
                    # Если это первый клик, запоминаем время
                    if first_click_time is None:
                        first_click_time = time.time()
                    break

    # Если прошло более 40 секунд с первого клика и кнопка "Play" еще не была нажата
    if first_click_time and time.time() - first_click_time >= 40:
        play_button_x = window_rect[0] + window_rect[2] // 2
        play_button_y = window_rect[1] + window_rect[3] - 100  # Высота 100 px от нижнего края экрана
        click(play_button_x, play_button_y)
        first_click_time = time.time()  # Обновляем время первого клика

print('[✅] | остановлено.')
