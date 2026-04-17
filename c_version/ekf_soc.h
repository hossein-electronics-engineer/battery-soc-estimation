#ifndef EKF_SOC_H
#define EKF_SOC_H

typedef struct {
    float q_capacity_coulomb;
    float r0;

    float soc;
    float P;
    float Q;
    float R;
} EmbeddedSOCEstimator;

void ekf_init(EmbeddedSOCEstimator *est, float q_capacity_coulomb, float r0);
void ekf_predict(EmbeddedSOCEstimator *est, float current, float dt);
void ekf_update(EmbeddedSOCEstimator *est, float voltage_measured, float current);
float ekf_step(EmbeddedSOCEstimator *est, float current, float voltage_measured, float dt);

#endif
