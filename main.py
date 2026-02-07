import tkinter as tk
import random
from tkinter import messagebox

# --- Константы игры ---
WIDTH = 800  # Ширина окна игры
HEIGHT = 600 # Высота окна игры
SEG_SIZE = 20 # Размер одного квадратика (змейки и еды)
# SPEED будет задаваться пользователем

# --- Цвета ---
BG_COLOR = "#2c3e50" # Темно-синий фон
SNAKE_COLOR = "#27ae60" # Ярко-зеленый
HEAD_COLOR = "#2ecc71" # Чуть светлее для головы
FOOD_COLOR = "#e74c3c" # Красный
TEXT_COLOR = "#ecf0f1" # Светлый текст
GAME_OVER_COLOR = "#c0392b" # Темно-красный для "Game Over"

# --- Класс SnakeGame ---
class SnakeGame:
    def __init__(self, root, speed):
        self.root = root
        self.root.title("Snake Game - Tkinter Edition")
        self.root.resizable(False, False) # Запретить изменение размера окна
        self.speed = speed # Скорость берем из настроек

        # Создаем холст для рисования
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()

        # Стиль для текста
        self.font_score = ("Orbitron", 16, "bold") # Игровой шрифт
        self.font_game_over = ("Orbitron", 32, "bold")

        # Начальное состояние
        self.reset_game()

        # Привязка клавиш
        self.canvas.focus_set() # Фокусируемся на холсте для приема клавиш
        self.canvas.bind("<Key>", self.change_direction)
        
        # Запуск игрового цикла
        self.main_loop()

    def reset_game(self):
        """Сброс всех параметров для начала новой игры"""
        self.score = 0
        self.direction = "Right"
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.food = None
        self.running = True
        self.create_food()
        self.render() # Перерисовать после сброса

    def create_food(self):
        """Создает еду в случайном месте на сетке"""
        while True: # Гарантируем, что еда не появится на змейке
            x = random.randint(0, (WIDTH - SEG_SIZE) // SEG_SIZE -1) * SEG_SIZE
            y = random.randint(0, (HEIGHT - SEG_SIZE) // SEG_SIZE -1) * SEG_SIZE
            if [x,y] not in self.snake:
                self.food = [x, y]
                break

    def change_direction(self, event):
        """Меняет направление, исключая разворот на 180 градусов"""
        key = event.keysym
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        
        if key in ["Up", "Down", "Left", "Right"]:
            if key != opposites.get(self.direction):
                self.direction = key
        elif not self.running and key.lower() == 'r': # Возможность перезапуска
            self.reset_game()


    def move_snake(self):
        """Вычисляет новую позицию головы и двигает хвост"""
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            head_y -= SEG_SIZE
        elif self.direction == "Down":
            head_y += SEG_SIZE
        elif self.direction == "Left":
            head_x -= SEG_SIZE
        elif self.direction == "Right":
            head_x += SEG_SIZE

        new_head = [head_x, head_y]

        # Проверка столкновений
        if (head_x < 0 or head_x >= WIDTH or 
            head_y < 0 or head_y >= HEIGHT or 
            new_head in self.snake[1:]): # Столкновение с собой (кроме хвоста, который будет удален)
            self.running = False
            return

        self.snake.insert(0, new_head)

        # Проверка: съели ли мы еду?
        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            self.score += 1
            self.create_food()
        else:
            # Если не съели, убираем последний сегмент хвоста
            self.snake.pop()

    def render(self):
        """Отрисовка всех объектов на холсте"""
        self.canvas.delete("all") # Очистка кадра
        
        if self.running:
            # Рисуем еду
            self.canvas.create_oval(
                self.food[0], self.food[1], 
                self.food[0] + SEG_SIZE, self.food[1] + SEG_SIZE, 
                fill=FOOD_COLOR, outline=TEXT_COLOR
            )

            # Рисуем змейку
            for i, segment in enumerate(self.snake):
                color = HEAD_COLOR if i == 0 else SNAKE_COLOR # Голова другого цвета
                self.canvas.create_rectangle(
                    segment[0], segment[1], 
                    segment[0] + SEG_SIZE, segment[1] + SEG_SIZE, 
                    fill=color, outline=BG_COLOR # Обводка цветом фона
                )
            
            # Рисуем счет
            self.canvas.create_text(
                WIDTH - 100, 20, text=f"SCORE: {self.score}", 
                fill=TEXT_COLOR, font=self.font_score, anchor="e"
            )
        else:
            # Экран проигрыша
            self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill=GAME_OVER_COLOR, stipple="gray50") # Полупрозрачная заливка
            self.canvas.create_text(
                WIDTH/2, HEIGHT/2 - 30, 
                text=f"GAME OVER", 
                fill=TEXT_COLOR, font=self.font_game_over, justify="center"
            )
            self.canvas.create_text(
                WIDTH/2, HEIGHT/2 + 30,
                text=f"Final Score: {self.score}\nPress 'R' to Restart",
                fill=TEXT_COLOR, font=("Orbitron", 20), justify="center"
            )

    def main_loop(self):
        """Главный цикл управления временем"""
        if self.running:
            self.move_snake()
        
        self.render()
        # Планируем следующий вызов через self.speed миллисекунд
        self.root.after(self.speed, self.main_loop)

# --- Класс для окна настроек ---
class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Настройки игры Snake")
        self.master.geometry("400x250")
        self.master.resizable(False, False)
        self.master.configure(bg="#34495e") # Темно-синий фон для окна настроек

        # Добавляем метку
        tk.Label(master, text="Выберите скорость игры:", 
                 bg="#34495e", fg=TEXT_COLOR, font=("Orbitron", 14, "bold")) \
                 .pack(pady=20)

        # Слайдер для выбора скорости
        self.speed_scale = tk.Scale(master, from_=50, to=500, orient=tk.HORIZONTAL, 
                                     label="Скорость (мс)", length=300, 
                                     bg="#34495e", fg=TEXT_COLOR, troughcolor="#2c3e50",
                                     font=("Orbitron", 10), sliderrelief="flat",
                                     highlightbackground="#34495e")
        self.speed_scale.set(100) # Значение по умолчанию
        self.speed_scale.pack(pady=10)

        # Кнопка "Начать игру"
        tk.Button(master, text="Начать игру", command=self.start_game, 
                  bg="#27ae60", fg="white", font=("Orbitron", 12, "bold"), 
                  relief="flat", padx=15, pady=5) \
                  .pack(pady=20)

    def start_game(self):
        selected_speed = self.speed_scale.get()
        self.master.destroy() # Закрываем окно настроек
        
        # Запускаем игру
        game_root = tk.Tk()
        game = SnakeGame(game_root, selected_speed)
        game_root.mainloop()

# --- Главный запуск приложения ---
if __name__ == "__main__":
    # Для шрифта Orbitron: его нет по умолчанию в Windows/Linux. 
    # Если его нет, то будет использоваться шрифт по умолчанию.
    # Для Windows: можно установить его (файл .ttf), для Linux: установить пакет 'fonts-orbitron'.
    # В противном случае, можно заменить на любой другой доступный шрифт, например "Arial".

    root_settings = tk.Tk()
    settings = SettingsWindow(root_settings)
    root_settings.mainloop()
