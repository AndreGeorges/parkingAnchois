
.
├── assets
│   ├── images
│   │   └── fond.jpg
│   └── __init__.py
├── config
│   ├── config_loader.py                    *** ancien config.py
│   ├── __init__.py
<!-- │   ├── __pycache__
│   │   ├── config.cpython-313.pyc
│   │   ├── config_loader.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── logsconfig.cpython-313.pyc
│   │   └── ui_config.cpython-313.pyc -->
│   └── ui_config.py                        ***  get_tarif() get_screen_color() get_color()
├── config.yaml
├── controllers
│   ├── email_controller.py                 *** ancien comm.py (logique email)
│   ├── gpio_controller.py                  *** ancien gpio_manager.py
│   ├── __init__.py
│   ├── parking_controller.py               *** ancien crud.py
<!-- │   ├── __pycache__
│   │   ├── email_controller.cpython-313.pyc
│   │   ├── gpio_controller.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── parking_controller.cpython-313.pyc
│   │   └── state_controller.cpython-313.pyc -->
│   └── state_controller.py                 *** eviter_surcharge_...
├── data
│   ├── db.json
│   └── transactions.json
├── Diagramme_etat_stationnement.png
├── exports
│   └── __init__.py
├── logs
│   ├── __init__.py
│   └── parking.log
├── main.py
├── models
│   ├── __init__.py
│   ├── logger_manager.py                               *** ancien logsconfig.py
│   ├── parking.py                                      *** ancien shared_state.py
<!-- │   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── logger_manager.cpython-313.pyc
│   │   ├── parking.cpython-313.pyc
│   │   ├── state_machine.cpython-313.pyc
│   │   └── vehicle.cpython-313.pyc -->
│   ├── state_machine.py                                *** ancien etats.py
│   └── vehicle.py                                      *** ancien liste_vehicules.py
<!-- ├── __pycache__
│   ├── api.cpython-313.pyc
│   ├── comm.cpython-313.pyc
│   ├── config.cpython-313.pyc
│   ├── crud.cpython-313.pyc
│   ├── etats.cpython-313.pyc
│   ├── gpio_manager.cpython-313.pyc
│   ├── liste_vehicules.cpython-313.pyc
│   ├── logsconfig.cpython-313.pyc
│   ├── logsmtp.cpython-313.pyc
│   ├── main.cpython-313.pyc
│   ├── shared_state.cpython-313.pyc
│   ├── ui_pygame.cpython-313.pyc
│   └── utils.cpython-313.pyc -->
├── README.md
├── services
│   ├── email_service.py                            *** ancien comm.py (SMTP / envoi email)
│   ├── __init__.py
<!-- │   ├── __pycache__
│   │   ├── email_service.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   └── weather_service.cpython-313.pyc -->
│   └── weather_service.py                          *** ancien api.py
└── views
    ├── __init__.py
    <!-- ├── __pycache__
    │   ├── __init__.cpython-313.pyc
    │   └── pygame_view.cpython-313.pyc -->
    ├── pygame_view.py                              *** ancien ui_pygame.py
    └── tkinter_auth_view.py                        *** ancien ui_tkinter.py

17 directories, 63 files


utils:
def eviter_surcharge_etat()
def eviter_surcharge_event()      --->   controllers/state_controller.py

get_tarif()
get_screen_color()
get_color()                     ---->   config/ui_config.py

draw_keyboard()
draw_button()
bouton_accueil()                ---->  views/pygame_view.py


