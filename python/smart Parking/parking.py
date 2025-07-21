import time
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict

# Logic
class ParkingLot:
    VEHICLE_SIZES = {'bike': 1, 'car': 2, 'truck': 4}
    VEHICLE_RATES = {'bike': 1, 'car': 2, 'truck': 4}

    def __init__(self, total_slots):
        self.total_slots = total_slots
        self.occupied_slots = 0
        self.vehicles = {}
        self.total_revenue = 0

    def park(self, vehicle_type, license_plate):
        if license_plate in self.vehicles:
            return f"{license_plate} is already parked."

        if vehicle_type not in self.VEHICLE_SIZES:
            return "Invalid vehicle type."

        required_slots = self.VEHICLE_SIZES[vehicle_type]
        if self.occupied_slots + required_slots > self.total_slots:
            return f"Not enough space for {vehicle_type}."

        self.vehicles[license_plate] = {
            "type": vehicle_type,
            "slots": required_slots,
            "start_time": time.time()
        }
        self.occupied_slots += required_slots
        return f"Parked {license_plate} ({vehicle_type})."

    def remove(self, license_plate):
        if license_plate not in self.vehicles:
            return f"{license_plate} not found."

        info = self.vehicles.pop(license_plate)
        self.occupied_slots -= info['slots']
        duration = max((time.time() - info['start_time']) / 3600, 1)
        fee = self.VEHICLE_RATES[info['type']] * int(duration)
        self.total_revenue += fee
        return f"Removed {license_plate} ({info['type']})\nFee: ${fee}"

    def status(self):
        return {
            "total": self.total_slots,
            "occupied": self.occupied_slots,
            "available": self.total_slots - self.occupied_slots,
            "vehicles": list(self.vehicles.keys())
        }

    def show_by_type(self):
        grouped = defaultdict(list)
        for plate, info in self.vehicles.items():
            grouped[info['type']].append(plate)
        return grouped

    def get_revenue(self):
        return self.total_revenue


# GUI
class ParkingApp:
    def __init__(self, root):
        self.lot = ParkingLot(20)
        self.root = root
        self.root.title("🚗 Smart Parking System")
        self.root.geometry("500x500")

        self.create_widgets()

    def create_widgets(self):
        # Entry fields
        self.plate_entry = ttk.Entry(self.root)
        self.plate_entry.insert(0, "License Plate")
        self.plate_entry.pack(pady=5)

        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.root, textvariable=self.type_var)
        self.type_dropdown['values'] = ['bike', 'car', 'truck']
        self.type_dropdown.set('bike')
        self.type_dropdown.pack(pady=5)

        # Buttons
        ttk.Button(self.root, text="Park", command=self.park_vehicle).pack(pady=5)
        ttk.Button(self.root, text="Remove", command=self.remove_vehicle).pack(pady=5)
        ttk.Button(self.root, text="View Status", command=self.view_status).pack(pady=5)
        ttk.Button(self.root, text="Grouped View", command=self.grouped_view).pack(pady=5)
        ttk.Button(self.root, text="Total Revenue", command=self.show_revenue).pack(pady=5)

        # Output
        self.output_box = tk.Text(self.root, height=15, width=60)
        self.output_box.pack(pady=10)

    def write_output(self, text):
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)

    def park_vehicle(self):
        plate = self.plate_entry.get().strip()
        vtype = self.type_var.get().strip()
        result = self.lot.park(vtype, plate)
        self.write_output(result)

    def remove_vehicle(self):
        plate = self.plate_entry.get().strip()
        result = self.lot.remove(plate)
        self.write_output(result)

    def view_status(self):
        status = self.lot.status()
        text = (
            f"📊 Parking Lot Status:\n"
            f"- Total Slots: {status['total']}\n"
            f"- Occupied: {status['occupied']}\n"
            f"- Available: {status['available']}\n"
            f"- Vehicles: {status['vehicles']}"
        )
        self.write_output(text)

    def grouped_view(self):
        grouped = self.lot.show_by_type()
        text = "🚗 Vehicles Grouped by Type:\n"
        for vtype, plates in grouped.items():
            text += f"- {vtype.upper()}: {plates}\n"
        self.write_output(text)

    def show_revenue(self):
        rev = self.lot.get_revenue()
        self.write_output(f"📈 Total Revenue: ${rev:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
