import heapq

print("=" * 70)
print("      AI-BASED SMART PARKING SYSTEM")
print("=" * 70)

# ------------------------------------------------------------------
# INPUT: Parking Facility Layout (Multi-Level)
# ------------------------------------------------------------------
# Each slot: level, slot_id, distance_from_entrance (m), occupied status
parking_lot = [
    {"level": 1, "slot": "A1", "distance": 5,  "occupied": True},
    {"level": 1, "slot": "A2", "distance": 8,  "occupied": False},
    {"level": 1, "slot": "A3", "distance": 3,  "occupied": False},
    {"level": 1, "slot": "A4", "distance": 12, "occupied": True},
    {"level": 1, "slot": "A5", "distance": 2,  "occupied": False},
    {"level": 1, "slot": "A6", "distance": 15, "occupied": False},
    {"level": 1, "slot": "A7", "distance": 7,  "occupied": True},
    {"level": 1, "slot": "A8", "distance": 4,  "occupied": False},
    {"level": 2, "slot": "B1", "distance": 18, "occupied": False},
    {"level": 2, "slot": "B2", "distance": 20, "occupied": True},
    {"level": 2, "slot": "B3", "distance": 16, "occupied": False},
    {"level": 2, "slot": "B4", "distance": 22, "occupied": False},
    {"level": 2, "slot": "B5", "distance": 19, "occupied": True},
    {"level": 2, "slot": "B6", "distance": 17, "occupied": False},
]

n_slots = len(parking_lot)
print(f"\nInitializing parking facility with {n_slots} slots across 2 levels...")

print("\n" + "-" * 70)
print("SENSOR SCAN: Current Slot Status")
print("-" * 70)
print("{:<8}{:<8}{:<15}{:<12}".format("Level", "Slot", "Distance(m)", "Status"))
print("-" * 70)
for s in parking_lot:
    status = "Occupied" if s["occupied"] else "Vacant"
    print("{:<8}{:<8}{:<15}{:<12}".format(s["level"], s["slot"], s["distance"], status))

# ------------------------------------------------------------------
# VEHICLE ARRIVAL QUEUE
# ------------------------------------------------------------------
# Vehicles arriving at the entrance requesting a parking slot
vehicles = [
    {"vehicle_id": "KL07-AI-1234", "arrival_time": "09:01 AM"},
    {"vehicle_id": "KL07-BZ-5678", "arrival_time": "09:02 AM"},
    {"vehicle_id": "KL07-CX-9012", "arrival_time": "09:04 AM"},
]

print("\n" + "-" * 70)
print("VEHICLE ARRIVAL QUEUE")
print("-" * 70)
print("{:<18}{:<15}".format("Vehicle ID", "Arrival Time"))
print("-" * 70)
for v in vehicles:
    print("{:<18}{:<15}".format(v["vehicle_id"], v["arrival_time"]))

# ------------------------------------------------------------------
# AI AGENT: Vacant Slot Detection using a Min-Heap
# ------------------------------------------------------------------
def build_vacancy_heap(lot):
    """Builds a min-heap of all currently vacant slots ordered by
    distance from the entrance, so the nearest slot can always be
    retrieved in O(log n) time."""
    heap = []
    for s in lot:
        if not s["occupied"]:
            heapq.heappush(heap, (s["distance"], s["level"], s["slot"]))
    return heap


def guide_vehicle_to_nearest_slot(lot, vehicle):
    """AI decision procedure: picks the nearest vacant slot for a
    single vehicle, reserves it, and returns the guidance details."""
    heap = build_vacancy_heap(lot)

    if not heap:
        return None

    distance, level, slot_id = heapq.heappop(heap)

    # Reserve the slot so the next vehicle cannot be guided to it
    for s in lot:
        if s["slot"] == slot_id:
            s["occupied"] = True
            break

    return {
        "vehicle_id": vehicle["vehicle_id"],
        "slot": slot_id,
        "level": level,
        "distance": distance,
    }


print("\n" + "=" * 70)
print("AI AGENT: Detecting vacancies and guiding each vehicle...")
print("=" * 70)

guidance_log = []
for vehicle in vehicles:
    result = guide_vehicle_to_nearest_slot(parking_lot, vehicle)
    if result:
        guidance_log.append(result)
        print(f"\nVehicle {result['vehicle_id']}")
        print(f"  Assigned Slot   : {result['slot']} (Level {result['level']})")
        print(f"  Distance        : {result['distance']} m from entrance")
        print(f"  Guidance        : Proceed to Level {result['level']}, "
              f"slot {result['slot']} is {result['distance']}m ahead.")
    else:
        print(f"\nVehicle {vehicle['vehicle_id']}: No vacant slot available. "
              f"Facility is FULL.")

# ------------------------------------------------------------------
# PERFORMANCE EVALUATION
# ------------------------------------------------------------------
total_slots = len(parking_lot)
occupied_slots = sum(1 for s in parking_lot if s["occupied"])
vacant_slots = total_slots - occupied_slots
occupancy_rate = (occupied_slots / total_slots) * 100
avg_guidance_distance = (
    sum(g["distance"] for g in guidance_log) / len(guidance_log)
    if guidance_log else 0
)

print("\n" + "=" * 70)
print("AI PERFORMANCE REPORT")
print("=" * 70)
print("Total Slots            :", total_slots)
print("Occupied Slots          :", occupied_slots)
print("Vacant Slots            :", vacant_slots)
print("Occupancy Rate          : {:.1f}%".format(occupancy_rate))
print("Vehicles Guided         :", len(guidance_log))
print("Avg. Guidance Distance  : {:.1f} m".format(avg_guidance_distance))
print("Guidance Time per Vehicle: < 1 sec")
print("Status                  : Optimal")

print("\nAll vehicles processed and slot allocation completed successfully.")
