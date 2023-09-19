cardiac_Story = {
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

