import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports
import tkinter


def flappy_bird():
    # Global Variables for the game
    FPS = 32
    SCREENWIDTH = 289
    SCREENHEIGHT = 511
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    GROUNDY = SCREENHEIGHT * 0.8
    GAME_images = {}
    GAME_SOUNDS = {}
    PLAYER = 'gallery/images/bird.png'
    BACKGROUND = 'gallery/images/background.png'
    PIPE = 'gallery/images/pipe.png'

    def welcomeScreen():
        """
        Shows welcome images on the screen
        """

        playerx = int(SCREENWIDTH / 5)
        playery = int((SCREENHEIGHT - GAME_images['player'].get_height()) / 2)
        start_screenx = int((SCREENWIDTH - GAME_images['start_screen'].get_width()) / 2)
        start_screeny = int(SCREENHEIGHT * 0.13)
        basex = 0
        while True:
            for event in pygame.event.get():
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If the user presses space or up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return
                else:
                    SCREEN.blit(GAME_images['background'], (0, 0))
                    SCREEN.blit(GAME_images['player'], (playerx, playery))
                    SCREEN.blit(GAME_images['start_screen'], (start_screenx, start_screeny))
                    SCREEN.blit(GAME_images['base'], (basex, GROUNDY))
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)

    def mainGame():
        score = 0
        playerx = int(SCREENWIDTH / 5)
        playery = int(SCREENWIDTH / 2)
        basex = 0

        # Create 2 pipes for blitting on the screen
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # my List of upper pipes
        upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        # my List of lower pipes
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8  # velocity while flapping
        playerFlapped = False  # It is true only when the bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
                        GAME_SOUNDS['wing'].play()

            crashTest = isCollide(playerx, playery, upperPipes,
                                  lowerPipes)  # This function will return true if the player is crashed
            if crashTest:
                return

                # check for score
            playerMidPos = playerx + GAME_images['player'].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_images['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f"Your score is {score}")
                    GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_images['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            # move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0 < upperPipes[0]['x'] < 5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
            if upperPipes[0]['x'] < -GAME_images['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # Lets blit our images now
            SCREEN.blit(GAME_images['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            SCREEN.blit(GAME_images['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_images['player'], (playerx, playery))
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_images['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width) / 2

            for digit in myDigits:
                SCREEN.blit(GAME_images['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
                Xoffset += GAME_images['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery > GROUNDY - 25 or playery < 0:
            GAME_SOUNDS['hit'].play()
            return True

        for pipe in upperPipes:
            pipeHeight = GAME_images['pipe'][0].get_height()
            if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_images['pipe'][0].get_width()):
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            if (playery + GAME_images['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                    GAME_images['pipe'][0].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        return False

    def getRandomPipe():
        """
        Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
        """
        pipeHeight = GAME_images['pipe'][0].get_height()
        offset = SCREENHEIGHT / 3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_images['base'].get_height() - 1.2 * offset))
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        pipe = [
            {'x': pipeX, 'y': -y1},  # upper Pipe
            {'x': pipeX, 'y': y2}  # lower Pipe
        ]
        return pipe

    if __name__ == "__main__":
        # This will be the main point from where our game will start
        pygame.init()  # Initialize all pygame's modules
        FPSCLOCK = pygame.time.Clock()
        pygame.display.set_caption('Flappy bird by AKV')
        GAME_images['numbers'] = (
            pygame.image.load('gallery/images/0.png').convert_alpha(),
            pygame.image.load('gallery/images/1.png').convert_alpha(),
            pygame.image.load('gallery/images/2.png').convert_alpha(),
            pygame.image.load('gallery/images/3.png').convert_alpha(),
            pygame.image.load('gallery/images/4.png').convert_alpha(),
            pygame.image.load('gallery/images/5.png').convert_alpha(),
            pygame.image.load('gallery/images/6.png').convert_alpha(),
            pygame.image.load('gallery/images/7.png').convert_alpha(),
            pygame.image.load('gallery/images/8.png').convert_alpha(),
            pygame.image.load('gallery/images/9.png').convert_alpha(),
        )

        GAME_images['start_screen'] = pygame.image.load('gallery/images/start_screen.png').convert_alpha()
        GAME_images['base'] = pygame.image.load('gallery/images/base.png').convert_alpha()
        GAME_images['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                               pygame.image.load(PIPE).convert_alpha()
                               )

        # Game sounds
        GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
        GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
        GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
        GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
        GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

        GAME_images['background'] = pygame.image.load(BACKGROUND).convert()
        GAME_images['player'] = pygame.image.load(PLAYER).convert_alpha()

        while True:
            welcomeScreen()  # Shows welcome screen to the user until he presses a button
            mainGame()  # This is the main game function


def colour_game():
    # create instance for window
    root_colour = tkinter.Tk()
    # set title
    root_colour.title("Simple Color Game")
    # set window size
    root_colour.geometry("650x450+300+90")
    # initialize and configure background
    # color for window
    bg = "pink"
    root_colour.config(bg=bg)
    root_colour.resizable(False, False)
    entry = tkinter.StringVar()
    # initialize variables
    count_ = total = 0
    time = 10
    # label to display title
    title = tkinter.Label(root_colour, text="Color Game", font=("ariel", 30, "underline bold"), width=10, bg="pink",
                          fg="black")
    title.place(x=205, y=25)

    # start function to start the game
    def start():
        global time
        btn.config(state=tkinter.DISABLED)

        # countdown function to display time
        def count_down():
            global time, total, count_
            if time >= 0:
                countdown.config(text=time)
                time = time - 1
                # call the count_down() function
                # to update the countdown time
                countdown.after(2000, count_down)
                # configure bg color to labels
                timeleftlbl.config(bg=bg)
                countdown.config(bg=bg)
                scorelbl.config(bg=bg)
                count.config(text=count_, bg=bg)
                totallbl.config(text=total, bg=bg)
                outof.config(text="/", bg=bg)

            else:
                time = 10
                total = count_ = 0
                # create new window to display
                # some message after game over
                new_root = tkinter.Toplevel()
                # set title
                new_root.title("Simple Color Game")
                # set window size
                new_root.geometry("650x450+300+90")
                # hide root window
                root_colour.withdraw()
                # label to display game over
                game_over = tkinter.Label(new_root, text="Game Over", font=("ariel", 40, "bold"))
                game_over.place(x=205, y=120)

                # function to start the game again
                def replay(event=None):
                    # hide new_root window
                    new_root.withdraw()
                    # call root window
                    root_colour.deiconify()
                    # focus input in entry box
                    e.focus()
                    # call stat function
                    start()

                # button to start the game again
                Play_again = tkinter.Button(new_root, text="Play Again", font=("ariel", 20, "bold"), bg="black",
                                            fg="gold",
                                            width=10, relief=tkinter.RIDGE, command=replay)
                Play_again.place(x=250, y=200)
                # bind enter button with new_root window
                new_root.bind("<Return>", replay)

        count_down()

        def changes():
            global bg
            # list of different colors
            colors = ["red", "green", "blue", "yellow", "pink", "brown"]
            # choose random colors
            bg = random.choice(colors)
            # confiure new random bg color
            # to window and labels
            root_colour.config(bg=bg)
            lbl.config(bg=bg)
            title.config(bg=bg)
            timeleftlbl.config(bg=bg)
            countdown.config(bg=bg)
            scorelbl.config(bg=bg)
            count.config(text=count_, bg=bg)
            totallbl.config(text=total, bg=bg)
            outof.config(text="/", bg=bg)
            entry.set("")

        def scores(event=None):
            global count_, total
            # update the score if the entered
            # color name is same as bg color
            if entry.get() == bg:
                count_ = count_ + 1
                total = total + 1

                changes()
            # if the entered colors does not match
            # with bg color update the total
            # submitted colors
            else:
                total = total + 1
                changes()

        btn1.config(command=scores)
        # bind Enter button with root window
        # to directly submit the entered colors
        # and display the score without pressing
        # the Submit button
        root_colour.bind("<Return>", scores)

    # buttons to start the game
    btn = tkinter.Button(root_colour, text="Start Game", font=("ariel", 20, "bold"), bg="black", fg="gold2", width=15,
                         relief=tkinter.RIDGE,
                         command=start)
    btn.place(x=200, y=100)
    # label to display the Time left text
    timeleftlbl = tkinter.Label(root_colour, text="Time Left : ", font=("ariel", 15, "bold"), height=2, bg=bg)
    timeleftlbl.place(x=55, y=165)
    # label to display the total time left to play the game
    countdown = tkinter.Label(root_colour, font=("ariel", 15, "bold"), height=2, bg=bg)
    countdown.place(x=175, y=165)
    # label to display the total score text
    scorelbl = tkinter.Label(root_colour, text="Your total Score is : ", font=("ariel", 15, "bold"), height=2, bg=bg)
    scorelbl.place(x=345, y=165)
    # label to display the total number of correct entered colors
    count = tkinter.Label(root_colour, font=("ariel", 15, "bold"), height=2, bg=bg)
    count.place(x=550, y=165)
    # label to display "/" symbol
    outof = tkinter.Label(root_colour, font=("ariel", 15, "bold"), height=2, bg=bg)
    outof.place(x=575, y=165)
    # label to display the both total number of correct and
    # incorrect entered colors
    totallbl = tkinter.Label(root_colour, font=("ariel", 15, "bold"), height=2, bg=bg)
    totallbl.place(x=590, y=165)
    # label to display enter color name text
    lbl = tkinter.Label(root_colour, text="Enter color name : ", width=15, font=("ariel", 15, "bold"), bg="pink",
                        fg="black")
    lbl.place(x=120, y=295)
    # entry box to get the input from player
    e = tkinter.Entry(root_colour, textvariable=entry, width=15, font=("ariel", 15, "bold"))
    e.place(x=340, y=295)
    e.focus()
    # submit button to submit the color and update score
    btn1 = tkinter.Button(root_colour, text="Submit", font=("ariel", 18, "bold"), bg="black", fg="gold2", width=10,
                          relief=tkinter.RIDGE)
    btn1.place(x=245, y=380)
    root_colour.mainloop()


root = tkinter.Tk()
root.geometry('300x200')
root.title("Gaming Nostalgia")

# colour game
btn_colour_game = tkinter.Button(root, text="Colour Game", command=colour_game)
btn_colour_game.pack(pady=10, fill='x')

# flappy bird
btn_flappy_bird = tkinter.Button(root, text="Flappy Bird", command=flappy_bird)
btn_flappy_bird.pack(pady=10, fill='x')

root.mainloop()
