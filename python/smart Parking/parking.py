import time
from collections import defaultdict

class ParkingLot:
    VEHICLE_SIZES = {
        'bike': 1,
        'car': 2,
        'truck': 4
    }

    VEHICLE_RATES = {
        'bike': 1,
        'car': 2,
        'truck': 4
    }

    def __init__(self, total_slots):
        self.total_slots = total_slots
        self.occupied_slots = 0
        self.vehicles = {}  # license_plate: {type, slots, time}
        self.total_revenue = 0

    def park(self, vehicle_type, license_plate):
        if license_plate in self.vehicles:
            print(f"❌ {license_plate} is already parked.")
            return

        if vehicle_type not in self.VEHICLE_SIZES:
            print(f"❌ Invalid vehicle type: {vehicle_type}")
            return

        required_slots = self.VEHICLE_SIZES[vehicle_type]
        if self.occupied_slots + required_slots > self.total_slots:
            print(f"🚫 Not enough space for {license_plate} ({vehicle_type})")
            return

        self.vehicles[license_plate] = {
            "type": vehicle_type,
            "slots": required_slots,
            "start_time": time.time()
        }
        self.occupied_slots += required_slots
        print(f"✅ Parked {license_plate} ({vehicle_type})")

    def remove(self, license_plate):
        if license_plate not in self.vehicles:
            print(f"❌ Vehicle {license_plate} not found.")
            return

        info = self.vehicles.pop(license_plate)
        self.occupied_slots -= info['slots']

        duration_hours = max((time.time() - info['start_time']) / 3600, 1)
        fee = self.VEHICLE_RATES[info['type']] * int(duration_hours)
        self.total_revenue += fee

        print(f"🅿️ Removed {license_plate} ({info['type']})")
        print(f"🕒 Parked for ~{int(duration_hours)} hour(s)")
        print(f"💰 Fee: ${fee}")

    def status(self):
        print("\n📊 Parking Lot Status:")
        print(f"• Total Slots: {self.total_slots}")
        print(f"• Occupied: {self.occupied_slots} / {self.total_slots}")
        print(f"• Parked Vehicles: {list(self.vehicles.keys())}")
        print(f"• Revenue: ${self.total_revenue:.2f}")

    def search(self, keyword):
        print(f"\n🔍 Search for: {keyword}")
        found = False
        for plate, info in self.vehicles.items():
            if keyword.lower() in plate.lower() or keyword.lower() in info['type']:
                print(f"• {plate}: {info['type']}")
                found = True
        if not found:
            print("No matching vehicle found.")

    def show_by_type(self):
        grouped = defaultdict(list)
        for plate, info in self.vehicles.items():
            grouped[info['type']].append(plate)

        print("\n🚗 Vehicles Grouped by Type:")
        for v_type, plates in grouped.items():
            print(f"• {v_type.upper()}: {plates}")

    def show_revenue(self):
        print(f"\n📈 Total Revenue: ${self.total_revenue:.2f}")
if __name__ == "__main__":
    lot = ParkingLot(20)
    lot.park('car', 'AA111')
    lot.park('bike', 'BB222')
    lot.park('truck', 'CC333')
    time.sleep(2)  # Simulate parking time
    lot.status()
    lot.search('bike')
    lot.show_by_type()
    lot.remove('BB222')
    lot.status()
    lot.show_revenue()
