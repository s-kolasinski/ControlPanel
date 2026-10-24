from communication_library.frame import Frame
from communication_library import ids
from communication_library.communication_manager import CommunicationManager


def send_frame(cm: CommunicationManager, priority: ids.PriorityID, device_type: ids.DeviceID, device: int, value: int = 0, operation: ids._RelayOperationID = ids._RelayOperationID.CLOSE) -> None:
    if device_type == ids.DeviceID.SERVO:
        frame = Frame(ids.BoardID.SOFTWARE,
                  priority,
                  ids.ActionID.SERVICE,
                  ids.BoardID.ROCKET,
                  device_type,
                  device,
                  ids.DataTypeID.INT16,
                  ids.OperationID.SERVO.value.POSITION,
                  (value, )
                  )
    elif device_type == ids.DeviceID.RELAY:
        frame = Frame(ids.BoardID.SOFTWARE,
                      priority,
                      ids.ActionID.SERVICE,
                      ids.BoardID.ROCKET,
                      device_type,
                      device,
                      ids.DataTypeID.NO_DATA,
                      operation,
                      tuple()
                      )

    cm.push(frame)
    cm.send()


def update_fuel_level(frame: Frame)->None:
    fuel_level = frame.as_dict()['payload'][0]
    print(f"Fuel level: {fuel_level}")

def update_oxidizer_level(frame: Frame)->None:
    oxidizer_level = frame.as_dict()['payload'][0]
    print(f"Oxidizer level: {oxidizer_level}")

def update_altitude(frame: Frame)->None:
    altitude = frame.as_dict()['payload'][0]
    print(f"Altitude: {altitude}")

def update_oxidizer_pressure(frame: Frame)->None:
    oxidizer_pressure = frame.as_dict()['payload'][0]
    print(f"Oxidizer pressure: {oxidizer_pressure}")

def update_angle(frame: Frame)->None:
    angle = frame.as_dict()['payload'][0]
    print(f"Angle: {angle}")

def register_callbacks(cm: CommunicationManager)->None:
    fuel_level_frame = Frame(ids.BoardID.SOFTWARE,
                            ids.PriorityID.LOW,
                            ids.ActionID.FEED,
                            ids.BoardID.ROCKET,
                            ids.DeviceID.SENSOR,
                            0, #fuel level
                            ids.DataTypeID.FLOAT,
                            ids.OperationID.SENSOR.value.READ,
                            ()
                        )
    oxidizer_level_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                1, #oxidizer level
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    altitude_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                2, #altitude
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    oxidizer_pressure_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                3, #oxidizer pressure
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    angle_frame = Frame(ids.BoardID.SOFTWARE,
                                ids.PriorityID.LOW,
                                ids.ActionID.FEED,
                                ids.BoardID.ROCKET,
                                ids.DeviceID.SENSOR,
                                4, #angle
                                ids.DataTypeID.FLOAT,
                                ids.OperationID.SENSOR.value.READ,
                                ()
                            )
    cm.register_callback(update_fuel_level, fuel_level_frame)
    cm.register_callback(update_oxidizer_pressure, oxidizer_level_frame)
    cm.register_callback(update_altitude, altitude_frame)
    cm.register_callback(update_oxidizer_pressure, oxidizer_pressure_frame)
    cm.register_callback(update_angle, angle_frame)