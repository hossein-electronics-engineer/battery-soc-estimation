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

    FILE *fp = fopen("c_output.csv", "w");
    if (fp == NULL) {
        printf("Error: could not create c_output.csv\n");
        return 1;
    }

    fprintf(fp, "Step,Current,Voltage,Estimated_SOC\n");
    printf("Step\tCurrent[A]\tVoltage[V]\tEstimated SOC\n");

    for (int i = 0; i < 10; i++) {
        float current = current_profile[i];
        float voltage = voltage_profile[i];
        float soc = ekf_step(&est, current, voltage, dt);

        printf("%d\t%.2f\t\t%.2f\t\t%.4f\n", i, current, voltage, soc);
        fprintf(fp, "%d,%.2f,%.2f,%.4f\n", i, current, voltage, soc);
    }

    fclose(fp);

    printf("\nResults saved to c_output.csv\n");

    return 0;
}
