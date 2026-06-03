parkinganchois/
│
├── main.py
├── README.md
├── config.yaml

├── parking.log
│
├── config/
│   ├── __init__.py
│   └── config_loader.py        *** ancien config.py
|   |----logsconfig.py
│
├── models/
│   ├── state_machine.py        *** ancien etats.py
│   ├── parking.py              *** ancien shared_state.py
│   ├── vehicle.py              *** ancien liste_vehicules.py

│
├── controllers/
│   ├── parking_controller.py   *** ancien crud.py
│   ├── gpio_controller.py      *** ancien gpio_manager.py
│   ├── email_controller.py     *** ancien comm.py (logique email)
│   └── state_controller.py     *** eviter_surcharge_...
│
├── services/
│   ├── weather_service.py      *** ancien api.py
│   ├── email_service.py        *** ancien comm.py (SMTP / envoi email)

│
├── views/
│   ├── pygame_view.py          *** ancien ui_pygame.py
│   └── tkinter_auth_view.py    *** ancien ui_tkinter.py

├── data/
    ├── db.json
    ├── transactions.json

├── logs/
    ├── parking.log
│
├── assets/
│   ├── images/
│   ├── weather_icons/
│   └── sounds/
│
└── exports/





utils:
def eviter_surcharge_etat()
def eviter_surcharge_event()      --->   controllers/state_controller.py

get_tarif()
get_screen_color()
get_color()                     ---->   config/ui_config.py

draw_keyboard()
draw_button()
bouton_accueil()                ---->  views/pygame_view.py
