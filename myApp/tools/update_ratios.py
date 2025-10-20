"""
Utility script to update service bad ratios at runtime.
This can be imported and used from your own scripts or interactive sessions.
"""

import importlib
import sys
import os

# Add parent directory to sys.path to allow importing the main module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import main module
import main

def update_ratios(api=None, auth=None, inventory=None, notification=None, payment=None):
    """
    Update the bad log ratios for any services at runtime.
    
    Args:
        api (int, optional): Bad log ratio for API service (0-10)
        auth (int, optional): Bad log ratio for Auth service (0-10)
        inventory (int, optional): Bad log ratio for Inventory service (0-10)
        notification (int, optional): Bad log ratio for Notification service (0-10)
        payment (int, optional): Bad log ratio for Payment service (0-10)
    
    Returns:
        dict: Current bad log ratios for all services
    """
    main.update_service_ratios(
        api_ratio=api,
        auth_ratio=auth,
        inventory_ratio=inventory,
        notification_ratio=notification,
        payment_ratio=payment
    )
    
    # Return current ratios
    return {
        "api": main.api_service.bad_log_ratio if main.api_service else None,
        "auth": main.auth_service.bad_log_ratio if main.auth_service else None,
        "inventory": main.inventory_service.bad_log_ratio if main.inventory_service else None,
        "notification": main.notification_service.bad_log_ratio if main.notification_service else None,
        "payment": main.payment_service.bad_log_ratio if main.payment_service else None
    }

def get_current_ratios():
    """Get the current bad log ratios for all services."""
    return {
        "api": main.api_service.bad_log_ratio if main.api_service else None,
        "auth": main.auth_service.bad_log_ratio if main.auth_service else None,
        "inventory": main.inventory_service.bad_log_ratio if main.inventory_service else None,
        "notification": main.notification_service.bad_log_ratio if main.notification_service else None,
        "payment": main.payment_service.bad_log_ratio if main.payment_service else None
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Update service bad log ratios at runtime")
    parser.add_argument("--api", type=int, choices=range(0, 11), help="API service bad ratio (0-10)")
    parser.add_argument("--auth", type=int, choices=range(0, 11), help="Auth service bad ratio (0-10)")
    parser.add_argument("--inventory", type=int, choices=range(0, 11), help="Inventory service bad ratio (0-10)")
    parser.add_argument("--notification", type=int, choices=range(0, 11), help="Notification service bad ratio (0-10)")
    parser.add_argument("--payment", type=int, choices=range(0, 11), help="Payment service bad ratio (0-10)")
    parser.add_argument("--get", action="store_true", help="Get current ratios without changing them")
    
    args = parser.parse_args()
    
    if args.get:
        current_ratios = get_current_ratios()
        print("Current bad log ratios:")
        for service, ratio in current_ratios.items():
            if ratio is not None:
                print(f"  {service.capitalize()} Service: {ratio}/10")
            else:
                print(f"  {service.capitalize()} Service: Not running")
    else:
        updated = update_ratios(
            api=args.api,
            auth=args.auth,
            inventory=args.inventory,
            notification=args.notification,
            payment=args.payment
        )
        
        print("Updated bad log ratios:")
        for service, ratio in updated.items():
            if ratio is not None:
                print(f"  {service.capitalize()} Service: {ratio}/10")
            else:
                print(f"  {service.capitalize()} Service: Not running")
