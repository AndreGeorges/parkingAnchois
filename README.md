parkinganchois/
│
├── main.py
├── README.md
├── config.yaml
├── db.json
├── transactions.json
├── parking.log
│
├── config/
│   ├── __init__.py
│   └── config_loader.py        *** ancien config.py
│
├── models/
│   ├── state_machine.py        *** ancien etats.py
│   ├── parking.py              *** ancien shared_state.py
│   ├── vehicle.py              *** ancien liste_vehicules.py
│   └── logger_manager.py       *** ancien logsconfig.py (migration en cours)
│
├── controllers/
│   ├── parking_controller.py   *** ancien crud.py
│   ├── gpio_controller.py      *** ancien gpio_manager.py
│   ├── email_controller.py     *** ancien comm.py (logique email)
│   └── weather_controller.py   *** wrapper de weather_service.py
│
├── services/
│   ├── weather_service.py      *** ancien api.py
│   ├── email_service.py        *** ancien comm.py (SMTP / envoi email)
│   └── log_export_service.py   *** export logs (prévu / optionnel)
│
├── views/
│   ├── pygame_view.py          *** ancien ui_pygame.py
│   └── tkinter_auth_view.py    *** ancien ui_tkinter.py
│
├── assets/
│   ├── images/
│   ├── weather_icons/
│   └── sounds/
│
└── exports/