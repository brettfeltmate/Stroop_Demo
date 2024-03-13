# -*- coding: utf-8 -*-

__author__ = "Brett Feltmate"

import klibs
from klibs import P
from klibs.KLUtilities import now
from klibs.KLUserInterface import any_key, ui_request
from klibs.KLCommunication import message
from klibs.KLText import add_text_style
from klibs.KLGraphics import fill, blit, flip, clear
from klibs.KLResponseListeners import KeypressListener

from random import choice

INSTUX  = "instrux"
DEFAULT = "default"
RED     = "RED"
GREEN   = "GREEN"
BLUE    = "BLUE"
YELLOW  = "YELLOW"
WORD    = "word"
INK     = "ink"

FONT_SIZE = 90

RED_INK    = (255,   0,   0, 255)
GREEN_INK  = (  0, 255,   0, 255)
BLUE_INK   = (  0,   0, 255, 255)
YELLOW_INK = (255, 255,   0, 255)

class stroop_demo(klibs.Experiment):

    def setup(self):
        add_text_style(INSTUX,  size = 48)
        add_text_style(DEFAULT, size = FONT_SIZE)
        add_text_style(RED,     size = FONT_SIZE, color =    RED_INK)
        add_text_style(GREEN,   size = FONT_SIZE, color =  GREEN_INK)
        add_text_style(BLUE,    size = FONT_SIZE, color =   BLUE_INK)
        add_text_style(YELLOW,  size = FONT_SIZE, color = YELLOW_INK)


        self.trial_listener = KeypressListener({
            "y": RED,
            "u": GREEN,
            "i": BLUE,
            "o": YELLOW
        })

        self.score = 0



    def block(self):
        if P.block_number == 1:
            instrux = "Welcome to the Stroop Task Demo!" + \
                     "\n\nFor your first task, you'll see words for colours (red, blue, etc)." + \
                     "\n\nYour objective is to press the key that matches the colour the word SAYS." + \
                     "\n\nGood luck! Press any key to begin."
            
        elif P.block_number == 2:
            instrux = "Great job!" + \
                        "\n\nThis time, each word will be printed in a colour." + \
                        "\n\nYour objective is still the same, to press the key that matches what the word SAYS." + \
                        "\nSo you'll need to ignore the colour it's printed in!" + \
                        "\n\nGood luck! Press any key to begin."
            
        elif P.block_number == 3:
            instrux = "You're doing great!" + \
                        "\n\nNow, things are going to get tricky!" + \
                        "\n\nIn this block, you'll see words for colours again." + \
                        "\n\nBut this time, you'll indicate the colour of the INK." + \
                        "\nSo now you'll need to ignore the what the word says!" + \
                        "\n\nGood luck! Press any key to begin."
            
        else:
            instrux = "Tricky right?" + \
                        "\n\nFor your final task, each word will be printed in a colour." + \
                        "\n\nIf this word is boxed-in\nExample: | RED |\nIndicate what the word SAYS." + \
                        "\n\nBut, if the word is NOT boxed-in\nExample: BLUE\nIndicate the colour of the INK." + \
                        "\n\nGood luck! Press any key to begin."
            
        fill()
        message(instrux, location=P.screen_c, style=INSTUX)
        flip()

        any_key()

    def trial_prep(self):
        self.word = choice([RED, GREEN, BLUE, YELLOW])

        if P.block_number == 1:
            self.respond_with = WORD

        elif P.block_number == 2:
            self.respond_with = WORD

        elif P.block_number == 3:
            self.respond_with = INK

        else:
            self.respond_with = choice([WORD, INK])

        if P.block_number == 1:
            self.style = DEFAULT
        else:
            self.style = self.word
            while self.style == self.word:
                self.style = choice([RED, GREEN, BLUE, YELLOW])

            if P.block_number == 4:
                self.word = self.word if self.respond_with == INK else f"| {self.word} |"

        

    def trial(self):

        fill()
        message(self.word, location=P.screen_c, style=self.style)
        flip()

        response, _ = self.trial_listener.collect()


        clear()
        then = now()
        while now() < then + 0.500:
            ui_request()

        

        correct = response == self.word if self.respond_with == WORD else response == self.style
       
        if correct:
            self.score += 1
        
        if P.development_mode:
            print(f"\n\nWord: {self.word}, \nStyle: {self.style}, \nTask: {self.respond_with}, \nResponse: {response}, \nCorrect: {correct}\n\n")

        msg = "Nice!" if correct else "Whoops!"


        fill()
        message(msg, location=P.screen_c, style=DEFAULT)
        flip()

        then = now()
        while now() < then + 0.500:
            ui_request()

        clear()

        then = now()
        while now() < then + 0.500:
            ui_request()


        return {
            "block_num": P.block_number,
            "trial_num": P.trial_number
        }

    def trial_clean_up(self):
        pass

    def clean_up(self):
        fill()
        score = (self.score / (P.trials_per_block * P.blocks_per_experiment)) * 100
        msg = f"Great job! You scored {score:.0f}%!\n\nThanks for playing! Press any key to exit."
        message(msg, location=P.screen_c)
        flip()
        any_key()
