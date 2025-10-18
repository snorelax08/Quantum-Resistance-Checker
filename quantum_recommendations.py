# Recommendations engine for quantum security improvements

RECOMMENDATIONS_DATABASE = {
    'RSA': {
        'risk': 'CRITICAL',
        'issue': 'RSA encryption is vulnerable to quantum computer attacks',
        'why': 'Quantum computers can use Shor\'s algorithm to break RSA in seconds',
        'recommendation': 'Migrate to post-quantum cryptography immediately',
        'alternatives': ['Kyber (NIST standardized)', 'Lattice-based encryption', 'Hash-based signatures'],
        'timeline': 'URGENT - Within 1-2 years',
        'priority': 1
    },
    'ECC': {
        'risk': 'HIGH',
        'issue': 'Elliptic Curve Cryptography is vulnerable to quantum attacks',
        'why': 'Quantum computers can break ECC faster than RSA',
        'recommendation': 'Plan migration to post-quantum algorithms',
        'alternatives': ['Kyber', 'Dilithium', 'FALCON'],
        'timeline': 'HIGH - Within 2-3 years',
        'priority': 2
    },
    'AES': {
        'risk': 'LOW',
        'issue': 'None - AES is quantum-safe',
        'why': 'AES-256 requires 2^128 operations even with quantum computers (Grover\'s algorithm)',
        'recommendation': 'No action needed - continue using AES',
        'alternatives': ['Keep current setup', 'Use AES-256 for extra security'],
        'timeline': 'SAFE - No immediate action',
        'priority': 0
    },
    'Kyber': {
        'risk': 'LOW',
        'issue': 'None - Kyber is quantum-safe',
        'why': 'NIST-standardized post-quantum algorithm based on lattice problems',
        'recommendation': 'Excellent choice - no changes needed',
        'alternatives': ['Already using best practice'],
        'timeline': 'SAFE - Future-proof',
        'priority': 0
    },
    'Dilithium': {
        'risk': 'LOW',
        'issue': 'None - Dilithium is quantum-safe',
        'why': 'NIST-standardized post-quantum digital signature algorithm',
        'recommendation': 'Excellent choice for signatures',
        'alternatives': ['Already optimal'],
        'timeline': 'SAFE - Future-proof',
        'priority': 0
    },
    'Unknown': {
        'risk': 'UNKNOWN',
        'issue': 'Encryption algorithm cannot be determined',
        'why': 'File type not recognized in database',
        'recommendation': 'Verify encryption method and check quantum compatibility',
        'alternatives': ['Check file documentation', 'Consult security team'],
        'timeline': 'REVIEW - Investigate further',
        'priority': 3
    }
}

def get_recommendations(algorithm, score):
    """
    Get recommendations based on algorithm and score
    Returns a formatted recommendation string
    """
    
    # Get base recommendation
    if 'RSA' in algorithm.upper():
        base_algo = 'RSA'
    elif 'ECC' in algorithm.upper():
        base_algo = 'ECC'
    elif 'AES' in algorithm.upper():
        base_algo = 'AES'
    elif 'KYBER' in algorithm.upper():
        base_algo = 'Kyber'
    elif 'DILITHIUM' in algorithm.upper():
        base_algo = 'Dilithium'
    else:
        base_algo = 'Unknown'
    
    if base_algo not in RECOMMENDATIONS_DATABASE:
        base_algo = 'Unknown'
    
    rec = RECOMMENDATIONS_DATABASE[base_algo]
    
    # Build recommendation text
    rec_text = f"""
{'='*80}
💡 SECURITY RECOMMENDATIONS
{'='*80}

CURRENT STATUS:
  Algorithm: {algorithm}
  Risk Level: {rec['risk']}
  Security Score: {score}/100

ISSUE:
  {rec['issue']}

WHY THIS MATTERS:
  {rec['why']}

WHAT YOU SHOULD DO:
  {rec['recommendation']}

ALTERNATIVE ALGORITHMS:
"""
    
    for i, alt in enumerate(rec['alternatives'], 1):
        rec_text += f"  {i}. {alt}\n"
    
    rec_text += f"""
TIMELINE:
  {rec['timeline']}

MIGRATION STEPS (if needed):
"""
    
    if base_algo == 'RSA':
        rec_text += """  1. Audit all systems currently using RSA
  2. Evaluate post-quantum options (Kyber recommended)
  3. Plan gradual migration to new algorithms
  4. Update cryptographic libraries
  5. Test new implementation thoroughly
  6. Deploy to production gradually
  7. Monitor for compatibility issues
  8. Complete migration before 2030
"""
    elif base_algo == 'ECC':
        rec_text += """  1. Assess current ECC implementation
  2. Test post-quantum alternatives (Kyber/Dilithium)
  3. Plan upgrade timeline
  4. Update systems gradually
  5. Monitor transition period
"""
    elif base_algo == 'AES':
        rec_text += """  1. No immediate action required
  2. Maintain current AES-256 implementation
  3. Monitor for new threats
  4. Keep cryptographic libraries updated
  5. Review security regularly
"""
    else:
        rec_text += """  1. Identify the exact encryption algorithm used
  2. Consult with security team
  3. Compare against quantum-safe standards
  4. Make informed upgrade decision
"""
    
    rec_text += f"""
{'='*80}
POST-QUANTUM CRYPTOGRAPHY OPTIONS:
{'='*80}

KYBER (Key Encapsulation):
  • NIST Standardized (2022)
  • Based on lattice problems
  • Fast and secure
  • Recommended for key exchange
  • Score Impact: +30 points

DILITHIUM (Digital Signatures):
  • NIST Standardized (2022)
  • Based on lattice problems
  • Secure signature algorithm
  • Recommended for authentication
  • Score Impact: +20 points

FALCON (Digital Signatures):
  • Compact signature size
  • Efficient computation
  • Alternative to Dilithium
  • Good for bandwidth-limited systems

{'='*80}
RESOURCES FOR FURTHER READING:
{'='*80}

  • NIST Post-Quantum Cryptography: https://csrc.nist.gov/projects/post-quantum-cryptography/
  • Quantum Computing Threat Timeline: https://www.nist.gov/news-and-events
  • Migration Guidelines: https://csrc.nist.gov/pubs/sp/800/176/rev-1/final

{'='*80}
"""
    
    return rec_text

def get_batch_recommendations(results_list):
    """
    Get overall recommendations for multiple files
    """
    
    high_risk_files = [r for r in results_list if r['total_score'] < 40]
    medium_risk_files = [r for r in results_list if 40 <= r['total_score'] < 60]
    low_risk_files = [r for r in results_list if r['total_score'] >= 60]
    
    rec_text = f"""
{'='*80}
📊 BATCH SECURITY RECOMMENDATIONS
{'='*80}

PORTFOLIO ANALYSIS:
  • Total Files: {len(results_list)}
  • Critical Risk Files: {len(high_risk_files)}
  • Medium Risk Files: {len(medium_risk_files)}
  • Low Risk Files: {len(low_risk_files)}

PRIORITY ACTIONS:

1. CRITICAL (Score < 40):
"""
    
    for f in high_risk_files:
        rec_text += f"   - {f['file_name']} ({f['algorithm']}): Upgrade IMMEDIATELY\n"
    
    if not high_risk_files:
        rec_text += "   - None found. Good!\n"
    
    rec_text += f"""
2. MEDIUM (Score 40-60):
"""
    
    for f in medium_risk_files:
        rec_text += f"   - {f['file_name']} ({f['algorithm']}): Plan upgrade\n"
    
    if not medium_risk_files:
        rec_text += "   - None found. Great!\n"
    
    rec_text += f"""
3. SECURE (Score > 60):
"""
    
    for f in low_risk_files:
        rec_text += f"   - {f['file_name']} ({f['algorithm']}): Well protected\n"
    
    rec_text += f"""
OVERALL MIGRATION STRATEGY:

Phase 1 (Next 6 months):
  ✓ Audit all encryption systems
  ✓ Identify vulnerable algorithms (RSA, ECC)
  ✓ Evaluate post-quantum options
  ✓ Create migration plan

Phase 2 (6-12 months):
  ✓ Pilot post-quantum implementation
  ✓ Test Kyber for key exchange
  ✓ Test Dilithium for signatures
  ✓ Train technical team

Phase 3 (12-24 months):
  ✓ Gradual rollout to production
  ✓ Monitor for issues
  ✓ Maintain backward compatibility
  ✓ Complete critical systems

Phase 4 (24+ months):
  ✓ Full migration complete
  ✓ Legacy systems phased out
  ✓ Regular security audits
  ✓ Stay updated with standards

{'='*80}
ESTIMATED IMPACT OF MIGRATION:

Before Migration:
  Average Score: {sum([r['total_score'] for r in results_list]) / len(results_list):.1f}/100

After Migration to Kyber/Dilithium:
  Estimated Score: 90+/100

Security Improvement: ~{90 - (sum([r['total_score'] for r in results_list]) / len(results_list)):.0f} points

{'='*80}
"""
    
    return rec_text