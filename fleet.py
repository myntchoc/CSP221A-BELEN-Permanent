#Fleet management system

from abc import ABC, abstractmethod


class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available
        message = (
            f"{robot_name} needs {required}% battery for this task "
            f"but only has {available}%."
        )
        super().__init__(message)


class Robot(ABC):
    #Base class for all robots in the fleet

    manufacturer = "Fleet Robotics"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return f"{type(self).__name__}(name={self.name!r}, battery={self.battery})"

    def use_battery(self, amount):
        if self.battery < amount:
            raise InsufficientBatteryError(self.name, amount, self.battery)
        self.battery -= amount

    @abstractmethod
    def perform_task(self):
        #Perform the task assigned to the robot.
        pass


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=10):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    def perform_task(self):
        self.use_battery(15)
        return f"{self.name} is cleaning the area."


class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self):
        self.use_battery(10)
        return f"{self.name} is surveying the area from the air."
