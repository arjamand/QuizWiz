from tkinter import *
from tkinter import ttk
from quiz_brain import QuizBrain
from typing import Optional
from PIL import Image, ImageTk  # Added for image scaling

COLORS = {
    "background": "#F8F8F8",  
    "primary": "#2C3E50",     
    "secondary": "grey85",    # Updated for better visibility
    "accent": "#3498DB",      
    "success": "#2ECC71",     
    "error": "#E74C3C",       
    "text": "#2C3E50",        
    "text_light": "#ECF0F1",  
    "transparent": "SystemButtonFace"  
}

class ModernQuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.setup_window()
        self.load_images()
        self.create_widgets()
        self.get_next_question()
        self.window.mainloop()

    def load_images(self):
        """Load and scale images"""
        self.true_image = PhotoImage(file="images/true.png")
        self.false_image = PhotoImage(file="images/false.png")
        
        # Scale background image to window size
        original_image = Image.open("images/deco1.png")
        scaled_image = original_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.deco_image = ImageTk.PhotoImage(scaled_image)

    def setup_window(self):
        """Configure the main window with modern styling"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 800
        window_height = 600
        
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        
        self.window.config(bg=COLORS["primary"])
        self.window.title("QuizWiz-Modern Quiz App")
        
        style = ttk.Style()
        style.configure("Custom.TButton", 
                       padding=10, 
                       font=("Helvetica", 12, "bold"))

    def create_widgets(self):
        """Create and arrange the UI elements"""
        # Background container
        self.background_frame = Frame(self.window, bg=COLORS["primary"])
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Add scaled decorative background
        self.deco_label = Label(
            self.background_frame,
            image=self.deco_image,
            bg=COLORS["primary"]
        )
        self.deco_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main container
        self.main_frame = Frame(
            self.window, 
            bg=COLORS["primary"],
            bd=0,
            highlightthickness=0
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Score frame at the top
        self.score_label = Label(
            self.main_frame,
            text="Score: 0/0",
            bg=COLORS["primary"],
            fg=COLORS["text_light"],
            font=("Helvetica", 16, "bold")
        )
        self.score_label.grid(row=0, column=0, pady=(0, 20))

        # Question frame with semi-transparent background
        self.question_frame = Frame(
            self.main_frame,
            bg=COLORS["secondary"],
            bd=2,
            relief="ridge"
        )
        self.question_frame.grid(row=1, column=0, pady=20)

        # Question text
        self.question_label = Label(
            self.question_frame,
            text="",
            wraplength=500,
            justify="center",
            font=("Helvetica", 18),
            bg=COLORS["secondary"],
            fg=COLORS["text"],
            width=40,
            height=6
        )
        self.question_label.pack(padx=20, pady=20)

        # Buttons frame (separate from question frame)
        self.buttons_frame = Frame(
            self.main_frame,
            bg=COLORS["primary"]
        )
        self.buttons_frame.grid(row=2, column=0, pady=20)

        # Custom buttons
        self.true_button = self.create_hover_button(
            self.buttons_frame,
            self.true_image,
            self.check_answer_true,
            COLORS["success"]
        )
        self.true_button.grid(row=0, column=1, padx=20)

        self.false_button = self.create_hover_button(
            self.buttons_frame,
            self.false_image,
            self.check_answer_false,
            COLORS["error"]
        )
        self.false_button.grid(row=0, column=0, padx=20)

    def create_hover_button(self, parent, image, command, hover_color):
        """Create a button with hover effect"""
        btn = Button(
            parent,
            image=image,
            command=command,
            bd=0,
            highlightthickness=0,
            bg=COLORS["transparent"],
            activebackground=hover_color,
            cursor="hand2"
        )
        return btn

    def show_score_popup(self):
        """Display the final score in a modern popup window"""
        popup = Toplevel()
        popup.title("Quiz Complete!")
        
        popup_width = 400
        popup_height = 300
        x_position = (self.window.winfo_screenwidth() - popup_width) // 2
        y_position = (self.window.winfo_screenheight() - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
        
        popup.configure(bg=COLORS["primary"])
        
        # Scale background image for popup
        original_popup_image = Image.open("images/deco1.png")
        scaled_popup_image = original_popup_image.resize((400, 300), Image.Resampling.LANCZOS)
        popup_bg = ImageTk.PhotoImage(scaled_popup_image)
        
        deco_label = Label(
            popup,
            image=popup_bg,
            bg=COLORS["primary"]
        )
        deco_label.image = popup_bg  # Keep a reference!
        deco_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        score_frame = Frame(
            popup,
            bg=COLORS["primary"]
        )
        score_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        congrats_label = Label(
            score_frame,
            text="Congratulations!",
            font=("Helvetica", 24, "bold"),
            bg=COLORS["primary"],
            fg=COLORS["text_light"]
        )
        congrats_label.pack(pady=(0, 20))
        
        score_label = Label(
            score_frame,
            text=f"Your final score:\n{self.quiz.score}/{self.quiz.question_number}",
            font=("Helvetica", 20),
            bg=COLORS["primary"],
            fg=COLORS["text_light"]
        )
        score_label.pack(pady=(0, 30))
        
        restart_button = Button(
            score_frame,
            text="Play Again",
            font=("Helvetica", 14, "bold"),
            bg=COLORS["accent"],
            fg=COLORS["text_light"],
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self.restart_quiz(popup)
        )
        restart_button.pack()

    def restart_quiz(self, popup: Optional[Toplevel] = None):
        """Reset the quiz and close any open popup"""
        self.quiz.reset_quiz()
        if popup and popup.winfo_exists():
            popup.destroy()
        self.get_next_question()
        self.update_score_display()

    def get_next_question(self):
        """Display the next question with smooth transition"""
        if self.quiz.still_has_questions():
            question_text = self.quiz.next_question()
            self.question_label.config(text=question_text)
            self.update_score_display()
            self.question_frame.config(bg=COLORS["secondary"])
            self.question_label.config(
                bg=COLORS["secondary"],
                fg=COLORS["text"]
            )
        else:
            self.show_score_popup()

    def update_score_display(self):
        """Update the score display with animation"""
        self.score_label.config(
            text=f"Score: {self.quiz.score}/{self.quiz.question_number}"
        )

    def check_answer_true(self):
        self.feedback(self.quiz.check_answer("True"))

    def check_answer_false(self):
        self.feedback(self.quiz.check_answer("False"))

    def feedback(self, is_correct: bool):
        """Provide visual feedback for answers with smooth transition"""
        if is_correct:
            self.question_frame.config(bg=COLORS["success"])
            self.question_label.config(
                bg=COLORS["success"],
                fg=COLORS["text_light"]
            )
        else:
            self.question_frame.config(bg=COLORS["error"])
            self.question_label.config(
                bg=COLORS["error"],
                fg=COLORS["text_light"]
            )
            
        self.window.after(1000, self.reset_question_display)

    def reset_question_display(self):
        """Reset the question display and move to next question"""
        self.get_next_question()