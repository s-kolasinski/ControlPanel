from nicegui import ui

# Główna kolumna zajmująca całą szerokość ekranu
with ui.column().classes('w-full'):
    
    # 1. Tytuł: duży tekst (text-4xl), pogrubiony (font-bold) i wyśrodkowany (text-center)
    ui.label('Control Panel') \
        .classes('text-4xl font-bold text-center w-full drop-shadow-md q-my-md')
    
    # 2. Rząd z suwakami
    # 'justify-between' - pierwszy element ląduje po lewej, a ostatni po prawej
    with ui.row().classes('w-full justify-between items-center px-80'):
        
        # Grupa lewego suwaka
        with ui.column().classes('items-center'):
            ui.label("0").classes('items-center ')
            ui.label("angle").classes('items-center')
            gauge = ui.echart({
        'series': [{
            'type': 'gauge',
            'startAngle': 180,  # Zaczynamy od lewej
            'endAngle': 0,      # Kończymy po prawej (półkole)
            'min': 0,
            'max': 100,
            'progress': {'show': True, 'width': 18}, # Szerokość paska
            'itemStyle': {'color': "#68ca30"},       # Kolor (niebieski)
            'detail': {
                'valueAnimation': True, 
                'formatter': '{value}%' # Pokazuje % pod wskazówką
            },
            'data': [{'value': 0, 'name': 'Fuel level'}]
        }]
    }).classes('w-96 h-64') # Ustawiamy rozmiar wskaźnika
            ui.label('Fuel intake')
            ui.slider(min=0, max=100, value=100).classes('w-48').props('label-always track-size="20px" thumb-size="40px" color="green"')
            ui.label('Fuel main')
            ui.slider(min=0, max=100, value=100).classes('w-48').props('label-always track-size="20px" thumb-size="40px" color="green"')

        with ui.column().classes('item-center'):
        
            with ui.row().classes('items-center'):
                ui.switch()
                ui.switch()
                ui.switch()
                
            with ui.row().classes('items-center'):
                ui.label('Igniter')
                ui.label('Parachute')
                ui.label('Oxidizer igniter')
        
        # Grupa prawego suwaka
        with ui.column().classes('items-center'):
            
            gauge = ui.echart({
                    'series': [{
                        'type': 'gauge',
                        'startAngle': 180,  # Zaczynamy od lewej
                        'endAngle': 0,      # Kończymy po prawej (półkole)
                        'min': 0,
                        'max': 100,
                        'progress': {'show': True, 'width': 18}, # Szerokość paska
                        'itemStyle': {'color': "#d1100a"},       # Kolor (niebieski)
                        'detail': {
                            'valueAnimation': True, 
                            'formatter': '{value}%' # Pokazuje % pod wskazówką
                        },
                        'data': [{'value': 0, 'name': 'Oxidizer level'}]
                    }]
                }).classes('w-96 h-64') # Ustawiamy rozmiar wskaźnika
            ui.label('Oxidizer intake')
            ui.slider(min=0, max=100, value=100).classes('w-48').props('label-always track-size="20px" thumb-size="40px" color="red"')
            ui.label('Oxidizer main')
            ui.slider(min=0, max=100, value=100).classes('w-48').props('label-always track-size="20px" thumb-size="40px" color="red"')
                        

ui.run()