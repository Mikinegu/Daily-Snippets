class ParkingLot:
    VEHICLE_SIZES = {
        'bike': 1,
        'car': 2,
        'truck': 4
    }

    def __init__(self, total_slots):
        self.total_slots = total_slots
        self.occupied_slots = 0
        self.vehicles = {}  # license_plate: (vehicle_type, slot_count)

    def park(self, vehicle_type, license_plate):
        if license_plate in self.vehicles:
            print(f"❌ Vehicle {license_plate} is already parked.")
            return

        if vehicle_type not in self.VEHICLE_SIZES:
            print(f"❌ Invalid vehicle type: {vehicle_type}")
            return

        required_slots = self.VEHICLE_SIZES[vehicle_type]
        if self.occupied_slots + required_slots > self.total_slots:
            print(f"🚫 Not enough space to park {license_plate} ({vehicle_type}).")
            return

        self.vehicles[license_plate] = (vehicle_type, required_slots)
        self.occupied_slots += required_slots
        print(f"✅ Parked {license_plate} ({vehicle_type})")

    def remove(self, license_plate):
        if license_plate not in self.vehicles:
            print(f"❌ Vehicle {license_plate} not found in the lot.")
            return

        _, slots = self.vehicles.pop(license_plate)
        self.occupied_slots -= slots
        print(f"🅿️ Removed {license_plate}")

    def status(self):
        print("\n📊 Current Parking Status:")
        print(f"- Total Slots: {self.total_slots}")
        print(f"- Occupied: {self.occupied_slots} / {self.total_slots}")
        print(f"- Vehicles: {list(self.vehicles.keys())}")
        print("- Detailed:")
        for plate, (v_type, slots) in self.vehicles.items():
            print(f"  • {plate}: {v_type}, {slots} slots")


# Example Usage
if __name__ == "__main__":
    lot = ParkingLot(20)
    lot.park('bike', 'AB123')
    lot.park('car', 'CD456')
    lot.park('truck', 'EF789')
    lot.remove('CD456')
    lot.status()
