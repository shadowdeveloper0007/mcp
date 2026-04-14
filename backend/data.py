TENANTS = [
    {
        "id": "T001",
        "name": "Rahul Sharma",
        "unit": "4B",
        "phone": "9876543210",
        "email": "rahul@email.com",
        "rent_amount": 25000,
        "paid_this_month": True,
    },
    {
        "id": "T002",
        "name": "Priya Mehta",
        "unit": "7A",
        "phone": "9123456780",
        "email": "priya@email.com",
        "rent_amount": 18000,
        "paid_this_month": False,
    },
    {
        "id": "T003",
        "name": "Amit Verma",
        "unit": "12C",
        "phone": "9988776655",
        "email": "amit@email.com",
        "rent_amount": 30000,
        "paid_this_month": False,
    },
    {
        "id": "T004",
        "name": "Sneha Kapoor",
        "unit": "2A",
        "phone": "9871234560",
        "email": "sneha@email.com",
        "rent_amount": 22000,
        "paid_this_month": True,
    },
]

UNITS = [
    {"unit": "4B", "status": "occupied", "rent": 25000, "floor": 4},
    {"unit": "7A", "status": "occupied", "rent": 18000, "floor": 7},
    {"unit": "12C", "status": "occupied", "rent": 30000, "floor": 12},
    {"unit": "2A", "status": "occupied", "rent": 22000, "floor": 2},
    {"unit": "5D", "status": "vacant", "rent": 20000, "floor": 5},
    {"unit": "9B", "status": "vacant", "rent": 27000, "floor": 9},
]

MAINTENANCE = [
    {
        "id": "M001",
        "unit": "4B",
        "issue": "Leaking tap in bathroom",
        "status": "open",
        "priority": "high",
    },
    {
        "id": "M002",
        "unit": "7A",
        "issue": "AC not cooling",
        "status": "open",
        "priority": "normal",
    },
    {
        "id": "M003",
        "unit": "12C",
        "issue": "Broken window latch",
        "status": "resolved",
        "priority": "low",
    },
]
