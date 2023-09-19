import pygame
import sys
import subprocess
#from cardiacLevelDictionary import cardiac_Story

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('2018-08-02-17971.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely


# ===================== CONSTANTS & GLOBALS =====================
#Screens and Margins
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 40
MARGIN = 20
CHATBOX_HEIGHT = 275
CTRL_BTN_SIZE = 20
CTRL_BTN_MARGIN = 5
CHATBOX_GAP = 50
USER_CHATBOX_HEIGHT = 125
USER_CHATBOX_PADDING = 10
USER_CHATBOX_Y_ADJUSTMENT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (80, 80, 80)
LIGHT_GREY = (160, 160, 160)
BORDER_BLUE = (0, 56, 168)  # a retro blue color
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (100, 149, 237)
VINTAGE_CREAM = (250, 245, 230)  # This is a soft cream color.
DARKER_VINTAGE_CREAM = (240, 230, 210)  # This is a darker soft cream color.

#Other Globals
click_sound = pygame.mixer.Sound('click.mp3')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('medday:emt')
font_path = "font1.ttf"
font = pygame.font.Font(font_path, 36)
title_font = pygame.font.Font(font_path, 26)

# ===================== UTILITY FUNCTIONS =====================
def generate_gradient(start_color, end_color, steps):
    """Generate a gradient list of colors between start_color and end_color."""
    gradient = []
    for i in range(steps):
        r = start_color[0] * (1 - i/steps) + end_color[0] * (i/steps)
        g = start_color[1] * (1 - i/steps) + end_color[1] * (i/steps)
        b = start_color[2] * (1 - i/steps) + end_color[2] * (i/steps)
        gradient.append((int(r), int(g), int(b)))
    return gradient



def wrap_text(text, font, max_width):
        """
        Wraps the given text to fit within the specified width.
        """
        words = text.split(' ')
        wrapped_lines = []
        current_line = words[0]

        for word in words[1:]:
            test_line = current_line + " " + word
            # Check the width of the test line with the given font
            test_width, _ = font.size(test_line)

            if test_width <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word

        wrapped_lines.append(current_line)
        return wrapped_lines

def draw_pixelated_gradient_border(rect, start_color, end_color, top_thickness=1, right_thickness=1, bottom_thickness=1,
                                   left_thickness=1):
    """Draw a pixelated gradient border around a pygame Rect."""
    # Generate the gradient
    gradient = generate_gradient(start_color, end_color,
                                 max(top_thickness, right_thickness, bottom_thickness, left_thickness))
    # Top border
    for i in range(rect.top, rect.top + top_thickness):
        color = gradient[i - rect.top]
        for j in range(rect.left, rect.right, 2):
            pygame.draw.line(screen, color, (j, i), (j + 1, i))
    # Bottom border
    for i in range(rect.bottom - bottom_thickness, rect.bottom):
        color = gradient[bottom_thickness - 1 - (i - (rect.bottom - bottom_thickness))]
        for j in range(rect.left, rect.right, 2):
            pygame.draw.line(screen, color, (j, i), (j + 1, i))
    # Left border
    for i in range(rect.left, rect.left + left_thickness):
        color = gradient[i - rect.left]
        for j in range(rect.top, rect.bottom, 2):
            pygame.draw.line(screen, color, (i, j), (i, j + 1))
    # Right border
    for i in range(rect.right - right_thickness, rect.right):
        color = gradient[right_thickness - 1 - (i - (rect.right - right_thickness))]
        for j in range(rect.top, rect.bottom, 2):
            pygame.draw.line(screen, color, (i, j), (i, j + 1))

def draw_pixelated_border(rect, color, top_thickness=1, right_thickness=1, bottom_thickness=1, left_thickness=1):
    """Draw a pixelated border around a pygame Rect with individual thickness for each side."""
    # Top border
    for i in range(rect.top, rect.top + top_thickness):
        for j in range(rect.left, rect.right, 2):
            pygame.draw.line(screen, color, (j, i), (j + 1, i))

    # Bottom border
    for i in range(rect.bottom - bottom_thickness, rect.bottom):
        for j in range(rect.left, rect.right, 2):
            pygame.draw.line(screen, color, (j, i), (j + 1, i))

    # Left border
    for i in range(rect.left, rect.left + left_thickness):
        for j in range(rect.top, rect.bottom, 2):
            pygame.draw.line(screen, color, (i, j), (i, j + 1))

    # Right border
    for i in range(rect.right - right_thickness, rect.right):
        for j in range(rect.top, rect.bottom, 2):
            pygame.draw.line(screen, color, (i, j), (i, j + 1))

def draw_title(screen, text, font, color, y_offset=0):
    """Draw a title on the top center of the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + text_surface.get_height() // 2))
    screen.blit(text_surface, text_rect)

# ===================== CLASS DEFINITIONS =====================
class Button:
    def __init__(self, x, y, text):
        self.text = text
        # Adjust the size and style of the option buttons to match the chat interface
        self.width = (WIDTH - 2*MARGIN - 3*USER_CHATBOX_PADDING) // 2
        self.height = 35  # Making it shorter for a more chat-like feel
        self.highlighted = False
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        if self.highlighted:
            pygame.draw.rect(screen, LIGHT_GREY, self.rect)
        else:
            pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.line(screen, WHITE, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), 2)  # Draw bottom border
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class WindowControlButton:
    def __init__(self, x, y, symbol, bgcolor):
        self.rect = pygame.Rect(x, y, CTRL_BTN_SIZE, CTRL_BTN_SIZE)
        self.symbol = symbol
        self.bgcolor = bgcolor
        self.symbol_font = pygame.font.Font(font_path, 24)

    def draw(self, screen):
        # Draw button background
        pygame.draw.rect(screen, self.bgcolor, self.rect)

        # Draw symbol
        text_surf = self.symbol_font.render(self.symbol, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

        # Draw pixelated border around the button
        draw_pixelated_border(self.rect, GREY, 2, 2, 2, 2)  # Uniform thickness for all sides


class SendButton:
    def __init__(self, x, y, image_path):
        self.original_image = pygame.image.load(image_path)
        # Scale the image
        self.image = pygame.transform.scale(self.original_image, (50, 50))  # adjust (30, 30) as per your preference
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    

# ===================== MAIN FUNCTION & HELPERS =====================
def main():
    clock = pygame.time.Clock()

    # Calculate initial button position
    button_gap_x = 250
    button_gap_y = 15
    initial_x = MARGIN + USER_CHATBOX_PADDING +36
    initial_y = HEIGHT - USER_CHATBOX_HEIGHT + USER_CHATBOX_PADDING - 75

    buttons = [
        Button(initial_x, initial_y-115, "Option 1"),
        Button(initial_x + BUTTON_WIDTH / 2 + button_gap_x, initial_y-115, "Option 2"),
        Button(initial_x, initial_y + BUTTON_HEIGHT + button_gap_y-108, "Option 3"),
        Button(initial_x + BUTTON_WIDTH / 2 + button_gap_x, initial_y + BUTTON_HEIGHT + button_gap_y-108, "Option 4"),
    ]

    # window control buttons
    close_btn = WindowControlButton(WIDTH - CTRL_BTN_MARGIN - CTRL_BTN_SIZE, CTRL_BTN_MARGIN, "X",
                                    (255, 0, 0))  # Red background
    minimize_btn = WindowControlButton(WIDTH - 2 * (CTRL_BTN_MARGIN + CTRL_BTN_SIZE), CTRL_BTN_MARGIN, "-",
                                       (0, 0, 255))  # Blue background

    # Initialize selected_option to None, indicating no option has been selected yet
    selected_option = None

    def distribute_buttons(total_buttons):
        positions = []
        
        # Calculate the base position
        base_x = initial_x
        base_y = initial_y
        
        for i in range(total_buttons):
            # Determine column (0 for left, 1 for right)
            col = i % 2
            # Determine row (integer division)
            row = i // 2
            
            # Calculate position based on column and row
            x = base_x + col * (BUTTON_WIDTH + button_gap_x) - 50
            y = base_y + row * (BUTTON_HEIGHT + button_gap_y) - 50
            
            positions.append((x, y))
        
        return positions
    
    def display_story_text(story_key, font, max_width):
        """Displays the story text in the chatbox."""
        story_text = story_data[story_key]["text"]

        # Use the wrap_text function to get lines of wrapped text
        wrapped_lines = wrap_text(story_text, font, max_width)

        # Draw each line with some vertical spacing
        y_position = inner_chatbox_rect.top + 10
        line_spacing = 20  # adjust this value based on your needs
        for line in wrapped_lines:
            text_surface = font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(topleft=(inner_chatbox_rect.left + 10, y_position))
            screen.blit(text_surface, text_rect)
            y_position += line_spacing

    current_state = "scene1" 
    mouse_pressed = False

    def create_buttons_for_state(state):
        options = story_data[state]["options"]
        positions = distribute_buttons(len(options))
        return [Button(pos[0], pos[1], option) for pos, option in zip(positions, options)]

    
    buttons = create_buttons_for_state(current_state)

    while True:
        # User Chatbox Drawing
        user_chatbox_rect = pygame.Rect(MARGIN, HEIGHT - USER_CHATBOX_HEIGHT - MARGIN - USER_CHATBOX_Y_ADJUSTMENT, WIDTH - 2 * MARGIN, USER_CHATBOX_HEIGHT)
        draw_pixelated_border(user_chatbox_rect, GREY, 4)  # Drawing the grey border around user chatbox

        # White inner area of the user chatbox
        inner_user_chatbox_rect = pygame.Rect(user_chatbox_rect.left + 2, user_chatbox_rect.top + 2,
                                            user_chatbox_rect.width - 4, user_chatbox_rect.height - 4)
        pygame.draw.rect(screen, WHITE, inner_user_chatbox_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse button release
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN and not mouse_pressed:
                mouse_pressed = True

                # Check if any option button is clicked
                for idx, button in enumerate(buttons):
                    if button.is_clicked(event.pos):
                        click_sound.play()
                        current_state = story_data[current_state]["next"][idx]
                        buttons = create_buttons_for_state(current_state)  # regenerate buttons for new state
                        break

        # Update and draw everything on the screen
        screen.fill(DARKER_VINTAGE_CREAM)

        # Draw an application border with a thicker top
        app_border = pygame.Rect(0, 0, WIDTH, HEIGHT)
        draw_pixelated_gradient_border(app_border, DARK_BLUE, LIGHT_BLUE, top_thickness=35, right_thickness=10, bottom_thickness=10, left_thickness=10)

        # Draw Words
        draw_title(screen, "emt sim: cardiac situation", title_font, WHITE, CTRL_BTN_SIZE // 2 - 3)

        # Draw Windows Control Buttons
        close_btn.draw(screen)
        minimize_btn.draw(screen)

        # If an option has been selected but not confirmed, visually indicate it
        for button in buttons:
            if button.text == selected_option:
                pygame.draw.rect(screen, LIGHT_GREY, button.rect)
            button.draw(screen)

        # Define a top margin for the chatbox
        CHATBOX_TOP_MARGIN = 40  # Adding 40 to maintain some padding from the top

        # Adjust the chatbox position
        chatbox_rect = pygame.Rect(MARGIN, CHATBOX_TOP_MARGIN, WIDTH - 2 * MARGIN, CHATBOX_HEIGHT)
        draw_pixelated_border(chatbox_rect, GREY, 5, 5, 5, 5)  # Thinner pixelated black border

        # Inner chatbox rect
        INNER_CHATBOX_MARGIN = 5
        inner_chatbox_rect = pygame.Rect(chatbox_rect.left + INNER_CHATBOX_MARGIN,
                                        chatbox_rect.top + INNER_CHATBOX_MARGIN,
                                        chatbox_rect.width - 2 * INNER_CHATBOX_MARGIN,
                                        chatbox_rect.height - 2 * INNER_CHATBOX_MARGIN)
        pygame.draw.rect(screen, WHITE, inner_chatbox_rect)


        # Define and draw send button
        send_btn_image_path = "mail.png"
        send_btn_x = inner_user_chatbox_rect.right - 65
        send_btn_y = inner_user_chatbox_rect.bottom - -8
        send_btn = SendButton(send_btn_x, send_btn_y, send_btn_image_path)
        send_btn.draw(screen)

        max_width = inner_chatbox_rect.width - 20  # adjust the subtraction value based on your desired padding

        display_story_text(current_state, font , max_width)
        pygame.display.flip()
        clock.tick(60)

story_data = {
    "scene1": {
        "text": "...You walk onto the scene...",
        "options": ["1.Assess Scene", "2.Approach Patient"],
        "next": ["scene2", "game_over"]
    },
    "game_over": {
        "text": "GROSS NEGLIGENCE",
        "options": ["RESTART"],
        "next": ["scene1"]
    },
    "scene2": {
        "text": "**It’s a foggy night. Some students are walking down the street, clearly intoxicated. The street is narrow and you are near a busy intersection.**",
        "options": ["Apply PBE", "Hi-Vis Vest/Gloves", "Approach Patient"],
        "next": ["game_over", "scene3", "game_over"]
    },
    "scene3": {
        "text": "**You applied your Hi-Vis Vest and Gloves**",
        "options": ["Approach Patient", "ALS Off"],
        "next": ["scene4", "game_over"]
    },
    "scene4": {
        "text": "You: Hi! I’m EMT Johnny. What’s your name? Patient: Hi Johnny, I’m Hugh. You: Hi Hugh, what’s bothering you today? Hugh: I’ve been feeling some chest pain. You: Alright, is it ok if I take the look? Hugh: Sure.",
        "options": ["Initial Assessment", "Inquire History", "Stroke Test"],
        "next": ["scene5", "scene5.1", "scene5.2"]
    },
    "scene5": {
        "text": "Intial Assessment Summary: -------------------------- Condition - Stable Observation - Sweaty, Flushed Responsiveness - Normal Airway - Normal Breathing - Slightly Labored Circulation - Normal Bleeding - Mild bleeding from head trauma",
        "options": ["Control Bleeding", "Ignore Bleeding"],
        "next": ["scene5.3", "game_over"]
    },
    "scene5.1": {
        "text": "Sample History: --------------- Symptoms - Sharp Chest Pains Allergies - Penicillin Medications - Medical Marijuana Medical Hist - Cardiac problems/low BP Last Intake - None Events Leading to Injury: Hugh: I was making dinner, and as I was opening the firdge, I felt a sharp pain in my chest which caused me to stumble and fall.",
        "options": ["Next"],
        "next": ["scene4"]
    },
    "scene5.2": {
        "text": "**Hugh shows normal function. He's probably not suffering from a stroke**",
        "options": ["Next"],
        "next": ["scene4"]
    },
    "scene5.3": {
        "text": "**You succesfully stopped the bleeding** You: There, that should stop the bleeding. Hugh: Thank you so much, I was begining to feel a little light headed.",
        "options": ["Physical Exam", "Neuro Check", "Initiate CPR"],
        "next": ["scene6", "scene6.1", "game_over"]
    },
    "scene6": {
        "text": "Physical Examination: --------------------- You: Where does the pain seem to originate from? Hugh: It feels like the pain is deep in my chest. Kind of like something is sitting on me. You: Does the pain feel as if it is radiating elsewhere? Hugh: Yeah, I feel it in my neck and jaw. You: Do you have shortness of breath? Hugh: Just a little bit, mainly when I try to get up and move around.",
        "options": ["Apply O2", "Setup ECG", "Give Medication"],
        "next": ["scene7", "scene8", "scene9"]
    },
    "scene6.1": {
        "text": "**Hugh seems alert and oriented. His Chest pain doesn't seem to be getting better.**",
        "options": ["Next"],
        "next": ["scene5.3"]
    },
    "scene7": {
        "text": "**You have decided to give Hugh breathing assistence. Choose the optimal method for a blood O2 level of 88%.**",
        "options": ["Nasal Cannula", "High Flow O2", "BVD"],
        "next": ["scene7.1", "scene7.2", "scene7.3"]
    },
    "scene7.1": {
        "text": "**Pulse Oximetry returns Sp02 as 96.** **Healthy O2 concentration as been achieved.**",
        "options": ["Next"],
        "next": ["scene6"]
    },
    "scene7.2": {
        "text": "**Pulse Oximetry returns Sp02 as 99.** **Sp02 levels indicate a less intense O2 treatment would have been optimal.**",
        "options": ["Change Treatment"],
        "next": ["scene7"]
    },
    "scene7.3": {
        "text": "**Pulse Oximetry returns 95** **Sp02 levels indicate a less intense O2 treatment would have been optimal.** **Your partner will be stuck manually operating the BVD treatment for a while.**",
        "options": ["Change Treatment"],
        "next": ["scene7"]
    },
    "scene8": {
        "text": "**ECG has been successfully set up.** **Whoever needs to read this will be happy to have it.**",
        "options": ["Next"],
        "next": ["scene6"]
    },
    "scene9": {
        "text": "**You have discerned that in order to stabilize Hugh in his current condition, specific medication is required.**",
        "options": ["Run Checks", "Aspirin", "Nitroglycerin", "Albuterol"],
        "next": ["scene9.1", "scene10", "game_over", "game_over"]
    },
    "scene9.1": {
        "text": "Check Results: ------------- Aspirin Allergy - None Nitroglycerin Allergy - None Pulmonary Hypertension Medication - None Erectile Dysfunction Medication - Yes Blood Pressure - 90/60 mmhg",
        "options": ["Next"],
        "next": ["scene9"]
    },
    "scene10": {
        "text": "**The appropriate dosage of aspirin is given to Hugh with no complications.** Hugh: Wow that was fast, my chest and breathing feels better already.",
        "options": ["Monitor Vitals", "Check ALS status"],
        "next": ["scene11", "scene10.1"]
    },
    "scene10.1": {
        "text": "**ALS will be here any minute now.**",
        "options": ["Next"],
        "next": ["scene10"]
    },
    "scene11": {
        "text": "Vitals Report: -------------- Pain lvl - 6 BPM - 88 SpO2 - 96% Blood Pressure - 90/60 mmhg Respiratory Rate - 16",
        "options": ["Next"],
        "next": ["scene12"]
    },
        "scene12": {
        "text": "**ALS have arrived on the scene and are preparing to transport Hugh to the nearest hospital.** You brief them on everything that has happened and provide them with the ECG readings.",
        "options": ["Hand over to ALS", "Accompany ALS in transport", "Stay on scene"],
        "next": ["scene13", "scene14", "game_over"]
    },
    "scene13": {
        "text": "**You hand over the care of Hugh to ALS.** The ALS team thanks you for your assistance and quickly moves Hugh into the ambulance. As you watch the ambulance drive away, you feel a sense of satisfaction knowing that you've made a difference in someone's life today.",
        "options": ["End Story"],
        "next": ["end"]
    },
    "scene14": {
        "text": "**You decide to accompany ALS during the transport to the hospital.** In the ambulance, you continue monitoring Hugh's vitals while the ALS paramedic administers advanced care. Upon arrival at the hospital, Hugh is swiftly moved to the emergency room. Later, you're informed that he's stable and will recover fully thanks to the timely intervention.",
        "options": ["End Story"],
        "next": ["end"]
    },
    "end": {
        "text": "The end. Thank you for playing!",
        "options": ["RESTART"],
        "next": ["scene1"]
    }

}

# ===================== EXECUTE MAIN =====================
if __name__ == "__main__":
    main()



