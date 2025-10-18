# This file contains the logic for scoring quantum resistance

# Comprehensive encryption database with many file types
ENCRYPTION_DATABASE = {
    # RSA/PGP Encryption (Vulnerable to Quantum)
    '.gpg': {'algorithm': 'RSA/PGP', 'quantum_safe': False, 'risk': 'CRITICAL', 'description': 'PGP/GPG encrypted file'},
    '.pgp': {'algorithm': 'RSA/PGP', 'quantum_safe': False, 'risk': 'CRITICAL', 'description': 'PGP encrypted file'},
    '.asc': {'algorithm': 'RSA/PGP', 'quantum_safe': False, 'risk': 'CRITICAL', 'description': 'ASCII-armored PGP file'},
    
    # AES Encryption (Quantum Safe)
    '.7z': {'algorithm': 'AES-256', 'quantum_safe': True, 'risk': 'LOW', 'description': '7-Zip compressed with AES'},
    '.zip': {'algorithm': 'AES', 'quantum_safe': True, 'risk': 'LOW', 'description': 'ZIP archive (possibly AES encrypted)'},
    '.rar': {'algorithm': 'AES', 'quantum_safe': True, 'risk': 'LOW', 'description': 'RAR archive (AES encrypted)'},
    '.aes': {'algorithm': 'AES', 'quantum_safe': True, 'risk': 'LOW', 'description': 'AES encrypted data'},
    '.enc': {'algorithm': 'AES', 'quantum_safe': True, 'risk': 'LOW', 'description': 'Generic encrypted data (assumed AES)'},
    
    # ECC Encryption (Vulnerable to Quantum)
    '.ecc': {'algorithm': 'ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'Elliptic Curve encrypted file'},
    
    # Certificate and Key Files (RSA/ECC - Vulnerable)
    '.pem': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'Privacy Enhanced Mail certificate'},
    '.cer': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'X.509 certificate'},
    '.crt': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'Certificate file'},
    '.der': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'DER encoded certificate'},
    '.pfx': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'PKCS#12 certificate'},
    '.p12': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'PKCS#12 certificate'},
    '.key': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'CRITICAL', 'description': 'Private key file'},
    '.pub': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'Public key file'},
    
    # Microsoft Office Encrypted
    '.docx': {'algorithm': 'AES-256', 'quantum_safe': True, 'risk': 'LOW', 'description': 'Word document (AES encrypted)'},
    '.xlsx': {'algorithm': 'AES-256', 'quantum_safe': True, 'risk': 'LOW', 'description': 'Excel spreadsheet (AES encrypted)'},
    '.pptx': {'algorithm': 'AES-256', 'quantum_safe': True, 'risk': 'LOW', 'description': 'PowerPoint (AES encrypted)'},
    
    # Other Encrypted Formats
    '.bin': {'algorithm': 'Unknown', 'quantum_safe': None, 'risk': 'UNKNOWN', 'description': 'Binary encrypted data'},
    '.dat': {'algorithm': 'Unknown', 'quantum_safe': None, 'risk': 'UNKNOWN', 'description': 'Data file (encryption unknown)'},
    '.rsa': {'algorithm': 'RSA', 'quantum_safe': False, 'risk': 'CRITICAL', 'description': 'RSA encrypted file'},
    '.encrypted': {'algorithm': 'Unknown', 'quantum_safe': None, 'risk': 'UNKNOWN', 'description': 'Encrypted file'},
    
    # Post-Quantum Algorithms (Future Safe)
    '.pqc': {'algorithm': 'Post-Quantum Lattice', 'quantum_safe': True, 'risk': 'LOW', 'description': 'Post-quantum cryptography file'},
    '.kyber': {'algorithm': 'Kyber (Lattice)', 'quantum_safe': True, 'risk': 'LOW', 'description': 'NIST Kyber encrypted'},
    '.dilithium': {'algorithm': 'Dilithium (Lattice)', 'quantum_safe': True, 'risk': 'LOW', 'description': 'NIST Dilithium signed'},
    
    # SSH and TLS Keys
    '.ppk': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'PuTTY private key'},
    '.ppt': {'algorithm': 'RSA/ECC', 'quantum_safe': False, 'risk': 'HIGH', 'description': 'Private key file'},
}

def score_by_algorithm(algorithm):
    """
    Score based on the encryption algorithm used
    Returns a score out of 30 (this is 30% of total score)
    """
    algorithm_upper = algorithm.upper()
    
    if 'AES' in algorithm_upper:
        return 28
    elif 'POST-QUANTUM' in algorithm_upper or 'LATTICE' in algorithm_upper or 'KYBER' in algorithm_upper or 'DILITHIUM' in algorithm_upper:
        return 30
    elif 'RSA' in algorithm_upper:
        return 8
    elif 'ECC' in algorithm_upper:
        return 12
    elif 'DES' in algorithm_upper:
        return 2
    elif 'UNKNOWN' in algorithm_upper:
        return 15
    else:
        return 15
    
def score_by_key_length(file_size, file_extension):
    """
    Estimate key length based on file size and extension
    Returns a score out of 40 (this is 40% of total score)
    """
    
    # If it's a key file, check its size
    if file_extension in ['.key', '.pem', '.cer', '.pub', '.pfx', '.p12', '.ppk', '.ppt']:
        if file_size < 100:
            return 5
        elif file_size < 1000:
            return 15
        elif file_size < 2000:
            return 25
        elif file_size < 4000:
            return 30
        else:
            return 35
    
    # For encrypted data files
    if file_size < 1000:
        return 10
    elif file_size < 1000000:
        return 20
    elif file_size < 10000000:
        return 28
    else:
        return 30

def score_by_file_type(file_extension):
    """
    Score based on file type/extension
    Returns a score out of 20 (this is 20% of total score)
    """
    
    modern_formats = ['.7z', '.gpg', '.zip', '.aes', '.pqc', '.kyber', '.dilithium', '.docx', '.xlsx', '.pptx']
    legacy_formats = ['.rar', '.pem', '.cer', '.key', '.bin']
    unknown_formats = ['.dat', '.enc', '.encrypted']
    
    if file_extension in modern_formats:
        return 18
    elif file_extension in legacy_formats:
        return 10
    elif file_extension in unknown_formats:
        return 12
    else:
        return 12

def calculate_quantum_vulnerability_score(file_path):
    """
    Main function that calculates the quantum vulnerability score
    Score is 0-100, where 100 is most secure against quantum attacks
    """
    
    import os
    
    # Get file info
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_name)[1].lower()
    
    # Look up the file type in our database
    if file_extension in ENCRYPTION_DATABASE:
        file_info = ENCRYPTION_DATABASE[file_extension]
        algorithm = file_info['algorithm']
        is_quantum_safe = file_info['quantum_safe']
        risk_level = file_info['risk']
        description = file_info['description']
    else:
        algorithm = "Unknown"
        is_quantum_safe = None
        risk_level = "UNKNOWN"
        description = "Unknown file type"
    
    # Calculate scores for each factor
    algorithm_score = score_by_algorithm(algorithm)
    key_length_score = score_by_key_length(file_size, file_extension)
    file_type_score = score_by_file_type(file_extension)
    entropy_score = 5  # Simplified entropy
    
    # Total score (out of 100)
    total_score = algorithm_score + key_length_score + file_type_score + entropy_score
    
    # Create results dictionary
    results = {
        'file_name': file_name,
        'file_size': file_size,
        'file_extension': file_extension,
        'algorithm': algorithm,
        'is_quantum_safe': is_quantum_safe,
        'risk_level': risk_level,
        'description': description,
        'algorithm_score': algorithm_score,
        'key_length_score': key_length_score,
        'file_type_score': file_type_score,
        'entropy_score': entropy_score,
        'total_score': total_score,
    }
    
    return results