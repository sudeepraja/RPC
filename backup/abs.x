struct intpair {
        int a;
        int b;
};

program ABS_PROG {
        version ABS_VERS {
                int ABS(int) = 1;
                float ABSf(float) = 2;
                int ADD(intpair) = 3;
        } = 1;
} = 0x23451111;