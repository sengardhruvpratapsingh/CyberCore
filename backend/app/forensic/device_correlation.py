def find_shared_devices(device_records):
    """
    Group phone numbers by IMEI and flag any IMEI that has
    been observed with more than one distinct phone number.

    This is a plain dict/set correlation, not a claim about
    identity. Multiple phone numbers sharing one IMEI is an
    observed association only - it does not by itself prove
    the same person used every number.
    """

    imei_to_numbers = {}

    for record in device_records:

        numbers = imei_to_numbers.setdefault(
            record.imei,
            set()
        )

        numbers.add(record.phone_number)

    findings = []

    for imei, numbers in imei_to_numbers.items():

        if len(numbers) > 1:

            findings.append({
                "imei": imei,
                "phone_numbers": sorted(numbers),
                "finding": (
                    "Same IMEI observed across "
                    f"{len(numbers)} distinct phone numbers."
                ),
                "association_type": "observed",
                "note": (
                    "This is an observed association, not proof "
                    "of shared identity or intent."
                )
            })

    return findings
