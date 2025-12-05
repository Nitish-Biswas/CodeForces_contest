import os

def find_fraudulent_merchants(non_fraud_codes, fraud_codes, mcc_thresholds, merchant_mcc_map, min_charges, charges):
    """
    Identifies fraudulent merchants based on transaction history, MCC thresholds, and disputes.
    
    Args:
        non_fraud_codes (str): Comma-separated list of non-fraudulent response codes.
        fraud_codes (str): Comma-separated list of fraudulent response codes.
        mcc_thresholds (list): List of strings "mcc,threshold" (e.g., "airline,0.25").
        merchant_mcc_map (list): List of strings "acct_id,mcc".
        min_charges (str): Minimum number of charges required before evaluation.
        charges (list): List of strings representing chronological events (CHARGE or DISPUTE).
    
    Returns:
        str: Comma-separated, lexicographically sorted list of fraudulent account IDs.
    """
    
    # --- 1. PARSE STATIC CONFIGURATION ---
    
    # Convert fraud codes to a set for O(1) lookup
    # Note: We strip whitespace to be safe
    fraud_codes_set = set(code.strip() for code in fraud_codes.split(','))
    
    # Parse MCC Thresholds into a dictionary: {'airline': 0.25, 'retail': 0.8}
    mcc_thresholds_dict = {}
    for item in mcc_thresholds:
        if not item: continue
        parts = item.split(',')
        mcc_thresholds_dict[parts[0].strip()] = float(parts[1].strip())

    # Parse Merchant MCC Map into a dictionary: {'acct_1': 'airline'}
    merchant_mcc_dict = {}
    for item in merchant_mcc_map:
        if not item: continue
        parts = item.split(',')
        merchant_mcc_dict[parts[0].strip()] = parts[1].strip()

    # Parse minimum charges
    min_charges_int = int(min_charges)

    # --- 2. INITIALIZE STATE TRACKING ---
    
    # Tracks currently flagged merchants
    flagged_merchants = set()
    
    # Tracks statistics per merchant
    # Format: {'acct_id': {'total': 0, 'fraud': 0}}
    merchant_stats = {}
    
    # Tracks individual charge details for Disputes
    # Format: {'charge_id': {'acct_id': '...', 'is_fraud': True/False}}
    charge_history = {}

    # --- 3. PROCESS EVENTS CHRONOLOGICALLY ---
    
    for event in charges:
        if not event: continue
        parts = event.split(',')
        event_type = parts[0].strip()

        if event_type == "CHARGE":
            # Format: CHARGE, charge_id, acct_id, amount, code
            charge_id = parts[1].strip()
            acct_id = parts[2].strip()
            # amount = parts[3] (unused in logic)
            code = parts[4].strip()
            
            # Initialize merchant stats if new
            if acct_id not in merchant_stats:
                merchant_stats[acct_id] = {'total': 0, 'fraud': 0}
            
            # Determine if this specific charge is fraud
            is_fraud = code in fraud_codes_set
            
            # Store charge history for potential future disputes
            charge_history[charge_id] = {
                'acct_id': acct_id,
                'is_fraud': is_fraud
            }
            
            # Update counts
            merchant_stats[acct_id]['total'] += 1
            if is_fraud:
                merchant_stats[acct_id]['fraud'] += 1
                
            # EVALUATION LOGIC (Part 2 "Ratchet")
            # If already flagged, they stay flagged (unless disputed later).
            # We only need to check if they should be NEWLY flagged here.
            if acct_id not in flagged_merchants:
                stats = merchant_stats[acct_id]
                if stats['total'] >= min_charges_int:
                    mcc = merchant_mcc_dict.get(acct_id)
                    if mcc and mcc in mcc_thresholds_dict:
                        threshold = mcc_thresholds_dict[mcc]
                        fraud_ratio = stats['fraud'] / stats['total']
                        
                        if fraud_ratio >= threshold:
                            flagged_merchants.add(acct_id)

        elif event_type == "DISPUTE":
            # Format: DISPUTE, charge_id
            charge_id = parts[1].strip()
            
            # Retrieve charge details
            if charge_id in charge_history:
                charge_data = charge_history[charge_id]
                acct_id = charge_data['acct_id']
                was_fraud = charge_data['is_fraud']
                
                # Disputes only affect the score if the original charge was considered fraud
                if was_fraud:
                    # Decrement fraud count
                    merchant_stats[acct_id]['fraud'] -= 1
                    # Mark this charge as no longer fraud in history (prevent double dispute issues)
                    charge_history[charge_id]['is_fraud'] = False
                    
                    # RE-EVALUATION LOGIC (Part 3)
                    # "This is the only way that their status can be restored."
                    # If they are currently flagged, we check if they now fall BELOW the threshold.
                    if acct_id in flagged_merchants:
                        stats = merchant_stats[acct_id]
                        
                        # Calculate new ratio
                        # Note: Total transactions count usually remains the same, only the fraud numerator drops,
                        # effectively turning a fraud transaction into a normal one.
                        fraud_ratio = 0
                        if stats['total'] > 0:
                            fraud_ratio = stats['fraud'] / stats['total']
                            
                        mcc = merchant_mcc_dict.get(acct_id)
                        threshold = mcc_thresholds_dict.get(mcc, 0)
                        
                        # If ratio drops below threshold, remove flag
                        if fraud_ratio < threshold:
                            flagged_merchants.remove(acct_id)

    # --- 4. FORMAT OUTPUT ---
    
    # Return comma-separated, lexicographically sorted list
    sorted_merchants = sorted(list(flagged_merchants))
    return ",".join(sorted_merchants)

# --- EXECUTION BLOCK FOR TESTING ---
if __name__ == '__main__':
    # Test Data derived from Image 7 (Part 2 Example) and Image 2 (Part 3 Dispute logic)
    
    # 1. Setup Input Variables
    non_fraud_codes_input = "approved,invalid_pin,expired_card"
    fraud_codes_input = "do_not_honor,stolen_card,lost_card"
    
    mcc_thresholds_input = [
        "retail,0.5",
        "airline,0.25",
        "venue,0.25"
    ]
    
    merchant_mcc_map_input = [
        "acct_1,airline",
        "acct_2,venue",
        "acct_3,retail"
    ]
    
    min_charges_input = "0" # Using 0 to match immediate evaluation examples
    
    # Scenario: 
    # acct_1 (airline, 0.25): 100 (fraud), 200 (ok), 300 (fraud) -> 2/3 = 0.66 (>0.25) -> FLAGGED
    # DISPUTE ch_2 (Wait, ch_2 was approved/ok in my fake data, let's look at image data)
    
    # Using specific data from Image 6/7 logic
    charges_input = [
        "CHARGE,ch_1,acct_1,100,do_not_honor", # Fraud. Count: 1/1 (1.0). Flagged? Yes (1.0 > 0.25)
        "CHARGE,ch_2,acct_1,200,approved",     # OK. Count: 1/2 (0.5). Flagged? Yes (Sticky)
        "CHARGE,ch_3,acct_1,300,do_not_honor", # Fraud. Count: 2/3 (0.66). Flagged? Yes
        "CHARGE,ch_4,acct_2,400,approved",     # OK.
        "CHARGE,ch_5,acct_2,500,approved",     # OK.
        "CHARGE,ch_6,acct_1,600,lost_card",    # Fraud. Count: 3/4 (0.75).
        "DISPUTE,ch_1",                        # Dispute ch_1. acct_1 Fraud count becomes 2. Total 4. Ratio 0.5. 
                                               # Threshold 0.25. Still > 0.25. Still Flagged.
                                               
        # Let's try a case where dispute CLEARS the merchant
        "CHARGE,ch_10,acct_3,100,do_not_honor", # Retail(0.5). 1/1=1.0. Flagged.
        "DISPUTE,ch_10"                         # 0/1=0.0. Unflagged.
    ]

    result = find_fraudulent_merchants(
        non_fraud_codes_input,
        fraud_codes_input,
        mcc_thresholds_input,
        merchant_mcc_map_input,
        min_charges_input,
        charges_input
    )
    
    print(f"Fraudulent Merchants: {result}")