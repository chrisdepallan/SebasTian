import curses
from curses import wrapper
import openai
import os
from curses.textpad import Textbox, rectangle
from dotenv import load_dotenv

# Set your OpenAI API key

load_dotenv()

def get_ai_response(user_input):
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OPENAI_API_KEY environment variable is not set"
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant in a terminal application."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def create_input_window(stdscr):
    h, w = stdscr.getmaxyx()
    input_win = curses.newwin(3, w-4, h-5, 2)
    box = Textbox(input_win)
    rectangle(stdscr, h-6, 1, h-2, w-2)
    stdscr.refresh()
    return box, input_win

def draw_menu(stdscr, selected_row_idx, ai_response=None):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Create menu items
    menu_items = ["Ask AI", "View History", "Settings", "Exit"]
    
    # Draw title
    title = "AI Terminal Assistant"
    start_x_title = int((w - len(title)) // 2)
    stdscr.addstr(2, start_x_title, title)
    
    # Draw menu
    for idx, item in enumerate(menu_items):
        x = int((w - len(item)) // 2)
        y = h//2 - len(menu_items)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, item)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, item)
    
    # Draw AI response if exists
    if ai_response:
        response_y = h-8
        stdscr.addstr(response_y, 2, "AI Response:", curses.A_BOLD)
        # Wrap text to fit window width
        words = ai_response.split()
        line = ""
        current_y = response_y + 1
        for word in words:
            if len(line) + len(word) + 1 < w-4:
                line += word + " "
            else:
                stdscr.addstr(current_y, 2, line)
                current_y += 1
                line = word + " "
        if line:
            stdscr.addstr(current_y, 2, line)
    
    stdscr.refresh()

def main(stdscr):
    # Clear screen and set up colors
    stdscr.clear()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)  # -1 means default background (black)
    stdscr.bkgd(' ', curses.color_pair(1))
    
    # Hide cursor
    curses.curs_set(0)
    
    current_row = 0
    ai_response = None
    
    # Clear screen again to ensure clean state
    stdscr.clear()
    stdscr.refresh()
    
    while True:
        draw_menu(stdscr, current_row, ai_response)
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 3:  # Exit option
                break
            elif current_row == 0:  # Ask AI option
                # Create input window
                box, input_win = create_input_window(stdscr)
                stdscr.addstr(stdscr.getmaxyx()[0]-6, 2, "Enter your question: (Ctrl+Alt+G to submit)")
                stdscr.refresh()
                
                # Get user input
                curses.curs_set(1)
                while True:
                    ch = input_win.getch()
                    if ch == 7:  # Ctrl+Alt+G (ASCII 7)
                        break
                    box.do_command(ch)
                user_input = box.gather().strip()
                curses.curs_set(0)
                
                # Get AI response
                ai_response = get_ai_response(user_input)
        
        draw_menu(stdscr, current_row, ai_response)

# Clear terminal before starting
os.system('cls' if os.name == 'nt' else 'clear')
wrapper(main)