from nicegui import ui, app
from functions import receive_frames, handle_relay, handle_servo, launch_rocket
from data import data

#Functions:
#1. create_gauge
#2. set_altitude
#3. update_ui


#UI strcture:
#   -TITLE
#   -main row:
#       -left panel:
#           -angle_label
#           -fuel_gauge
#           -fuel_intake_slider   
#       -middle panel:
#           -altitude bar
#           -sw_parachute & sw_ox_igniter
#           -launch_btn
#       -right panel:   
#           -ox_pressure_label
#           -ox_gauge
#           -ox_intake_slider



MAX_ALTITUDE = 1000 #[m] Used for altitude bar
UI_UPDATE_TIME = 0.01 #[s]



def create_gauge(name: str, color: str):
    """creates gauge"""
    return ui.echart({
        'series': [{
            'type': 'gauge',
            'animationDurationUpdate': UI_UPDATE_TIME*1000, #in ms
            'animationEasingUpdate': 'linear',
            'startAngle': 180,
            'endAngle': 0,
            'min': 0,
            'max': 100,
            'center': ['50%', '70%'],
            'radius': '100%',
            'progress': {'show': True, 'width': 16},
            'itemStyle': {'color': color},
            'axisLine': {
                'lineStyle': {
                    'width': 16,
                    'color': [[1, '#1e293b']],
                }
            },
            'axisTick': {'distance': -22, 'lineStyle': {'color': '#475569'}},
            'splitLine': {
                'distance': -26,
                'length': 10,
                'lineStyle': {'color': '#64748b', 'width': 2},
            },
            'axisLabel': {'distance': 12, 'color': '#94a3b8', 'fontSize': 11},
            'pointer': {'itemStyle': {'color': color}, 'length': '65%'},
            'title': {
                'offsetCenter': [0, '20%'],
                'color': '#94a3b8',
                'fontSize': 13,
            },
            'detail': {
                'valueAnimation': True,
                'formatter': '{value}%',
                'color': '#f8fafc',
                'fontSize': 24,
                'offsetCenter': [0, '-15%'],
            },
            'data': [{'value': 0, 'name': name}],
        }]
    }).classes('w-80 h-52')



def set_altitude(current_meters: float, max_altitude: float):
    """updates altitude bar"""
    percent = max(0.0, min(100.0, (current_meters / max_altitude) * 100.0))
    altitude_label.set_text(f'{current_meters:.0f} m')
    altitude_fill.style(f'height: {percent}%')
    rocket_marker.style(f'bottom: {percent}%')


def update_ui():
    """updates altitude bar and gauges"""
    fuel_gauge.options['series'][0]['data'][0]['value'] = data['fuel_level']
    fuel_gauge.update()
    
    ox_gauge.options['series'][0]['data'][0]['value'] = data['ox_level']
    ox_gauge.update()

    set_altitude(data['altitude'], MAX_ALTITUDE)




ui.dark_mode().enable()
ui.query('body').classes('bg-slate-950 text-slate-100 select-none')


# Main column
with ui.column().classes('w-full min-h-screen px-8 py-6 justify-between'):

    # Title
    with ui.column().classes('w-full items-center mb-2'):
        ui.label('CONTROL PANEL').classes(
            'text-4xl font-black tracking-widest text-center text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-slate-400 drop-shadow-lg'
        )
        ui.element('div').classes(
            'w-32 h-1 bg-cyan-500 rounded-full mt-1 shadow-[0_0_12px_#06b6d4]'
        )   

    # Main row (left panel | middle panel | right panel)
    with ui.row().classes(
        'w-full justify-between items-stretch gap-8 flex-nowrap'
    ):

        # === Left column (ANGLE, FUEL_LEVEL, FUEL_INTAKE) ===
        with ui.card().classes(
            'items-center bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl w-96 justify-between'
        ):
            with ui.column().classes(
                'items-center bg-slate-950/80 px-6 py-3 rounded-xl border border-slate-800/80 w-full'
            ):
                angle_label = ui.label().bind_text_from(data, 'angle', backward=lambda x: f'{x}°').classes(
                    'text-3xl font-mono font-bold text-emerald-400 tracking-wider'
                )
                ui.label('ANGLE').classes(
                    'text-xs uppercase tracking-widest text-slate-400 font-semibold'
                )

            fuel_gauge = create_gauge('Fuel Level', '#10b981')

            with ui.column().classes('w-full items-center gap-4 mt-2'):
                with ui.column().classes('w-full items-center'):
                    ui.label('FUEL INTAKE').classes(
                        'text-xs uppercase tracking-wider text-slate-300 font-semibold mb-6'
                    )
                    fuel_intake_slider = (
                        ui.slider(min=0, max=100, value=100)
                        .classes('w-64')
                        .props(
                            'label-always track-size="10px" thumb-size="24px" color="emerald-5"'
                        ).on('change', lambda e: handle_servo(e, 0))
                    )


        # ==== Middle column (ALTITUDE BAR, PARACHUTE & OXIDIZER_HEATER SWITCHES, LAUNCH BUTTON) ===
        with ui.column().classes('items-center justify-between flex-grow gap-4'):

            #ALTITUDE BAR
            with ui.card().classes(
                'w-full flex-grow bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl flex flex-col justify-between items-center'
            ):
                
                with ui.row().classes('w-full justify-between items-center'):
                    with ui.column().classes('gap-0'):
                        ui.label('ROCKET ALTITUDE').classes(
                            'text-sm font-bold uppercase tracking-widest text-slate-300'
                        )
                        ui.label(f'Target Apogee: {MAX_ALTITUDE} m').classes(
                            'text-xs text-slate-500'
                        )
                    altitude_label = ui.label('0 m').classes(
                        'text-3xl font-mono font-bold text-cyan-400'
                    )

                with ui.row().classes(
                    ' items-center justify-center gap-6 my-4 flex-grow'
                ):
                    with ui.column().classes(
                        'h-64 justify-between items-end text-xs font-mono text-slate-400 py-1'
                    ):
                        ui.label(f'{int(MAX_ALTITUDE)} m')
                        ui.label(f'{int(MAX_ALTITUDE * 0.75)} m')
                        ui.label(f'{int(MAX_ALTITUDE * 0.50)} m')
                        ui.label(f'{int(MAX_ALTITUDE * 0.25)} m')
                        ui.label('0 m')

                    
                    with ui.element('div').classes(
                        'relative w-14 h-64 bg-slate-950 rounded-full border-2 border-slate-800 flex flex-col justify-end p-1 shadow-inner'
                    ):
                        
                        for pos in [25, 50, 75]:
                            ui.element('div').classes(
                                'absolute left-2 right-2 border-b border-dashed border-slate-800/80'
                            ).style(f'bottom: {pos}%')

                        
                        altitude_fill = (
                            ui.element('div')
                            .classes(
                                'w-full bg-gradient-to-t from-cyan-900/60 via-cyan-500/80 to-cyan-300 rounded-full transition-all duration-300'
                            )
                            .style('height: 0%')
                        )

                        
                        rocket_marker = (
                            ui.element('div')
                            .classes(
                                'absolute left-1/2 -translate-x-1/2 translate-y-1/2 transition-all duration-300 z-10 flex flex-col items-center'
                            )
                            .style('bottom: 0%')
                        )
                        with rocket_marker:
                            ui.icon('rocket', size='34px').classes(
                                'text-white drop-shadow-[0_0_10px_#06b6d4]'
                            )

                ui.label('GROUND LEVEL').classes(
                    'text-[10px] font-mono uppercase tracking-widest text-slate-500'
                )

            #SWITCHES PANEL
            with ui.card().classes(
                'bg-slate-900/90 border border-slate-800 rounded-2xl px-10 py-4 shadow-2xl w-full items-center'
            ):
                with ui.row().classes('items-center justify-around w-full'):

                    with ui.column().classes('items-center gap-1'):
                        sw_parachute = ui.switch(on_change = lambda e: handle_relay(e, 2)).props(
                            'color="cyan-5" size="lg"'
                        )
                        ui.label('PARACHUTE').classes(
                            'text-xs font-bold uppercase tracking-wider text-slate-300'
                        )

                    with ui.column().classes('items-center gap-1'):
                        sw_ox_igniter = ui.switch(on_change = lambda e: handle_relay(e, 0)).props(
                            'color="red-5" size="lg"'
                        )
                        ui.label('OXIDIZER IGNITER').classes(
                            'text-xs font-bold uppercase tracking-wider text-slate-300'
                        )

            # START BUTTON
            launch_btn = (
            ui.button('LAUNCH', on_click = launch_rocket, icon='rocket_launch')
            .classes(
                'w-full py-4 rounded-2xl text-xl font-black tracking-widest '
                'shadow-[0_0_20px_rgba(34,197,94,0.4)] transition-all duration-300 '
                'border-2 border-green-500 bg-green-950/80 hover:bg-green-500 '
                'hover:shadow-[0_0_35px_rgba(34,197,94,0.8)] text-green-400 hover:text-slate-950'
            )
            .props('flat')
        )
        # === Right column (OXIDIZER_PRESSURE, OXIDIZER_LEVEL, OXIDIZER_INTAKE) ===
        with ui.card().classes(
            'items-center bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl w-96 justify-between'
        ):
            with ui.column().classes(
                'items-center bg-slate-950/80 px-6 py-3 rounded-xl border border-slate-800/80 w-full'
            ):
                ox_pressure_label = ui.label().bind_text_from(data, 'ox_pressure', backward=lambda x: f'{float(x):.2f} bar').classes(
                    'text-3xl font-mono font-bold text-rose-500 tracking-wider'
                )
                ui.label('OXIDIZER PRESSURE').classes(
                    'text-xs uppercase tracking-widest text-slate-400 font-semibold'
                )

            ox_gauge = create_gauge('Oxidizer Level', '#f43f5e')

            with ui.column().classes('w-full items-center gap-4 mt-2'):
                with ui.column().classes('w-full items-center'):
                    ui.label('OXIDIZER INTAKE').classes(
                        'text-xs uppercase tracking-wider text-slate-300 font-semibold mb-6'
                    )
                    ox_intake_slider = (
                        ui.slider(min=0, max=100, value=100)
                        .classes('w-64')
                        .props(
                            'label-always track-size="10px" thumb-size="24px" color="red-5"'
                        ).on('change', lambda e: handle_servo(e, 1))
                    )



ui.timer(UI_UPDATE_TIME, update_ui)

app.on_startup(receive_frames)

ui.run()