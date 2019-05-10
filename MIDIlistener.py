"""REMEMBER TO INSTALL THE PACKAGE WITH pip install python-rtmidi"""

from __future__ import print_function

import logging
import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput


STRING_TO_MIDINOTE = {6:40, 5:45, 4:50, 3:55, 2:59, 1:64}
class MIDIInput(object):
    def __init__(self,  callback = print, callback2= print):
        self.callback = callback
        self.callback2 = callback2
        self.last_note = 0
        self.current_notes = set()
        self.on = True
        try:
            self.midiin, port_name = open_midiinput(0, api=0)
        except:
            sys.exit()
        self.midiin.ignore_types(sysex=False)
    def off(self):
        self.on = False
    def on_update(self):
        #verify if the port is receiving any input
        if self.on:
            try:
                timer = time.time()
                #get the MIDI input
                msg = self.midiin.get_message()
                print(msg)

                #if input received
                while msg != None:
                    message, deltatime = msg
                    timer += deltatime

                    #ignore exception message to avoid crash
                    if len(message) < 3:
                        print("CRASH AVERTED")
                        return


                    sysex_message = message[0] == 240
                    if not sysex_message:
                        #separate message into Note and velocity
                        # print(message)
                        string = message[0]
                        note_on = message[2] > 80
                        midiNote = message[1]
                        velocity = message[2]

                        #print(message)

                        #means a note is actually being played, so we want to add to active notes
                        if note_on:
                            self.current_notes.add(midiNote)
                            self.last_note = midiNote
                            self.last_string = string
                            self.callback((str(self.last_string),str(self.last_note)))
                        #note not being played, so don't add/remove from active notes
                        else:
                            if midiNote in self.current_notes:
                                self.current_notes.remove(midiNote)

                    else:
                        # print(message)
                        # self.callback2("REE")



                        if (len(message) == 8 and message[4] == 1):
                            string = message[5]
                            midiNote = message[6]
                            print(string-1)
                            print(midiNote - STRING_TO_MIDINOTE[string])
                            self.callback2(string-1, midiNote - STRING_TO_MIDINOTE[string])
                            print('called back')
                            # self.callback2(str(string) + " has finger on fret #:" + str(int(midiNote)-STRING_TO_MIDINOTE[string]))
                    msg = self.midiin.get_message()
                    

        # time.sleep(0.01)
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


