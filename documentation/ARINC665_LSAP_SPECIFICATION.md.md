# ARINC Report 665-5 Loadable Software Airplane Parts (LSAP) Specification

## 1\. Scope & System Definition

ARINC Report 665 specifies the standards for formatting, packaging, verifying, and distributing Loadable Software Airplane Parts (LSAPs). LSAPs represent all operational software, flight control laws, navigation databases, and configuration tables loaded into commercial transport aircraft avionics Line Replaceable Units (LRUs) using ARINC 615 and ARINC 615A data loaders.

## 2\. File Structures & Formats

- **Header File (`.LUH` / `.LND` / `.LUS`)**:  
  - Format Version: `0x8005` for ARINC 665-5.  
  - Word Alignment: 32-bit word alignment throughout all binary tables.  
  - Part Number Syntax: Alphanumeric format `MMM-SSSS-CCCC` (up to 32 uppercase characters).  
  - Target Hardware List: List of compatible LRU part numbers / Functional Item Numbers (FINs).  
  - Payload File List: Exact file byte lengths, CRC-32 checksums, and relative directory paths.  
- **Media Set Directory Files**:  
  - `LOADS.LST`: Media catalog indexing all loadable parts and header paths.  
  - `FILES.LST`: Media catalog indexing all physical files, volume numbers, and checksums.  
  - Multi-Volume Support: Sequencing for multi-disk distributions (Disk 1 of N).

## 3\. Cryptographic & Data Integrity Architecture

- **CRC-16-CCITT**:  
  - Polynomial \$x^{16} \+ x^{12} \+ x^5 \+ 1\$ (`0x1021`) computed over header parameter blocks.  
- **CRC-32 (IEEE 802.3 / ISO 3309\)**:  
  - Polynomial `0xEDB88320` computed individually over every payload data file.  
- **SHA-256 Digest & Digital Signatures**:  
  - Cryptographic hash binding the entire load package per ARINC 665-5 Section 3.7.  
  - Digital Signature Block implementing X.509 PKI certificates per FAA AC 20-145 to prevent unauthorized software alteration.

## 4\. Aeronautical Data Loading Compatibility

- Compatible with ARINC 615A Ethernet data loading over TFTP.  
- Compatible with ARINC 615-3/4 legacy ARINC 429 high-speed bus data loading.