"""REMEMBER TO INSTALL THE PACKAGE WITH pip install python-rtmidi"""

from __future__ import print_function

import logging
import sys
import time
import rtmidi
from rtmidi.midiutil import open_midiinput


STRING_TO_MIDINOTE = {6:40, 5:45, 4:50, 3:55, 2:59, 1:64}
class MIDIInput(object):
    def __init__(self,  callback = print, callback2= print, callback3 = print, callback4 = print):
        self.callback = callback
        self.callback2 = callback2
        self.callback3 = callback3
        self.callback4 = callback4
        self.last_note = 0
        self.current_notes = set()
        self.on = True
        self.midiin, port_name = open_midiinput(0, api=0)
        self.last_note_fret = {0:10, 1:10, 2:10, 3:10, 4:10, 5:10}

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
                #print(msg)
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
                        note_on = message[2] > 65
                        midiNote = message[1]
                        velocity = message[2]

                        #print(message)

                        #means a note is actually being played, so we want to add to active notes
                        if note_on:
                            self.current_notes.add(midiNote)
                            self.last_note = midiNote
                            self.last_string = string
                            self.callback((str(self.last_string),str(self.last_note)))
                            self.callback3(midiNote)
                        #note not being played, so don't add/remove from active notes
                        else:
                            if midiNote in self.current_notes:
                                self.current_notes.remove(midiNote)

                    else:




                        if (len(message) == 8 and message[4] == 1):
                            string = message[5]
                            midiNote = message[6]
                            # print(string-1)
                            # print(midiNote - STRING_TO_MIDINOTE[string])
                            self.callback2(string-1, midiNote - STRING_TO_MIDINOTE[string])
                            self.callback4(self.last_note_fret[string-1])
                            print(self.last_note_fret[string-1], midiNote)
                            self.last_note_fret[string-1] = midiNote
                            print("HERE")
                            # self.callback2(str(string) + " has finger on fret #:" + str(int(midiNote)-STRING_TO_MIDINOTE[string]))
                    msg = self.midiin.get_message()
                    

        # time.sleep(0.01)
            except KeyboardInterrupt:
                print('')
