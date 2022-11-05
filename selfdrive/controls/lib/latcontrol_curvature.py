import math

from cereal import log
from selfdrive.controls.lib.latcontrol import LatControl, MIN_STEER_SPEED
from selfdrive.controls.lib.pid import PIDController


class LatControlCurvature(LatControl):
  def __init__(self, CP, CI):
    super().__init__(CP, CI)
    self.steer_max = 0.02
    self.pid = PIDController((CP.lateralTuning.pid.kpBP, CP.lateralTuning.pid.kpV),
                             (CP.lateralTuning.pid.kiBP, CP.lateralTuning.pid.kiV),
                             k_f=CP.lateralTuning.pid.kf, pos_limit=self.steer_max, neg_limit=-self.steer_max)

  def reset(self):
    super().reset()
    self.pid.reset()

  def update(self, active, CS, VM, params, last_actuators, steer_limited, desired_curvature, desired_curvature_rate, llk):
    curvature_log = log.ControlsState.LateralCurvatureState.new_message()

    curvature_log.actualCurvature = -VM.calc_curvature(math.radians(CS.steeringAngleDeg - params.angleOffsetDeg), CS.vEgo, params.roll)
    curvature_log.desiredCurvature = desired_curvature
    curvature_log.error = desired_curvature - curvature_log.actualCurvature

    if CS.vEgo < MIN_STEER_SPEED or not active:
      output = 0.0
      curvature_log.active = False
    else:
      freeze_integrator = steer_limited or CS.steeringPressed or CS.vEgo < 5
      output = self.pid.update(curvature_log.error,
                               feedforward=desired_curvature,
                               speed=CS.vEgo,
                               freeze_integrator=freeze_integrator)

      curvature_log.active = True
      curvature_log.p = self.pid.p
      curvature_log.i = self.pid.i
      curvature_log.d = self.pid.d
      curvature_log.f = self.pid.f
      curvature_log.output = -output

    return 0., 0., -output, curvature_log