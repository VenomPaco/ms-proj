
from math import sqrt, pi
from vector import Vector3D
import vector

GM: float = 3.986004418e14      # m^3 s^-2
EARTH_RADIUS: float = 6.371e6   # m

class OrbitalPlane:
    __id = 0

    @staticmethod
    def __next_id() -> int:
        ret = OrbitalPlane.__id
        OrbitalPlane.__id += 1
        return ret

    def __init__(self, eccentricity: float = 0, semimajor_axis: float = 0,
            inclination: float = 0, longitude: float = 0):
        if eccentricity != 0:
            raise NotImplementedError
        
        self.id = OrbitalPlane.__next_id()

        self.eccentricity = eccentricity
        self.semimajor_axis = semimajor_axis
        self.inclination = inclination
        self.longitude = longitude

        self.orbital_speed = sqrt(GM / semimajor_axis)
        self.angular_speed = self.orbital_speed / semimajor_axis

    @property
    def orbital_period(self) -> float:
        return 2 * pi * sqrt(pow(self.semimajor_axis, 3) / GM)

class Satellite:
    __id = 0

    def __next_id() -> int:
        ret = Satellite.__id
        Satellite.__id += 1
        return ret

    def __init__(self, orbital_plane: OrbitalPlane, arg_periapsis: float = 0):
        self.id = Satellite.__next_id()
        
        self.orbital_plane = orbital_plane
        self.arg_periapsis = arg_periapsis

        self.connections = set()

    def calc_position(self, t: float) -> Vector3D:
        r = self.orbital_plane.semimajor_axis
        true_anomaly = (t * self.orbital_plane.angular_speed) % (2 * pi)

        position: Vector3D = vector.obj(x=r, y=0, z=0)
        return (position.rotateY(self.arg_periapsis + true_anomaly)
                        .rotateX(self.orbital_plane.inclination)
                        .rotateY(self.orbital_plane.longitude))

    def calc_velocity(self, t: float) -> Vector3D:
        direction = self.calc_position(t).rotateY(pi / 2).unit()
        return self.orbital_plane.orbital_speed * direction

    def connect(self, other_id: int):
        self.connections.add(other_id)

    def disconnect(self, other_id: int):
        self.connections.remove(other_id)

    def distance_to(self, other: 'Satellite', t: float):
        self_pos = self.calc_position(t)
        other_pos = other.calc_position(t)
        return (self_pos - other_pos).mag

if __name__ == "__main__":
    semimajor_axis = 6_921_000
    inclination = 0.6
    
    s1 = Satellite(OrbitalPlane(0, semimajor_axis, inclination, 0), 0)
    s2 = Satellite(OrbitalPlane(0, semimajor_axis, inclination, 1), 0)
    
    print(s1.calc_position(0), s2.calc_position(0), s1.distance_to(s2, 0))