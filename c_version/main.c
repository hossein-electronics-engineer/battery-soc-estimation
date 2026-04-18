#include <stdio.h>
#include <stdlib.h>
#include "ekf_soc.h"

#define MAX_SAMPLES 5000

int main() {
    EmbeddedSOCEstimator est;

    float time_arr[MAX_SAMPLES];
    float current_arr[MAX_SAMPLES];
    float soc_true_arr[MAX_SAMPLES];
    float soc_python_arr[MAX_SAMPLES];
    float vrc_true_arr[MAX_SAMPLES];
    float vrc_python_arr[MAX_SAMPLES];
    float voltage_arr[MAX_SAMPLES];

    float soc_c_arr[MAX_SAMPLES];
    float vrc_c_arr[MAX_SAMPLES];

    int n = 0;

    FILE *fp_in = fopen("../results/simulation_results.csv", "r");
    if (fp_in == NULL) {
        printf("Error: could not open ../results/simulation_results.csv\n");
        return 1;
    }

    FILE *fp_out = fopen("c_output.csv", "w");
    if (fp_out == NULL) {
        printf("Error: could not create c_output.csv\n");
        fclose(fp_in);
        return 1;
    }

    char header[256];
    fgets(header, sizeof(header), fp_in);

    while (n < MAX_SAMPLES) {
        float t, current, soc_true, soc_python, vrc_true, vrc_python, ocv, v_terminal;

        int ret = fscanf(
            fp_in,
            "%f,%f,%f,%f,%f,%f,%f,%f",
            &t,
            &current,
            &soc_true,
            &soc_python,
            &vrc_true,
            &vrc_python,
            &ocv,
            &v_terminal
        );

        if (ret != 8) {
            break;
        }

        time_arr[n] = t;
        current_arr[n] = current;
        soc_true_arr[n] = soc_true;
        soc_python_arr[n] = soc_python;
        vrc_true_arr[n] = vrc_true;
        vrc_python_arr[n] = vrc_python;
        voltage_arr[n] = v_terminal;
        n++;
    }

    fclose(fp_in);

    if (n < 2) {
        printf("Error: not enough samples in simulation_results.csv\n");
        fclose(fp_out);
        return 1;
    }

    {
        float q_capacity_coulomb = 2.3f * 3600.0f;
        float r0 = 0.05f;
        float r1 = 0.02f;
        float c1 = 2000.0f;

        ekf_init(&est, q_capacity_coulomb, r0, r1, c1);
    }

    soc_c_arr[0] = est.soc;
    vrc_c_arr[0] = est.v_rc;

    for (int i = 1; i < n; i++) {
        float dt = time_arr[i] - time_arr[i - 1];

        ekf_step(&est, current_arr[i], voltage_arr[i], dt);

        soc_c_arr[i] = est.soc;
        vrc_c_arr[i] = est.v_rc;
    }

    fprintf(fp_out, "Step,Time,Current,Voltage,True_SOC,Python_SOC,C_SOC,True_VRC,Python_VRC,C_VRC\n");

    for (int i = 0; i < n; i++) {
        fprintf(
            fp_out,
            "%d,%.2f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            i,
            time_arr[i],
            current_arr[i],
            voltage_arr[i],
            soc_true_arr[i],
            soc_python_arr[i],
            soc_c_arr[i],
            vrc_true_arr[i],
            vrc_python_arr[i],
            vrc_c_arr[i]
        );
    }

    fclose(fp_out);

    printf("2-state C replay completed successfully.\n");
    printf("Loaded %d samples from ../results/simulation_results.csv\n", n);
    printf("Results saved to c_output.csv\n");

    return 0;
}