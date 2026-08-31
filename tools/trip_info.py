TRIP_INFO = {
    "destination": "Kudremukha",
    "start_date": "August 20, 2026",
    "end_date": "August 22, 2026",
    "departure": "Bengaluru",
    "departure_time": "9:30 PM",
    "trip_duration": "3 days",
    "day_1": "Bengaluru to Kudremukha",
    "day_2": "Kudremukha trek",
    "day_3": "Return journey and beach visit",
}


def get_trip_info(topic: str) -> str:
    """
    Retrieve information about the Kudremukha trip.
    """

    topic = topic.lower().strip()

    if topic in TRIP_INFO:
        return TRIP_INFO[topic]

    if topic in ["destination", "location"]:
        return TRIP_INFO["destination"]

    if topic in ["date", "dates"]:
        return (
            f"{TRIP_INFO['start_date']} "
            f"to {TRIP_INFO['end_date']}"
        )

    if topic in ["departure", "departure_time"]:
        return (
            f"Departure from {TRIP_INFO['departure']} "
            f"at {TRIP_INFO['departure_time']}"
        )

    return (
        "Available trip information: "
        + ", ".join(TRIP_INFO.keys())
    )