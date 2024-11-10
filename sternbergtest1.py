import turtle
import random
import time
import datetime
import os

class Button:
    def __init__(self, text, center_x, center_y, padding, onclick_function=None):
        self.text = text
        self.center_x = center_x
        self.center_y = center_y
        self.padding = padding
        self.onclick = onclick_function
        
        # Create a turtle to measure the text size
        measurer = turtle.Turtle()
        measurer.hideturtle()
        measurer.penup()
        measurer.write(self.text, align="center", font=("Arial", 12, "bold"))
        text_width = measurer.xcor() * 2
        self.width = text_width + padding * 6  # Increase the padding to make the button wider
        self.height = 20 + padding * 2
        measurer.clear()
        
        # Calculate button coordinates
        self.x1 = center_x - self.width / 2
        self.y1 = center_y + self.height / 2
        self.x2 = center_x + self.width / 2
        self.y2 = center_y - self.height / 2
        
    def draw(self, screen):
        screen.tracer(0)
        button = turtle.Turtle()
        button.hideturtle()
        button.penup()
        button.goto(self.x1, self.y1)
        
        button.pendown()
        button.fillcolor("lightgray")
        button.begin_fill()
        for _ in range(2):
            button.forward(self.width)
            button.right(90)
            button.forward(self.height)
            button.right(90)
        button.end_fill()
        
        button.penup()
        button.goto(self.center_x, self.center_y - 10)
        button.write(self.text, align="center", font=("Arial", 12, "bold"))
        
        screen.update()
        
    def is_clicked(self, x, y):
        return (self.x1 <= x <= self.x2 and 
                self.y2 <= y <= self.y1)

def setup_screen():
    screen = turtle.Screen()
    screen.title("Sternberg test")
    screen.bgcolor("white")
    screen.setup(width=600*1.2, height=400*1.2)
    screen.tracer(0)
    return screen

def clear_screen():
    turtle.clear()
    turtle.clearscreen()
    setup_screen()

class SternbergTest:
    def __init__(self):
        self.results = []
        self.current_trial = 0
        self.total_trials = 20
        self.orientation = None
        self.set_size = None
        
        # Create directories for logs if they don't exist
        if not os.path.exists('horizontal_log'):
            os.makedirs('horizontal_log')
        if not os.path.exists('vertical_log'):
            os.makedirs('vertical_log')
        
    def save_results(self):
        timestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        filename = f"WlogW{timestamp}_num{self.set_size}_{self.orientation}.txt"
        
        if self.orientation == "horizontal":
            filepath = os.path.join('horizontal_log', filename)
        else:
            filepath = os.path.join('vertical_log', filename)
        
        with open(filepath, "w") as f:
            f.write("Index,Number Set(),Number,User Input,T/F,Time(ms)\n")
            for idx, result in enumerate(self.results):
                f.write(f"{idx},{result['number_set']},{result['target']},{result['user_input']},{result['correct']},{result['response_time']}\n")
        
        return filepath

    def select_orientation(self):
        screen = setup_screen()
        clear_screen()
        
        text = turtle.Turtle()
        text.hideturtle()
        text.penup()
        text.goto(0, 100)
        text.write("방향을 선택하세요", align="center", font=("Arial", 14, "normal"))
        
        buttons = [
            Button("가로", -75, 30, 20, lambda: self.set_orientation("horizontal")),
            Button("세로", 75, 30, 20, lambda: self.set_orientation("vertical"))
        ]
        
        for button in buttons:
            button.draw(screen)
        
        def handle_click(x, y):
            for button in buttons:
                if button.is_clicked(x, y) and button.onclick:
                    button.onclick()
        
        screen.onclick(handle_click)
        screen.listen()
        screen.update()

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.start_test()

    def display_numbers(self, numbers, screen):
        screen.tracer(0)
        clear_screen()
        
        text = turtle.Turtle()
        text.hideturtle()
        text.penup()
        
        if self.orientation == "horizontal":
            text.goto(0, 0)
            text.write("   ".join(map(str, numbers)), align="center", font=("Arial", 16, "bold"))  # Increased spacing between numbers
        else:
            total_height = 40 * len(numbers)
            for num in numbers:
                total_height = 40 * len(numbers)  # 숫자들의 총 높이
                start_y = (total_height) // 2  # 화면 중앙에서 시작
                
                for num in numbers:
                    text.goto(0, start_y)
                    text.write(str(num), align="center", font=("Arial", 16, "bold"))
                    start_y -= 45  # Increased spacing between numbers in vertical mode
        
        screen.update()
        time.sleep(2)
        clear_screen()

    def check_number(self, numbers, target, screen):
        screen.tracer(0)
        clear_screen()
        
        # 모든 터틀 객체를 리스트로 관리
        turtles = []
        
        # 목표 숫자 표시
        number_display = turtle.Turtle()
        number_display.hideturtle()
        number_display.penup()
        number_display.goto(0, 20)
        number_display.write(str(target), align="center", font=("Arial", 24, "bold"))
        turtles.append(number_display)
        
        screen.update()
        
        start_time = int(time.time() * 1000)
        response = None
        correct = None
        user_input = None
        
        def on_key_press(key):
            nonlocal response, correct, user_input
            if key == 'v':
                response = True
                user_input = "True"
            elif key == 'n':
                response = False
                user_input = "False"

        # 키보드 입력을 받을 때, 각 키를 직접 on_key_press에 연결
        screen.listen()
        screen.onkey(lambda: on_key_press('v'), 'v')
        screen.onkey(lambda: on_key_press('n'), 'n')
        
        
        while response is None and int(time.time() * 1000) - start_time < 5000:
            screen.update()
        
        end_time = int(time.time() * 1000)
        response_time = end_time - start_time
        
        if response is None:
            user_input = "TimeOut"
            correct = False
        else:
            correct = (response == (target in numbers))
        
        # 결과 저장
        self.results.append({
            'number_set': str(tuple(numbers)).replace(',', ''),
            'target': target,
            'user_input': user_input,
            'correct': correct,
            'response_time': min(response_time, 5000)
        })
        
        # 기존 텍스트 지우기
        for t in turtles:
            t.clear()
            t.hideturtle()
        
        # 정답 여부 표시
        feedback = turtle.Turtle()
        feedback.hideturtle()
        feedback.penup()
        feedback.goto(0, 0)
        if correct:
            feedback.color("blue")
            feedback.write("정답!", align="center", font=("Arial", 20, "bold"))
        else:
            feedback.color("red")
            feedback.write("오답", align="center", font=("Arial", 20, "bold"))
        
        screen.update()
        time.sleep(1)
        
        return correct

    def run_trial(self):
        if self.current_trial >= self.total_trials:
            filename = self.save_results()
            
            screen = setup_screen()
            clear_screen()
            
            text = turtle.Turtle()
            text.hideturtle()
            text.penup()
            text.goto(0, 0)
            text.write(f"{filename}\n에 저장되었습니다.", align="center", font=("Arial", 14, "normal"))
            
            button = Button("Close", 0, -50, 20, turtle.bye)
            button.draw(screen)
            
            screen.onclick(lambda x, y: button.is_clicked(x, y) and button.onclick())
            screen.listen()
            return
        
        screen = setup_screen()
        numbers = random.sample(range(1, 10), self.set_size)
        self.display_numbers(numbers, screen)
        
        target = random.randint(1, 9)
        self.check_number(numbers, target, screen)
        
        self.current_trial += 1
        time.sleep(1)
        self.run_trial()

    def start_test(self):
        self.current_trial = 0
        self.results = []
        self.run_trial()

def show_number_selection():
    screen = setup_screen()
    clear_screen()
    
    text = turtle.Turtle()
    text.hideturtle()
    text.penup()
    text.goto(0, 100)
    text.write("숫자 세트 크기를 선택하세요", align="center", font=("Arial", 14, "normal"))
    
    test = SternbergTest()
    
    def start_with_size(size):
        test.set_size = size
        test.select_orientation()
    
    buttons = [
        Button("3", -75, 30, 20, lambda: start_with_size(3)),
        Button("5", 75, 30, 20, lambda: start_with_size(5)),
        Button("7", -75, -50, 20, lambda: start_with_size(7)),
        Button("9", 75, -50, 20, lambda: start_with_size(9))
    ]
    
    for button in buttons:
        button.draw(screen)
    
    def handle_click(x, y):
        for button in buttons:
            if button.is_clicked(x, y) and button.onclick:
                button.onclick()
    
    screen.onclick(handle_click)
    screen.listen()
    screen.update()

def main():
    screen = setup_screen()
    
    text = turtle.Turtle()
    text.hideturtle()
    text.penup()
    text.goto(0, 100)
    text.write("스턴버그 테스트", align="center", font=("Arial", 18, "bold"))
    text.penup()

    
     # 키 안내 텍스트를 박스로 감싸서 표시
    text.hideturtle()
    text.penup()
    text.goto(0, 140)
    text.pendown()
    text.pensize(2)
    text.goto(-110, 140)
    text.goto(-110, 90)
    text.goto(110, 90)
    text.goto(110, 140)
    text.goto(0, 140)
    text.penup()


    text.goto(0,30)
    text.write(" 제시된 숫자의 나열을 보고,\n해당 숫자가 있었으면 'v', 없었으면 'n'을 눌러주세요", align="center", font=("Arial", 12, "bold"))
    
    button = Button("Start", 0, -50, 20, show_number_selection)
    button.draw(screen)
    
    def handle_click(x, y):
        if button.is_clicked(x, y):
            button.onclick()
    
    screen.onclick(handle_click)
    screen.listen()
    screen.update()
    
    screen.mainloop()

if __name__ == "__main__":
    main()
