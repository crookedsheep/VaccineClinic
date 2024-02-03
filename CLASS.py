# Joo-Young Gonzalez 
# Date: 02/02/2024
# Module 4 Assignment 4
import pygame, sys
from pygame.locals import QUIT
import pygwidgets


class PatientClass():
  def __init__(self, id, name, phone, address):
    # a patient will have their own instance of demographics, vaccines, and symptoms
    self._id = id
    self._name = name
    self._phone = phone
    self._address = address
    self._vaccines = {"vacc_A": False, "vacc_B": False, "vacc_C": False} 
    self._symptoms = {"sympt_A": False, "sympt_B": False, "sympt_C": False}

  # set and get methods used by the clinic class
  def setVaccine(self, vac_name, vac_status):
    self._vaccines[vac_name] = vac_status

  def setSymptom(self, sympt_name, sympt_status):
    self._symptoms[sympt_name] = sympt_status
    
  def getVaccines(self):
    return self._vaccines

  def getSymptoms(self):
    return self._symptoms
  
  def setDemographics(self, name, phone, address):
    self._name = name
    self._phone = phone
    self._address = address
# for debugging
  def show(self):
    print("Name: ",self._name)
    print("Phone: ",self._phone)
    print("Address: ",self._address)
    print("Vaccines: ",self._vaccines)
    print("Symptoms: ",self._symptoms)



class ClinicClass():
  def __init__(self, maxPatients):
    # there will be only one instance of the clinic class during the running of the code
    # we will track a dictionary of patient objects, the next patient ID, the current patient, the max number of patients
    # and the vaccine and symptom totals
    self._patientDict = {}
    self._nextpatientID = 0
    self._currentPatient = None
    self._maxPatients = maxPatients
    self._vaccineTotals = {"vacc_A": 0, "vacc_B": 0, "vacc_C": 0}
    self._vaccineSymptomTotals = {
      "vacc_A": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0},
      "vacc_B": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0}, 
      "vacc_C": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0}
    }
  # used in the addPatientInfo method to add a new patient object
  def addPatientObject(self, name, phone, address):
    try :
      if self._nextpatientID >= self._maxPatients:
        raise ValueError("Maximum number of patients reached")
    except ValueError as e:
      print(e)
      return False
    newPatient = PatientClass(self._nextpatientID, name, phone, address) 
    self._patientDict[self._nextpatientID] = newPatient
    self._nextpatientID += 1
    return True
  
  # we will use this method to add a new patient or update an existing patient
  def addPatientInfo(self,id, name_input, phone_input, address_input, vaccine_input, symptom_input, new_patient):
    
    if new_patient:
      self.addPatientObject(name_input, phone_input, address_input)
      # set the current patient to the new patient
      self._currentPatient = self._patientDict[self._nextpatientID - 1]

    else:
      # if we are updating an existing patient, we will set the current patient to the patient we are updating
      self._currentPatient = self._patientDict[id]
      self._currentPatient.setDemographics(name_input, phone_input, address_input)
      # we will make a copy of the previous vaccines and symptoms to compare with the new input to update our totals
      previous_vaccines = self._currentPatient._vaccines.copy()
      previous_symptoms = self._currentPatient._symptoms.copy()

  # we will update our vaccine totals and symptom totals when we add a new patient/ or update
    for vaccine, v_status in vaccine_input.items():
      if new_patient:
        if v_status:
          self._vaccineTotals[vaccine] += 1
      # else, not a new patient, updating info
      else:
        if v_status and not previous_vaccines[vaccine]:
          self._vaccineTotals[vaccine] += 1
        if not v_status and previous_vaccines[vaccine]:
          self._vaccineTotals[vaccine] -= 1
      # set the vaccine status for the current patient based on the input
      self._currentPatient.setVaccine(vaccine, v_status)

    for symptom, s_status in symptom_input.items():
      for vaccine, v_status in vaccine_input.items():
        if new_patient:
          if v_status and s_status:
            self._vaccineSymptomTotals[vaccine][symptom] += 1
        # else, not a new patient, just updating info
        else:
          if v_status and s_status and not (previous_symptoms[symptom] and previous_vaccines[vaccine]):
            self._vaccineSymptomTotals[vaccine][symptom] += 1
          if not (v_status and s_status) and previous_symptoms[symptom] and previous_vaccines[vaccine]:
            self._vaccineSymptomTotals[vaccine][symptom] -= 1
      self._currentPatient.setSymptom(symptom, s_status)
 
 # report patient info
  def reportPatientInfo(self, input):
    patientID = input
    try:
      patientID = int(patientID)
    except ValueError:
      print("Invalid input")
    if patientID not in self._patientDict:
      print("patient Id not found")
    else: 
      self._patientDict[patientID].show()

# get patient info
  def getPatientName(self, id):
    return self._patientDict[id]._name
  def getPatientPhone(self, id):
    return self._patientDict[id]._phone
  def getPatientAddress(self, id):
    return self._patientDict[id]._address
# get vaccine and symptom info for a patient
  def getPatientVaccines(self, id):
    return self._patientDict[id].getVaccines()
  def getPatientSymptoms(self, id):
    return self._patientDict[id].getSymptoms()
    
# reports vaccine totals and symptoms 
  def reportVaccineTotals(self, key):
    vaccine_totals_string = f"Total {key} vaccines: {self._vaccineTotals[key]}\n"
    return vaccine_totals_string
  
  def reportSymptomTotals(self, key, sympt):
    symptom_totals_string = f"Total {key} vaccines with {sympt}: {self._vaccineSymptomTotals[key][sympt]}\n"
    return symptom_totals_string

  def resetData(self):
    self._vaccineTotals = {"vacc_A": 0, "vacc_B": 0, "vacc_C": 0}
    # vaccine symptom totals
    self._vaccineSymptomTotals = {
      "vacc_A": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0},
      "vacc_B": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0}, 
      "vacc_C": {"sympt_A": 0, "sympt_B": 0, "sympt_C": 0}
    }
    # reset patient data through clinic class
    self._patientDict = {}
    self._nextpatientID = 0
    self._currentPatient = None



class PatientScreen:

  def __init__(self, clinic, window, redcircle, greencircle, buttonup, buttondown, current_screen, max_patients):
      self._clinic = clinic # access to clinic class methods
      self._current_patients = 0 # we will use this to keep track of the current number of patients
      self._current_patient_index = 0 # we will use this to keep track of the current patient index as we click next and previous
      self._window = window
      self._max_patients = max_patients
      # demographic inputs
      self._name_input = pygwidgets.InputText(window, (230, 20), "", width=250, fontSize=25)
      self._phone_input = pygwidgets.InputText(window, (230, 60), "", width=200, fontSize=25)
      self._address_input = pygwidgets.InputText(window, (230, 100), "", width=250, fontSize=25)
      # variables used later when adding patient info
      self._name = None
      self._phone = None
      self._address = None
      # variables used to track the vaccine and symptom status for the current screen
      self._vaccines = {"vacc_A": False, "vacc_B": False, "vacc_C": False}
      self._symptoms = {"sympt_A": False, "sympt_B": False, "sympt_C": False}
  
      self._current_screen = current_screen
      # vaccine buttons
      self._vacc_A_button = pygwidgets.CustomCheckBox(window, (150,180), greencircle, redcircle, value=False)
      self._vacc_B_button = pygwidgets.CustomCheckBox(window, (250,180), greencircle, redcircle, value=False) 
      self._vacc_C_button = pygwidgets.CustomCheckBox(window, (350,180), greencircle, redcircle, value=False) 
      # symptom buttons
      self._sympt_A_button = pygwidgets.CustomCheckBox(window, (150,330), greencircle, redcircle, value=False)
      self._sympt_B_button = pygwidgets.CustomCheckBox(window, (250,330), greencircle, redcircle, value=False)
      self._sympt_C_button = pygwidgets.CustomCheckBox(window, (350,330), greencircle, redcircle, value=False) 
     
      # other buttons
      self._prev_button = pygwidgets.CustomButton(window, (20,435), buttonup, buttondown) 
      self._prev_text = pygwidgets.DisplayText(window, (25,439), "Previous", fontSize=20) 
      self._next_button = pygwidgets.CustomButton(window, (180,435), buttonup, buttondown)  
      self._next_text = pygwidgets.DisplayText(window, (195,439), "Next", fontSize=20)  
      self._submit_button = pygwidgets.CustomButton(window, (340,435), buttonup, buttondown)  
      self._submit_text = pygwidgets.DisplayText(window, (350,439), "Submit", fontSize=20)  
      self._exit_button = pygwidgets.CustomButton(window, (500,435), buttonup, buttondown)  
      self._exit_text = pygwidgets.DisplayText(window, (520,439), "Exit", fontSize=20)  


# draw to screen
  def draw(self, window):
  # draw standard text
      patient_name = pygwidgets.DisplayText(window,(20,20),"Patient Name:",textColor=(0,0,0))
      patient_phone = pygwidgets.DisplayText(window,(20,60),"Patient Phone:",textColor=(0,0,0))
      patient_address = pygwidgets.DisplayText(window,(20,100),"Patient Address:",textColor=(0,0,0))
      patient_name.draw()
      patient_phone.draw()
      patient_address.draw()
      patient_symptoms = pygwidgets.DisplayText(window,(20,140),"Patient Vaccines:            VaccineA          VaccineB          VaccineC ",textColor=(0,0,0))
      patient_vaccines = pygwidgets.DisplayText(window,(20,270),"Patient Symptoms:       SymptomA          SymptomB          SymptomC ",textColor=(0,0,0))
      patient_symptoms.draw()
      patient_vaccines.draw() 
# draw buttons
      self._submit_button.draw()
      self._submit_text.draw()
      self._prev_button.draw()
      self._prev_text.draw()
      self._next_button.draw()
      self._next_text.draw()
      self._exit_button.draw()
      self._exit_text.draw()

# input and interaction buttons for patient info
      self._name_input.draw()
      self._phone_input.draw()
      self._address_input.draw()
      self._vacc_A_button.draw()
      self._vacc_B_button.draw()
      self._vacc_C_button.draw()
      self._sympt_A_button.draw()
      self._sympt_B_button.draw()
      self._sympt_C_button.draw()


  def handleEvent(self, event):
      # handles input text boxes
      if self._name_input.handleEvent(event):
        pass
      if self._phone_input.handleEvent(event):
        pass
      if self._address_input.handleEvent(event):
        pass
      # handles vaccine and symptom buttons, if clicked we need to update the vaccine and symptom status
      if self._vacc_A_button.handleEvent(event):
        self._vaccines["vacc_A"] = self._vacc_A_button.getValue()
      if self._vacc_B_button.handleEvent(event):
        self._vaccines["vacc_B"] = self._vacc_B_button.getValue()
      if self._vacc_C_button.handleEvent(event):
        self._vaccines["vacc_C"] = self._vacc_C_button.getValue()
      if self._sympt_A_button.handleEvent(event):
        self._symptoms["sympt_A"] = self._sympt_A_button.getValue()
      if self._sympt_B_button.handleEvent(event):  
        self._symptoms["sympt_B"] = self._sympt_B_button.getValue()
      if self._sympt_C_button.handleEvent(event):
        self._symptoms["sympt_C"] = self._sympt_C_button.getValue()
      # handles submit button, we will add the patient info to the clinic class
      # and we will also add input validation here
      if self._submit_button.handleEvent(event):
        self.name = self._name_input.getText()
        self.phone = self._phone_input.getText()
        self.address = self._address_input.getText()
        # add our input validation here after submitting
        try:
          if self.name == "" or self.phone == "" or self.address == "":
            raise ValueError("Please fill out all fields")
          # Check if the name is valid
          if not self.name.isalpha() or len(self.name) > 100:
            raise ValueError("Please enter a valid name")
          # Check if the phone number is valid
          if not self.phone.isdigit() or len(self.phone) != 10:
            raise ValueError("Please enter a valid phone number")
          # Check if the address is valid
          if len(self.address) > 100:
            raise ValueError("Address is too long")

          # handles previous patient info that is updated, uses clinic class method
          if self._current_patient_index < self._current_patients:
            self._clinic.addPatientInfo(self._current_patient_index,self.name, self.phone, self.address, self._vaccines, self._symptoms, False)
            
          # handles new patient info that is added, uses clinic class method
          elif self._current_patient_index == self._current_patients and self._current_patients < self._max_patients:
            self._clinic.addPatientInfo(self._current_patient_index,self.name, self.phone, self.address, self._vaccines, self._symptoms, True)
            self._current_patients += 1
            self._current_patient_index += 1
            self._current_screen[0] = "menu"
            self.reset()
        
        except ValueError as e:
          print(e)
          pass
      
      # handles the previous and next buttons, we will reset the screen, increment or decrement the index appropriately
      # to display the next or previous patient info
      if self._prev_button.handleEvent(event):
        if self._current_patient_index > 0:
          self.reset()
          self._current_patient_index -= 1
          self.displayPatientInfo(self._current_patient_index)
        else:
          print("No previous patients to display")

      if self._next_button.handleEvent(event):
        if (self._current_patient_index < (self._current_patients - 1)):
          self.reset()
          self._current_patient_index += 1
          self.displayPatientInfo(self._current_patient_index)
        else:
          print("No more patients to display")

      if self._exit_button.handleEvent(event):
        self._current_patient_index = self._current_patients
        self._current_screen[0] = "menu"
        self.reset()

  # we will call this function when we click the next or previous buttons
  def displayPatientInfo(self, index):
      # grab the patient info from the clinic class methods
      self._name_input.setText(self._clinic.getPatientName(index))
      self._phone_input.setText(self._clinic.getPatientPhone(index))
      self._address_input.setText(self._clinic.getPatientAddress(index))
      # grab the patient's vaccine and symptom info from the clinic class methods
      vaccines = self._clinic.getPatientVaccines(index)
      symptoms = self._clinic.getPatientSymptoms(index) 
      if vaccines["vacc_A"]:
        self._vacc_A_button.setValue(True)
        self._vaccines["vacc_A"] = True
      else:
        self._vacc_A_button.setValue(False)
        self._vaccines["vacc_A"] = False
      if vaccines["vacc_B"]:
        self._vacc_B_button.setValue(True)
        self._vaccines["vacc_B"] = True
      else:
        self._vacc_B_button.setValue(False)
        self._vaccines["vacc_B"] = False
      if vaccines["vacc_C"]:
        self._vacc_C_button.setValue(True)
        self._vaccines["vacc_C"] = True
      else:
        self._vacc_C_button.setValue(False)
        self._vaccines["vacc_C"] = False
      #symptoms
      if symptoms["sympt_A"]:
        self._sympt_A_button.setValue(True)
        self._symptoms["sympt_A"] = True
      else:
        self._sympt_A_button.setValue(False)
        self._symptoms["sympt_A"] = False
      if symptoms["sympt_B"]: 
        self._sympt_B_button.setValue(True)
        self._symptoms["sympt_B"] = True
      else:
        self._sympt_B_button.setValue(False)
        self._symptoms["sympt_B"] = False
      if symptoms["sympt_C"]:
        self._sympt_C_button.setValue(True)
        self._symptoms["sympt_C"] = True
      else:
        self._sympt_C_button.setValue(False)
        self._symptoms["sympt_C"] = False

      self.draw(self._window)
        
  # we will call reset when we submit a patient info or when we exit the patient screen
  def reset(self):
      self._name_input.setText("") 
      self._phone_input.setText("")
      self._address_input.setText("")
      self._vacc_A_button.setValue(False)
      self._vacc_B_button.setValue(False)
      self._vacc_C_button.setValue(False)
      self._sympt_A_button.setValue(False)
      self._sympt_B_button.setValue(False)
      self._sympt_C_button.setValue(False)
      self._vaccines = {"vacc_A": False, "vacc_B": False, "vacc_C": False}
      self._symptoms = {"sympt_A": False, "sympt_B": False, "sympt_C": False}

  # this function is only for use to reset the patient screen when we click main menu reset
  def deepReset(self):  
      self._current_patients = 0
      self._current_patient_index = 0
      self.reset()

  
# Our main menu screen which displays all our main button options
class MainMenu:
  def __init__(self, clinic, window, buttonup, buttondown, current_screen, reset_screen):
    self._clinic = clinic
    self._current_screen = current_screen
    self._reset_screen = reset_screen

    self._main_menu_text = pygwidgets.DisplayText(window,(240,20),"Main Menu",fontSize=30,textColor=(0,0,0))
    self._input_button = pygwidgets.CustomButton(window,(20,120),up=buttonup,down=buttondown)
    self._input_button_text = pygwidgets.DisplayText(window,(30,130),"Input patient Info")

    self._report_individual = pygwidgets.CustomButton(window,(20,240),up=buttonup,down=buttondown)
    self._report_individual_text = pygwidgets.DisplayText(window,(30,250),"Report on Individual")

    self._report_vaccines = pygwidgets.CustomButton(window,(20,360),up=buttonup,down=buttondown)
    self._report_vaccines_text = pygwidgets.DisplayText(window,(30,370),"Report Total Vaccines")  
  
    self._report_symptoms = pygwidgets.CustomButton(window,(340,120),up=buttonup,down=buttondown)
    self._report_symptoms_text = pygwidgets.DisplayText(window,(350,130),"Report on Symptoms")

    self._reset_button = pygwidgets.CustomButton(window,(340,240),up=buttonup,down=buttondown)
    self._reset_text = pygwidgets.DisplayText(window,(350,250),"Reset")

    self._quit_button = pygwidgets.CustomButton(window,(340,360),up=buttonup,down=buttondown)
    self._quit_text = pygwidgets.DisplayText(window,(350,370),"Quit")


  def draw(self):
    self._main_menu_text.draw()
    self._input_button.draw()
    self._input_button_text.draw()
    self._report_individual.draw()
    self._report_individual_text.draw()
    self._report_vaccines.draw()
    self._report_vaccines_text.draw()
    self._report_symptoms.draw()
    self._report_symptoms_text.draw()
    self._reset_button.draw()
    self._reset_text.draw()
    self._quit_button.draw()
    self._quit_text.draw()

 # alters our current screen variable to the appropriate screen
  def handleEvent(self, event):
    if self._input_button.handleEvent(event):
      self._current_screen[0] = "input information" 
    if self._report_individual.handleEvent(event):
      self._current_screen[0] = "report individual"
    if self._report_vaccines.handleEvent(event):
      self._current_screen[0] = "report vaccines"
    if self._report_symptoms.handleEvent(event):
      self._current_screen[0] = "report symptoms"
    if self._reset_button.handleEvent(event):
      self._current_screen[0] = "reset"
    if self._quit_button.handleEvent(event):
      sys.exit()
        
# report individual screen allows user to enter a patient ID and display the patient info
class ReportIndividualScreen:
    
    def __init__(self, clinic, window, buttonup, buttondown, current_screen):
        self._clinic = clinic # access to clinic class methods
        self._window = window
        self._current_screen = current_screen
        self._patient_id_input = pygwidgets.InputText(window,(150,20),width=100,fontSize=25)
        self._patient_id_prompt = pygwidgets.DisplayText(window,(20,20),"Enter Patient ID:",textColor=(0,0,0))
        self._submit_button = pygwidgets.CustomButton(window,(300,20),buttonup,buttondown)
        self._submit_text = pygwidgets.DisplayText(window,(320,24),"Submit",textColor=(0,0,0))
        self._exit_button = pygwidgets.CustomButton(window,(500,435),buttonup,buttondown)
        self._exit_text = pygwidgets.DisplayText(window,(520,439),"Exit",textColor=(0,0,0))
        self._patient_info_text = pygwidgets.DisplayText(window,(20,60),"")
        # we will add the text to display here in the event handler
        self._patient_vaccine_text = pygwidgets.DisplayText(window,(20,100),"")
        self._patient_symptom_text = pygwidgets.DisplayText(window,(20,140),"")
      

    def draw(self):
        self._patient_id_input.draw()
        self._patient_id_prompt.draw()
        self._patient_info_text.draw()
        self._patient_vaccine_text.draw()
        self._patient_symptom_text.draw()
        self._submit_button.draw()
        self._submit_text.draw()
        self._exit_button.draw()
        self._exit_text.draw()


    def handleEvent(self, event):
        if self._patient_id_input.handleEvent(event):
            pass
        if self._submit_button.handleEvent(event):
        # when the submit button is clicked, we will display the patient info
            try:
              # here we try for exceptions, if we catch an exception, we will print the error and pass
              print("Patient ID:",self._patient_id_input.getText())
              if self._patient_id_input.getText() == "":
                  raise ValueError("Please enter a patient ID")
              if self._patient_id_input.getText().isdigit() == False:
                  raise ValueError("Please enter a valid patient ID")
              if int(self._patient_id_input.getText()) not in self._clinic._patientDict:
                  raise ValueError("Patient not found")
              # if nothing is raised, we will display the patient info
              patient_id = int(self._patient_id_input.getText())
              if patient_id in self._clinic._patientDict:
                print("patient found in dictionary")
                # grab the patient info from the clinic class methods
                name = self._clinic.getPatientName(patient_id)
                phone = self._clinic.getPatientPhone(patient_id)
                address = self._clinic.getPatientAddress(patient_id)
                vaccines = self._clinic.getPatientVaccines(patient_id)
                symptoms = self._clinic.getPatientSymptoms(patient_id)
                self._patient_info_text.setValue(f"Name: {name}           Phone: {phone}           Address: {address}")
                self._patient_vaccine_text.setValue(f"Vaccines: {vaccines}")
                self._patient_symptom_text.setValue(f"Symptoms: {symptoms}")
                                                   
            except ValueError as e:
              print(e)
              pass

        if self._exit_button.handleEvent(event):
            self._patient_id_input.setText("")
            self._patient_info_text.setValue("")
            self._patient_vaccine_text.setValue("")
            self._patient_symptom_text.setValue("")
            self._current_screen[0] = "menu" 

# report vaccine totals screen allows user to see the total number of vaccines administered
class ReportVaccinesScreen:
  def __init__(self, clinic, window, buttonup, buttondown, current_screen):
    self._clinic = clinic # access to clinic instance
    self._window = window # access to window instance
    self._current_screen = current_screen # access to current screen variable
    self._report_vacc_A = pygwidgets.DisplayText(window,(20,60),"", fontSize=20)
    self._report_vacc_B = pygwidgets.DisplayText(window,(20,100),"", fontSize=20)
    self._report_vacc_C = pygwidgets.DisplayText(window,(20,140),"", fontSize=20)
    self._exit_button = pygwidgets.CustomButton(window,(500,435),buttonup,buttondown)
    self._exit_text = pygwidgets.DisplayText(window,(520,439),"Exit")

  def draw(self):
    # accessing clinic instance methods to set the values for the report text
    default_text = pygwidgets.DisplayText(self._window, (20, 20), "Total Vaccines Registered", textColor=(0,0,0), fontSize=24)
    default_text.draw()
    self._report_vacc_A.setValue(self._clinic.reportVaccineTotals("vacc_A"))
    self._report_vacc_A.draw()
    self._report_vacc_B.setValue(self._clinic.reportVaccineTotals("vacc_B"))
    self._report_vacc_B.draw()
    self._report_vacc_C.setValue(self._clinic.reportVaccineTotals("vacc_C"))
    self._report_vacc_C.draw()
    self._exit_button.draw()
    self._exit_text.draw()

  def handleEvent(self, event):
    if self._exit_button.handleEvent(event):
      # when exiting, reset the report text and return to the main menu
      self._current_screen[0] = "menu"
      self._report_vacc_A.setValue("")
      self._report_vacc_B.setValue("")
      self._report_vacc_C.setValue("")
      pass

# report symptom totals screen allows user to see the total number of symptoms reported
class ReportSymptomsScreen:

  def __init__(self, clinic, window, buttonup, buttondown, current_screen):
    self._clinic = clinic # acccess to clinic instance
    self._window = window # access to window instance
    self._current_screen = current_screen # access to current screen variable

    self._report_vacA_symptA = pygwidgets.DisplayText(window, (50, 60), "", textColor=(0,0,0))
    self._report_vacA_symptB = pygwidgets.DisplayText(window, (50, 100), "", textColor=(0,0,0))
    self._report_vacA_symptC = pygwidgets.DisplayText(window, (50, 140), "", textColor=(0,0,0))
    self._report_vacB_symptA = pygwidgets.DisplayText(window, (50, 200), "", textColor=(0,0,0))  
    self._report_vacB_symptB = pygwidgets.DisplayText(window, (50, 240), "", textColor=(0,0,0))
    self._report_vacB_symptC = pygwidgets.DisplayText(window, (50, 280), "", textColor=(0,0,0))
    self._report_vacC_symptA = pygwidgets.DisplayText(window, (50, 340), "", textColor=(0,0,0))
    self._report_vacC_symptB = pygwidgets.DisplayText(window, (50, 380), "", textColor=(0,0,0))
    self._report_vacC_symptC = pygwidgets.DisplayText(window, (50, 420), "", textColor=(0,0,0))
    self._exit_button = pygwidgets.CustomButton(window, (500, 435), up=buttonup, down=buttondown)
    self._exit_text = pygwidgets.DisplayText(window, (520, 439), "Exit", textColor=(0,0,0))

# drawing the report to the screen
  def draw(self):
    # setting the values for the report text with the clinic instance methods
    default_text = pygwidgets.DisplayText(self._window, (50, 20), "Total Vaccines with Symptoms", textColor=(0,0,0), fontSize=24)
    default_text.draw()
    self._report_vacA_symptA.setValue(self._clinic.reportSymptomTotals("vacc_A", "sympt_A"))
    self._report_vacA_symptA.draw()
    self._report_vacA_symptB.setValue(self._clinic.reportSymptomTotals("vacc_A", "sympt_B"))
    self._report_vacA_symptB.draw()
    self._report_vacA_symptC.setValue(self._clinic.reportSymptomTotals("vacc_A", "sympt_C"))
    self._report_vacA_symptC.draw()
    self._report_vacB_symptA.setValue(self._clinic.reportSymptomTotals("vacc_B", "sympt_A"))
    self._report_vacB_symptA.draw()
    self._report_vacB_symptB.setValue(self._clinic.reportSymptomTotals("vacc_B", "sympt_B"))
    self._report_vacB_symptB.draw()
    self._report_vacB_symptC.setValue(self._clinic.reportSymptomTotals("vacc_B", "sympt_C"))
    self._report_vacB_symptC.draw()
    self._report_vacC_symptA.setValue(self._clinic.reportSymptomTotals("vacc_C", "sympt_A"))
    self._report_vacC_symptA.draw()
    self._report_vacC_symptB.setValue(self._clinic.reportSymptomTotals("vacc_C", "sympt_B"))
    self._report_vacC_symptB.draw()
    self._report_vacC_symptC.setValue(self._clinic.reportSymptomTotals("vacc_C", "sympt_C"))
    self._report_vacC_symptC.draw()
    self._exit_button.draw()
    self._exit_text.draw()

  def handleEvent(self, event):
    if self._exit_button.handleEvent(event):
      # when exiting, reset the report text and return to the main menu
      self._current_screen[0] = "menu"
      self._report_vacA_symptA.setValue("")
      self._report_vacA_symptB.setValue("")
      self._report_vacA_symptC.setValue("")
      self._report_vacB_symptA.setValue("")
      self._report_vacB_symptB.setValue("")
      self._report_vacB_symptC.setValue("")
      self._report_vacC_symptA.setValue("")
      self._report_vacC_symptB.setValue("")
      self._report_vacC_symptC.setValue("")
      pass
  
# reset vaccination totals and symptom totals, and patient data  
class ResetScreen:
  # used keyword parameter for buttons in initialization, unless otherwise specified, the default button images will be used
  def __init__(self, clinic, window, current_screen, patient_screen, buttonup='images/smallupbutton.png', buttondown='images/smalldownbutton.png'):
    self._clinic = clinic
    self._window = window
    self._current_screen = current_screen
    self._patient_screen = patient_screen
    self._reset_text = pygwidgets.DisplayText(window, (180,50), "Click reset to erase all clinic data", textColor=(0,0,0), fontSize=24)
    #self._reset_button = pygwidgets.CustomButton(window, (260, 100), up=buttonup, down=buttondown)
    self._reset_button = pygwidgets.TextButton(window, (260, 100), "Reset", width=100, height=50)
    self._exit_button = pygwidgets.TextButton(window, (500,370), "Exit", width=100, height=50)
    
  def draw(self):
    self._reset_text.draw()
    self._reset_button.draw()
    self._exit_button.draw()
  
  def handleEvent(self, event):
    # exit reset screen and return to main menu
    if self._exit_button.handleEvent(event):
      self._current_screen[0] = "menu"
      pass
    # reset the clinic data and return to the main menu
    elif self._reset_button.handleEvent(event):
      self.reset_function()
      self._current_screen[0] = "menu"
      self.draw()
      pass

  def reset_function(self):
    # using clinic class method to reset patient and clinic data
    self._clinic.resetData()
    # reset patient screen data
    self._patient_screen.deepReset()
    self._current_screen[0] = "menu" 

