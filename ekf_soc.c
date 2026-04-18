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

void ekf_init(
    EmbeddedSOCEstimator *est,
    float q_capacity_coulomb,
    float r0,
    float r1,
    float c1
) {
    est->q_capacity_coulomb = q_capacity_coulomb;
    est->r0 = r0;
    est->r1 = r1;
    est->c1 = c1;

    est->soc = 0.9f;
    est->v_rc = 0.0f;

    est->P[0][0] = 1e-4f;
    est->P[0][1] = 0.0f;
    est->P[1][0] = 0.0f;
    est->P[1][1] = 1e-4f;

    est->Q[0][0] = 1e-6f;
    est->Q[0][1] = 0.0f;
    est->Q[1][0] = 0.0f;
    est->Q[1][1] = 1e-5f;

    est->R = 1e-2f;
}

void ekf_predict(EmbeddedSOCEstimator *est, float current, float dt) {
    float alpha = expf(-dt / (est->r1 * est->c1));

    float soc_pred = est->soc - (current * dt) / est->q_capacity_coulomb;
    soc_pred = clamp(soc_pred, 0.0f, 1.0f);

    float vrc_pred = alpha * est->v_rc + est->r1 * (1.0f - alpha) * current;

    est->soc = soc_pred;
    est->v_rc = vrc_pred;

    /* F = [[1, 0],
            [0, alpha]] */

    float P00 = est->P[0][0];
    float P01 = est->P[0][1];
    float P10 = est->P[1][0];
    float P11 = est->P[1][1];

    float FP00 = P00;
    float FP01 = P01;
    float FP10 = alpha * P10;
    float FP11 = alpha * P11;

    float Pnew00 = FP00;
    float Pnew01 = alpha * FP01;
    float Pnew10 = FP10;
    float Pnew11 = alpha * FP11;

    est->P[0][0] = Pnew00 + est->Q[0][0];
    est->P[0][1] = Pnew01 + est->Q[0][1];
    est->P[1][0] = Pnew10 + est->Q[1][0];
    est->P[1][1] = Pnew11 + est->Q[1][1];
}

void ekf_update(EmbeddedSOCEstimator *est, float voltage_measured, float current) {
    float soc = est->soc;
    float v_rc = est->v_rc;

    float v_pred = ocv_from_soc(soc) - current * est->r0 - v_rc;

    float eps = 1e-5f;
    float soc_plus = clamp(soc + eps, 0.0f, 1.0f);
    float soc_minus = clamp(soc - eps, 0.0f, 1.0f);

    float d_ocv = (ocv_from_soc(soc_plus) - ocv_from_soc(soc_minus)) /
                  (soc_plus - soc_minus + 1e-12f);

    /* H = [d_ocv, -1] */
    float H0 = d_ocv;
    float H1 = -1.0f;

    float y = voltage_measured - v_pred;

    float P00 = est->P[0][0];
    float P01 = est->P[0][1];
    float P10 = est->P[1][0];
    float P11 = est->P[1][1];

    float S = H0 * (P00 * H0 + P01 * H1) +
              H1 * (P10 * H0 + P11 * H1) +
              est->R;

    float K0 = (P00 * H0 + P01 * H1) / S;
    float K1 = (P10 * H0 + P11 * H1) / S;

    est->soc = est->soc + K0 * y;
    est->v_rc = est->v_rc + K1 * y;

    est->soc = clamp(est->soc, 0.0f, 1.0f);

    /* P = (I - K H) P */
    float KH00 = K0 * H0;
    float KH01 = K0 * H1;
    float KH10 = K1 * H0;
    float KH11 = K1 * H1;

    float M00 = 1.0f - KH00;
    float M01 = -KH01;
    float M10 = -KH10;
    float M11 = 1.0f - KH11;

    float newP00 = M00 * P00 + M01 * P10;
    float newP01 = M00 * P01 + M01 * P11;
    float newP10 = M10 * P00 + M11 * P10;
    float newP11 = M10 * P01 + M11 * P11;

    est->P[0][0] = newP00;
    est->P[0][1] = newP01;
    est->P[1][0] = newP10;
    est->P[1][1] = newP11;
}

void ekf_step(EmbeddedSOCEstimator *est, float current, float voltage_measured, float dt) {
    ekf_predict(est, current, dt);
    ekf_update(est, voltage_measured, current);
}