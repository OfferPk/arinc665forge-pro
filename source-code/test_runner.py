#!/usr/bin/env python3
"""
ARINC665Forge Pro - Automated Test Runner & Verification Suite
10 Comprehensive Verification Tests for ARINC Report 665-5 / FAA AC 20-145 Compliance
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib.machinery import SourceFileLoader
cli_module = SourceFileLoader("arinc665_cli", os.path.join(os.path.dirname(__file__), "arinc665-cli.py")).load_module()
ARINC665LSAP = cli_module.ARINC665LSAP

class TestARINC665ForgePro(unittest.TestCase):
    def setUp(self):
        self.lsap = ARINC665LSAP(part_number="JEP-NAV-2611-0001", media_pn="BOE-FMC-2611-0001")

    # Test 1: Part Number Syntax
    def test_01_part_number_syntax(self):
        self.assertTrue(self.lsap.validate_part_number("JEP-NAV-2611-0001"))
        self.assertTrue(self.lsap.validate_part_number("HON-FCC-0402"))
        self.assertTrue(self.lsap.validate_part_number("COL-TER-30AS-01"))

    # Test 2: Invalid Part Number Rejection
    def test_02_invalid_part_number_rejection(self):
        self.assertFalse(self.lsap.validate_part_number("lower_case_pn"))
        self.assertFalse(self.lsap.validate_part_number("INVALID@CHAR#"))
        self.assertFalse(self.lsap.validate_part_number("A" * 35)) # Exceeds 32 chars
        self.assertFalse(self.lsap.validate_part_number(""))

    # Test 3: Header Format Version
    def test_03_header_format_version(self):
        hdr = self.lsap.generate_header()
        self.assertEqual(hdr['format_version'], "0x8005 (ARINC 665-5)")
        self.assertEqual(hdr['part_number'], "JEP-NAV-2611-0001")

    # Test 4: CRC-16 Load Checksum
    def test_04_crc16_load_checksum(self):
        c16 = self.lsap.compute_crc16(b"ARINC_665_TEST_PAYLOAD")
        self.assertIsInstance(c16, int)
        self.assertGreater(c16, 0)
        self.assertLessEqual(c16, 0xFFFF)

    # Test 5: CRC-32 File Level Integrity
    def test_05_crc32_file_integrity(self):
        c32 = self.lsap.compute_crc32(b"AIRAC_CYCLE_2611_NAV_DATA_POINTS")
        self.assertIsInstance(c32, int)
        self.assertGreater(c32, 0)
        self.assertLessEqual(c32, 0xFFFFFFFF)

    # Test 6: SHA-256 Digest Validation
    def test_06_sha256_digest(self):
        s256 = self.lsap.compute_sha256(b"ARINC_665_LOAD_INTEGRITY")
        self.assertEqual(len(s256), 64, "SHA-256 must produce 64 hex characters")

    # Test 7: Target Hardware Compatibility Check
    def test_07_target_hardware_compatibility(self):
        self.assertTrue(self.lsap.check_compatibility("B787-FMC-L"))
        self.assertTrue(self.lsap.check_compatibility("B787-FMC-R"))

    # Test 8: Target Hardware Incompatibility Rejection
    def test_08_target_hardware_incompatibility(self):
        self.assertFalse(self.lsap.check_compatibility("A320-FMGC-1"), "Must reject incompatible aircraft type LRU")
        self.assertFalse(self.lsap.check_compatibility("B737-FCC-A"))

    # Test 9: Data File Directory Table
    def test_09_data_file_directory(self):
        hdr = self.lsap.generate_header()
        self.assertEqual(len(hdr['files']), 2)
        f1 = hdr['files'][0]
        self.assertEqual(f1['name'], "AIRAC2611.DAT")
        self.assertEqual(f1['size_bytes'], 14680064)
        self.assertTrue(f1['crc32'].startswith("0x"))

    # Test 10: 10-Point Normative Airworthiness Audit
    def test_10_normative_compliance_audit(self):
        audit = self.lsap.run_normative_audit()
        self.assertEqual(audit['total'], 10, "Total audit rules must equal 10")
        self.assertEqual(audit['passed'], 10, "All 10 audit rules must pass")
        self.assertEqual(audit['score'], "100.0%", "Compliance score must be 100.0%")
        self.assertEqual(audit['status'], "ARINC_665_5_LSAP_AIRWORTHY_CERTIFIED")

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestARINC665ForgePro)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    print("\nALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY.")
