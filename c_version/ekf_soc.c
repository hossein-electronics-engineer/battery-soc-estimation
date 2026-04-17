#include "ekf_soc.h"
#include <math.h>

static float clamp(float x, float min_val, float max_val) {
    if (x < min_val) return min_val;
    if (x > max_val) return max_val;
    return x;
}

static float ocv_from_soc(float soc) {
    soc = clamp(soc, 0.0f, 1.0f);
    return 3.0f + 1.2f * soc + 0.1f * sinf(2.0f * 3.1415926f * soc);
}

void ekf_init(EmbeddedSOCEstimator *est, float q_capacity_coulomb, float r0) {
    est->q_capacity_coulomb = q_capacity_coulomb;
    est->r0 = r0;

    est->soc = 0.9f;
    est->P = 1e-4f;
    est->Q = 1e-6f;
    est->R = 1e-3f;
}

void ekf_predict(EmbeddedSOCEstimator *est, float current, float dt) {
    est->soc = est->soc - (current * dt) / est->q_capacity_coulomb;
    est->soc = clamp(est->soc, 0.0f, 1.0f);

    est->P = est->P + est->Q;
}

void ekf_update(EmbeddedSOCEstimator *est, float voltage_measured, float current) {
    float soc = est->soc;
    float v_pred = ocv_from_soc(soc) - current * est->r0;

    float eps = 1e-5f;
    float soc_plus = clamp(soc + eps, 0.0f, 1.0f);
    float soc_minus = clamp(soc - eps, 0.0f, 1.0f);

    float d_ocv = (ocv_from_soc(soc_plus) - ocv_from_soc(soc_minus)) /
                  (soc_plus - soc_minus + 1e-12f);

    float H = d_ocv;
    float y = voltage_measured - v_pred;
    float S = H * est->P * H + est->R;
    float K = (est->P * H) / S;

    est->soc = est->soc + K * y;
    est->soc = clamp(est->soc, 0.0f, 1.0f);

    est->P = (1.0f - K * H) * est->P;
}

float ekf_step(EmbeddedSOCEstimator *est, float current, float voltage_measured, float dt) {
    ekf_predict(est, current, dt);
    ekf_update(est, voltage_measured, current);
    return est->soc;
}
