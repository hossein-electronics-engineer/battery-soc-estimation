#ifndef EKF_SOC_H
#define EKF_SOC_H

typedef struct {
    float q_capacity_coulomb;
    float r0;
    float r1;
    float c1;

    /* State: [SOC, V_RC] */
    float soc;
    float v_rc;

    /* Covariance matrix */
    float P[2][2];

    /* Process noise */
    float Q[2][2];

    /* Measurement noise */
    float R;
} EmbeddedSOCEstimator;

void ekf_init(
    EmbeddedSOCEstimator *est,
    float q_capacity_coulomb,
    float r0,
    float r1,
    float c1
);

void ekf_predict(EmbeddedSOCEstimator *est, float current, float dt);
void ekf_update(EmbeddedSOCEstimator *est, float voltage_measured, float current);
void ekf_step(EmbeddedSOCEstimator *est, float current, float voltage_measured, float dt);

#endif