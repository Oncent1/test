from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.task import Task
import random

class QuantumCity(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self._init_controls()
        self.player = self.loader.loadModel('models/box')
        self.player.reparentTo(self.render)
        self.player.setScale(0.5, 0.5, 1.0)
        self.player.setColor(1, 0, 0, 1)
        self.player.setPos(0, 0, 0.5)
        self.camera_distance = 8
        self.first_person = False

        self.environment = self.loader.loadModel('models/environment')
        self.environment.reparentTo(self.render)
        self.environment.setScale(0.25)
        self.environment.setPos(-8, 42, 0)

        self._build_city()
        self.taskMgr.add(self.update, 'update')

    def _init_controls(self):
        self.accept('escape', self.userExit)
        self.keys = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'turn_left': False,
            'turn_right': False,
        }
        for key in ['w', 's', 'a', 'd', 'arrow_left', 'arrow_right']:
            self.accept(key, self._set_key, [key, True])
            self.accept(f'{key}-up', self._set_key, [key, False])
        self.accept('c', self._toggle_view)
        self.accept('q', self._quantum_leap)

    def _set_key(self, key, value):
        mapping = {
            'w': 'forward',
            's': 'backward',
            'a': 'left',
            'd': 'right',
            'arrow_left': 'turn_left',
            'arrow_right': 'turn_right',
        }
        if key in mapping:
            self.keys[mapping[key]] = value

    def _toggle_view(self):
        self.first_person = not self.first_person

    def _quantum_leap(self):
        x = random.uniform(-25, 25)
        y = random.uniform(-25, 25)
        self.player.setPos(x, y, 0.5)

    def _build_city(self):
        ground = self.loader.loadModel('models/box')
        ground.reparentTo(self.render)
        ground.setScale(50, 50, 0.1)
        ground.setPos(0, 0, -0.05)
        ground.setColor(0.5, 0.5, 0.5, 1)

        for i in range(-10, 11, 2):
            for j in range(-10, 11, 2):
                if i == 0 and j == 0:
                    continue
                self._create_building(i * 2, j * 2)

    def _create_building(self, x, y):
        height = random.uniform(2.0, 8.0)
        levels = random.randint(1, 3)
        level_height = height / levels
        base_x = random.uniform(0.8, 2.5)
        base_y = random.uniform(0.8, 2.5)
        cur_z = 0.0
        for _ in range(levels):
            b = self.loader.loadModel('models/box')
            b.reparentTo(self.render)
            shrink = random.uniform(0.7, 1.0)
            b.setScale(base_x * shrink, base_y * shrink, level_height)
            b.setPos(x, y, cur_z + level_height / 2)
            shade = 0.4 + random.random() * 0.6
            b.setColor(shade, shade, shade, 1)
            cur_z += level_height

    def update(self, task):
        dt = globalClock.getDt()
        pos = self.player.getPos()
        hpr = self.player.getHpr()
        speed = 10
        turn_speed = 60
        if self.keys['forward']:
            pos += self.player.getQuat().getForward() * (speed * dt)
        if self.keys['backward']:
            pos -= self.player.getQuat().getForward() * (speed * dt)
        if self.keys['left']:
            pos -= self.player.getQuat().getRight() * (speed * dt)
        if self.keys['right']:
            pos += self.player.getQuat().getRight() * (speed * dt)
        if self.keys['turn_left']:
            hpr.x -= turn_speed * dt
        if self.keys['turn_right']:
            hpr.x += turn_speed * dt
        self.player.setPos(pos)
        self.player.setHpr(hpr)

        if self.first_person:
            self.camera.reparentTo(self.player)
            self.camera.setPos(0, 0, 1)
            self.camera.setHpr(0, 0, 0)
        else:
            self.camera.reparentTo(self.render)
            cam_pos = pos - self.player.getQuat().getForward() * self.camera_distance + Vec3(0,0,3)
            self.camera.setPos(cam_pos)
            self.camera.lookAt(self.player)

        return Task.cont


if __name__ == '__main__':
    app = QuantumCity()
    app.run()
