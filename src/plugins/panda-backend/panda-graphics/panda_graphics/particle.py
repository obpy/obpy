#
# <module description>
# See <TODO: No Sphinx docs yet - add some> for the primary source of documentation
# for this module.
#
# Copyright (C) 2012 The OpenBlox Project
#
# This file is part of The OpenBlox Game Engine.
#
#     The OpenBlox Game Engine is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     The OpenBlox Game Engine is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with The OpenBlox Game Engine.  If not, see <http://www.gnu.org/licenses/>.
#


__author__ = "openblocks"
__date__ = "Jul 19, 2012 6:01:26 PM"


from direct.particles.Particles import *
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup

import obengine.datatypes
import obplugin.panda_utils

import texture


class ParticleEmitter(obplugin.panda_utils.PandaResource):

    def __init__(self, window):

        self._window = window

        self._particle_effect = ParticleEffect()
        self._reset()

    @obengine.datatypes.nested_property
    def particle_lifespan():

        def fget(self):
            return self._particle_lifespan

        def fset(self, new_lifespan):

            self._particle_lifespan = new_lifespan
            self._particle_generator.factory.setLifespanBase(self._particle_lifespan)

        return locals()

    @obengine.datatypes.nested_property
    def particle_birthrate():

        def fget(self):
            return self._particle_birthrate

        def fset(self, new_birthrate):

            self._particle_birthrate = new_birthrate
            self._particle_generator.setBirthRate(self._particle_birthrate)

        return locals()

    @obengine.datatypes.nested_property
    def particle_rise_velocity():

        def fget(self):
            return self._particle_velocity

        def fset(self, new_velocity):

            self._particle_velocity = new_velocity
            self._particle_generator.emitter.setOffsetForce(Vec3(0.0, 0.0, self._particle_velocity))

        return locals()

    @obengine.datatypes.nested_property
    def particle_texture():

        def fget(self):
            return self._particle_texture

        def fset(self, new_texture):

            self._particle_texture = new_texture
            self._particle_generator.renderer.setTexture(new_texture.texture)

        return locals()

    @obengine.datatypes.nested_property
    def disable_alpha():

        def fget(self):
            return self._disable_alpha

        def fset(self, disable_alpha):

            self._disable_alpha = disable_alpha
            self._particle_generator.renderer.setAlphaDisable(self._disable_alpha)

        return locals()

    def _reset(self):

        self._particle_effect.reset()
        self._particle_generator = Particles()

        self._particle_generator.setFactory("PointParticleFactory")
        self._particle_generator.setRenderer("SpriteParticleRenderer")
        self._particle_generator.setEmitter("DiscEmitter")
        self._particle_generator.setPoolSize(10000)
        self._particle_generator.setBirthRate(0.25)
        self._particle_generator.setLitterSize(20)
        self._particle_generator.setLitterSpread(0)
        self._particle_generator.setSystemLifespan(0.0)
        self._particle_generator.setLocalVelocityFlag(True)
        self._particle_generator.setSystemGrowsOlderFlag(False)

        self.particle_lifespan = 8.0
        self._particle_generator.factory.setLifespanSpread(0.0)
        self._particle_generator.factory.setMassBase(1.0)
        self._particle_generator.factory.setMassSpread(0.0)
        self._particle_generator.factory.setTerminalVelocityBase(400.0)
        self._particle_generator.factory.setTerminalVelocitySpread(0.0)

        self._particle_generator.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self._particle_generator.renderer.setUserAlpha(0.1)

        default_texture = texture.Texture('smoke.png')
        default_texture.on_loaded += lambda: self._set_texture(default_texture)
        default_texture.load()

        self._particle_generator.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self._particle_generator.renderer.setXScaleFlag(True)
        self._particle_generator.renderer.setYScaleFlag(True)
        self._particle_generator.renderer.setAnimAngleFlag(False)
        self._particle_generator.renderer.setInitialXScale(0.0025)
        self._particle_generator.renderer.setFinalXScale(0.04)
        self._particle_generator.renderer.setInitialYScale(0.0025)
        self._particle_generator.renderer.setFinalYScale(0.04)
        self._particle_generator.renderer.setNonanimatedTheta(0.0)
        self._particle_generator.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self._disable_alpha = False

        self._particle_generator.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self._particle_generator.emitter.setAmplitude(1.0)
        self._particle_generator.emitter.setAmplitudeSpread(0.75)
        self.particle_rise_velocity = 1.0
        self._particle_generator.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self._particle_generator.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

        self._particle_effect.addParticles(self._particle_generator)

        particle_force_group = ForceGroup()
        rising_force = LinearNoiseForce(0.15, 0.0)
        rising_force.setActive(True)
        particle_force_group.addForce(rising_force)
        self._particle_effect.addForceGroup(particle_force_group)

        self._particle_generator.nodePath.setLightOff()
        self._particle_generator.nodePath.setTransparency(TransparencyAttrib.MDual, 1)

        self._particle_effect.start(self._window.panda_window.render)

    def _set_texture(self, default_texture):
        self.particle_texture = default_texture
