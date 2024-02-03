# Joo-Young Gonzalez 
# Date: 02/02/2024
# Module 4 Assignment 4
#

import pygame, sys
from pygame.locals import QUIT
from CLASS import *
import pygwidgets

# Constants
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 240)
LIGHT_GREEN = (173, 240, 173)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
PATIENTS_MAX = 15
# load assets, images, sounds, etc.
buttonup = "images/blankupbutton.png"
buttondown = "images/blankdownbutton.png"
greencircle = "images/greencircle.png"
redcircle = "images/redcircle.png"
smallup = "images/smallupbutton.png"
smalldown = "images/smalldownbutton.png"

# Initialize world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Module 3 Assignment')
window.fill(WHITE)
clock = pygame.time.Clock()
# way to track which screen should be displayed
current_screen = ["menu"]

# Initialize variables
oClinic = ClinicClass(PATIENTS_MAX) # where we store our dictionary of patient objects, as well as vaccine and symptom totals
# patient screen allows us to add a new patient object or cycle through to update old patients
oPatientScreen = PatientScreen(oClinic, window, redcircle, greencircle, smallup, smalldown, current_screen, PATIENTS_MAX) 
# reset screen allows us to reset all vaccine and symptom totals and the patient dictionary
oReset = ResetScreen(oClinic, window, current_screen, oPatientScreen) 
# main menu allows us to navigate to the other screens
oMainMenu = MainMenu(oClinic, window, buttonup, buttondown, current_screen, oReset) 
# allows user to report an individual's information when entering patient's index(their dictionary index in oClinic)
oReportIndividual = ReportIndividualScreen(oClinic, window, smallup, smalldown, current_screen)
# reports vaccine totals for current patients
oReportVaccineTotals = ReportVaccinesScreen(oClinic, window, smallup, smalldown, current_screen)
# reports symptoms associated with each vaccine
oReportSymptoms = ReportSymptomsScreen(oClinic, window, smallup, smalldown, current_screen)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        # handles main menu's events if we are in the menu
        if current_screen[0] == "menu": 
            oMainMenu.handleEvent(event)

        # calls the PatientScreen function to handle events
        elif current_screen[0] == "input information":
        # Handle the events for the text inputs
            oPatientScreen.handleEvent(event)

        # calls the ReportIndividualScreen handleEvent function   
        elif current_screen[0] == "report individual":
            if oReportIndividual.handleEvent(event):
                pass
        # calls to the ReportVaccinesScreen           
        elif current_screen[0] == "report vaccines":
            if oReportVaccineTotals.handleEvent(event):
                pass
        # calls to the ReportSymptomsScreen
        elif current_screen[0] == "report symptoms":
            if oReportSymptoms.handleEvent(event):
                pass
        # calls to the ResetScreen
        elif current_screen[0] == "reset":
            if oReset.handleEvent(event):
                pass
                                                
            
    window.fill(WHITE)
  
    if current_screen[0] == "menu":
        window.fill(LIGHT_BLUE)
        oMainMenu.draw()
    
    if current_screen[0] == "input information":
      # add new patient to the clinic dictionary
        window.fill(LIGHT_BLUE)
        oPatientScreen.draw(window)
                                                          
    if current_screen[0] == "report individual":
      # display report for individual patient
        window.fill(LIGHT_GREEN)
        oReportIndividual.draw()

    if current_screen[0] == "report vaccines":
      # display report for total vaccines
        window.fill(LIGHT_BLUE)
        oReportVaccineTotals.draw()

    if current_screen[0] == "report symptoms":
        # display report for total symptoms
        window.fill(LIGHT_BLUE)
        oReportSymptoms.draw()

    if current_screen[0] == "reset":
        # reset all vaccine and symptom data
        window.fill(LIGHT_BLUE)
        oReset.draw()
       

    pygame.display.update()
