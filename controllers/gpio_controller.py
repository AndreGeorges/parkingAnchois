from gpiozero import LED, Button, Buzzer, Servo, AngularServo
from time import sleep, time
from config.config_loader import GPIO

capt_veh_entre = Button(GPIO["capt_veh_entre"], pull_up=True)
select_duree = Button(GPIO["select_duree"], pull_up=True)
confirm_paiement = Button(GPIO["confirm_paiement"], pull_up=True)
capt_veh_sort = Button(GPIO["capt_veh_sort"], pull_up=True)
annul = Button(GPIO["annul"], pull_up=True)
erreur = Button(GPIO["erreur"], pull_up=True)
err_idle = Button(GPIO["err_idle"], pull_up=True)
idle_ferme = Button(GPIO["idle_ferme"], pull_up=True)

led_verte = LED(GPIO["led_verte"])
led_jaune = LED(GPIO["led_jaune"])
led_rouge = LED(GPIO["led_rouge"])

buzzer = Buzzer(GPIO["buzzer"])
servo = AngularServo(GPIO["servo"], min_angle=-45, max_angle=45)

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
    
