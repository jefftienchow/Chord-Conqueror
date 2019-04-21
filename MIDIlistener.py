"""REMEMBER TO INSTALL THE PACKAGE WITH pip install python-rtmidi"""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput

class MIDIInput(object):
    def __init__(self,  callback = print):
        self.callback = callback
        self.last_note = 0
        self.current_notes = set()
        try:
            self.midiin, port_name = open_midiinput(0)
        except:
            sys.exit()

    def on_update(self):
        #verify if the port is receiving any input
        try:
            timer = time.time()
            #get the MIDI input
            msg = self.midiin.get_message()

            #if input received
            if msg:
                message, deltatime = msg
                timer += deltatime

                #separate message into Note and velocity
                note_on = message[0] == 144
                midiNote = message[1]
                velocity = message[2]

                #print(message)

                #means a note is actually being played, so we want to add to active notes
                if note_on:
                    self.current_notes.add(midiNote)
                    self.last_note = midiNote
                    self.callback(str(self.last_note))
                #note not being played, so don't add/remove from active notes
                else:
                    if midiNote in self.current_notes:
                        self.current_notes.remove(midiNote)

            time.sleep(0.01)
        except KeyboardInterrupt:
            print('')
        







# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.




# port = sys.argv[1] if len(sys.argv) > 1 else None

# try:
#     midiin, port_name = open_midiinput(port)
# except (EOFError, KeyboardInterrupt):
#     sys.exit()

# print("Entering main loop. Press Control-C to exit.")
# try:
#     timer = time.time()
#     while True:
#         msg = midiin.get_message()

#         if msg:
#             message, deltatime = msg
#             timer += deltatime
#             # print("[%s] @%0.6f %r" % (port_name, timer, message))
#             print(message)

#         time.sleep(0.01)
# except KeyboardInterrupt:
#     print('')
# finally:
#     print("Exit.")
#     midiin.close_port()
#     del midiin






#fp.py




        # frame = self.controller.on_update()
        # self.time = frame / 44100
        # self.display.on_update(self.time)
        # self.player.on_update(self.time)

        # if not self.player.get_done():
        #     self.label.text = "Press \"P\" to "
        #     if self.playing:
        #         self.label.text += "pause.\n"
        #     elif self.started:
        #         self.label.text += "unpause\n"
        #         self.label.text += "Press \"R\" to restart\n"

        #     else:
        #         self.label.text += "begin.\n"
        #     self.label.text += "score: %d\n" % self.player.get_score()
        #     if self.player.get_streak() >= 5:
        #         self.label.text += "                                                  Streak: %d   2x Bonus" % self.player.get_streak()
        # else:
        #     self.label.text = "Final score is: %d\n" % self.player.get_score()
        #     self.label.text += "Accuracy is: %d %%\n" % self.player.get_accuracy()

        #     self.label.text += "Highest streak: %d\n" % self.player.get_max_streak()
        #     self.label.text += "Press \"R\" to restart"


