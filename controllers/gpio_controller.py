from gpiozero import LED, Button, Buzzer, Servo, AngularServo
from time import sleep, time

# les pins du gpio
capt_veh_entre = Button(25, pull_up=True)
select_duree = Button(9, pull_up=True)
confirm_paiement = Button(11, pull_up=True)
capt_veh_sort = Button(5, pull_up=True)
annul = Button(6, pull_up=True)
erreur = Button(13, pull_up=True)
err_idle = Button(19, pull_up=True)
idle_ferme = Button(26, pull_up=True)

led_verte = LED(14)
led_jaune = LED(15)
led_rouge = LED(18)

buzzer = Buzzer(17)
servo = AngularServo(27, min_angle = -45, max_angle = 45)

# mets toutes les variables a off  au depart pour eviter un comportement aleatoire
led_verte.off()
led_jaune.off()
led_rouge.off()

buzzer.off()
servo.detach()

    
def vert():
    led_verte.on()
    led_jaune.off()
    led_rouge.off()
    
def jaune():
    led_verte.off()
    led_jaune.on()
    led_rouge.off()

def jaune_blink():
    led_verte.off()
    led_jaune.blink()
    led_rouge.off()
    
def rouge():
    led_verte.off()
    led_jaune.on()
    led_rouge.on()

def buzzer_court():
    buzzer.on()
    sleep(1)
    buzzer.off()
    
def buzzer_alarme():
    buzzer.beep(on_time=0.1, off_time=0.1,n=5, background=True)
    
def barriere_ouvert():
    servo.angle = 45
    sleep(2)
    servo.detach()    # detach fait que le servo est desactive apres utilisation

def barriere_ferme():
    servo.angle = -45
    sleep(2)
    servo.detach()
    
