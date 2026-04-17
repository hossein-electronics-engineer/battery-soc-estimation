#include <stdio.h>
#include "ekf_soc.h"

int main() {
    EmbeddedSOCEstimator est;

    float q_capacity_coulomb = 2.3f * 3600.0f;
    float r0 = 0.05f;
    float dt = 1.0f;

    ekf_init(&est, q_capacity_coulomb, r0);

    float current_profile[10] = {
        0.0f, 2.0f, 2.0f, 1.0f, 0.0f,
        -1.5f, -1.5f, 2.5f, 2.5f, 0.0f
    };

    float voltage_profile[10] = {
        4.02f, 3.92f, 3.88f, 3.90f, 3.91f,
        3.98f, 4.01f, 3.83f, 3.76f, 3.85f
    };

    printf("Step\tCurrent[A]\tVoltage[V]\tEstimated SOC\n");

    for (int i = 0; i < 10; i++) {
        float soc = ekf_step(&est, current_profile[i], voltage_profile[i], dt);
        printf("%d\t%.2f\t\t%.2f\t\t%.4f\n", i, current_profile[i], voltage_profile[i], soc);
    }

    return 0;
}
