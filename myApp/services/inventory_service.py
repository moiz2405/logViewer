import asyncio
import random
try:
    # When imported as a module
    from functions.logger import get_logger
except ImportError:
    # When imported directly
    from ..functions.logger import get_logger

logger = get_logger("InventoryService")

class InventoryService:
    def __init__(self, bad_log_ratio: int = 2):
        self.bad_log_ratio = bad_log_ratio
        logger.info(f"Inventory Service initialized with bad_log_ratio: {bad_log_ratio}")
    
    def set_bad_ratio(self, ratio: int):
        """Update the bad log ratio for this service"""
        if not isinstance(ratio, int) or not (0 <= ratio <= 10):
            logger.error(f"Invalid bad_log_ratio: {ratio}, must be between 0-10")
            return
        logger.info(f"Updating Inventory Service bad_log_ratio: {self.bad_log_ratio} -> {ratio}")
        self.bad_log_ratio = ratio
    
    async def run(self):
        """
        Simulate inventory service.
        bad_log_ratio: number of bad logs per 10 logs (0-10)
        """
        log_count = 0
        items = [
            {"name": "Laptop", "sku": "LT-5432", "category": "Electronics"},
            {"name": "Phone", "sku": "PH-9875", "category": "Electronics"},
            {"name": "Keyboard", "sku": "KB-3345", "category": "Peripherals"},
            {"name": "Mouse", "sku": "MS-1122", "category": "Peripherals"},
            {"name": "Monitor", "sku": "MN-7788", "category": "Displays"},
            {"name": "Headphones", "sku": "HP-4567", "category": "Audio"},
            {"name": "USB Cable", "sku": "USB-1234", "category": "Accessories"},
            {"name": "Docking Station", "sku": "DS-8910", "category": "Peripherals"}
        ]
        
        warehouses = ["NYC-1", "LAX-2", "CHI-3", "ATL-4", "SEA-5"]
        
        while True:
            log_count += 1
            item = random.choice(items)
            qty = random.randint(1, 50)
            warehouse = random.choice(warehouses)
            
            # Good logs
            if log_count % 10 > self.bad_log_ratio:
                actions = ["add", "remove", "update", "check", "transfer", "restock"]
                action = random.choice(actions)
                
                if action == "add":
                    logger.info(f"Stock added: {qty} units of {item['name']} (SKU: {item['sku']}) to {warehouse}")
                    logger.debug(f"Inventory transaction ID: INV-{random.randint(10000, 99999)}")
                
                elif action == "remove":
                    remove_reason = random.choice(["sale", "damage", "return", "transfer"])
                    logger.info(f"Stock removed: {qty} units of {item['name']} due to {remove_reason}")
                    logger.debug(f"Current stock level: {random.randint(50, 200)} units")
                
                elif action == "update":
                    logger.info(f"Stock level updated for {item['name']} in {warehouse}")
                    logger.info(f"Inventory reconciliation completed for {item['category']} category")
                
                elif action == "check":
                    available = random.randint(20, 100)
                    logger.info(f"Inventory check OK for {item['name']}, available: {available} units")
                    if available < 30:
                        logger.warning(f"Low stock alert for {item['name']} (SKU: {item['sku']}): {available} units")
                
                elif action == "transfer":
                    dest_warehouse = random.choice([w for w in warehouses if w != warehouse])
                    logger.info(f"Inventory transfer: {qty} units of {item['name']} from {warehouse} to {dest_warehouse}")
                    logger.debug(f"Transfer shipment ID: TR-{random.randint(1000, 9999)}")
                
                elif action == "restock":
                    logger.info(f"Restock order placed for {item['name']}: {qty} units")
                    logger.debug(f"Expected delivery in {random.randint(1, 7)} days")
            
            # Bad logs
            else:
                error_types = ["sync_failed", "low_stock", "data_error", "barcode_scan_failed", "system_error"]
                error_type = random.choice(error_types)
                
                if error_type == "sync_failed":
                    logger.error(f"Inventory sync failed for {item['name']} in {warehouse}")
                    logger.debug(f"Database connection timeout after 30s")
                    logger.warning(f"Retry {random.randint(1, 3)} of 3 for inventory sync")
                
                elif error_type == "low_stock":
                    current = random.randint(0, 5)
                    logger.warning(f"Critical low stock for {item['name']}: {current} units remaining")
                    if current == 0:
                        logger.error(f"Stockout detected for {item['name']} (SKU: {item['sku']})")
                        logger.info(f"Auto-reorder triggered for {item['name']}")
                
                elif error_type == "data_error":
                    logger.error(f"Data inconsistency found for {item['name']} in {warehouse}")
                    logger.warning(f"Expected: {random.randint(50, 100)}, Actual: {random.randint(20, 49)}")
                    logger.info(f"Manual reconciliation required for SKU: {item['sku']}")
                
                elif error_type == "barcode_scan_failed":
                    logger.error(f"Barcode scan failed for {item['name']} (SKU: {item['sku']})")
                    logger.warning(f"Item metadata update required for {item['name']}")
                
                elif error_type == "system_error":
                    logger.error(f"Inventory system error in {warehouse} warehouse module")
                    logger.error(f"Failed to update stock levels for {item['category']} category")
                    logger.debug(f"Stack trace: NullReferenceException in UpdateStock() method")
            
            await asyncio.sleep(random.uniform(1.5, 4.0))
