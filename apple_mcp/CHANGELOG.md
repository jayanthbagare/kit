# Changelog

## Version 1.0.0 - 2025-10-27

### Major Refactoring and Testing

#### Fixed Issues
1. **Hardcoded Paths**
   - Fixed hardcoded path `/home/claude/tonnage_mcp_server.py` in test client
   - Updated to use dynamic path resolution based on project structure
   - Updated `mcp_config.json` to use `${PROJECT_ROOT}` placeholder

2. **Dependency Installation**
   - Removed inappropriate `--break-system-packages` flag from Flask installation
   - Added proper error handling for missing dependencies
   - Enhanced requirements.txt with testing and development dependencies

3. **Missing Dependencies**
   - Added pytest and testing frameworks
   - Added code quality tools (black, flake8, mypy)
   - Added development dependencies section

#### Project Restructuring
Reorganized the project into a proper Python package structure:

```
apple_mcp/
├── src/
│   └── tonnage_mcp/          # Main package
│       ├── __init__.py
│       ├── server.py          # MCP server (formerly tonnage_mcp_server.py)
│       └── http_wrapper.py    # HTTP wrapper (formerly http_mcp_wrapper.py)
├── tests/
│   ├── unit/                  # Unit tests
│   │   ├── test_server.py     # 13 tests for server
│   │   └── test_http_wrapper.py # 12 tests for HTTP wrapper
│   └── integration/           # Integration tests
│       └── test_integration.py # 3 end-to-end tests
├── examples/
│   ├── client_example.py      # Example client (formerly test_mcp_client.py)
│   └── sample_data.csv        # Sample training data
├── docs/
│   ├── QUICK_START.md
│   └── N8N_INTEGRATION_GUIDE.md
├── config/
│   └── mcp_config.json        # MCP configuration
├── requirements.txt           # Updated with all dependencies
├── setup.py                   # Package setup configuration
├── pytest.ini                 # Pytest configuration
├── .gitignore                 # Git ignore rules
└── README.md                  # Comprehensive documentation
```

#### New Test Suite
Created comprehensive test coverage (78% overall):

**Unit Tests - Server (13 tests)**
- Server initialization and configuration
- Model training with valid and invalid data
- Prediction functionality with and without training
- Valid values retrieval
- Batch prediction
- Error handling for unknown methods and tools

**Unit Tests - HTTP Wrapper (12 tests)**
- Health check endpoint
- Index/documentation endpoint
- Training endpoint with success and error cases
- Prediction endpoint with validation
- Batch prediction endpoint
- Valid values endpoint
- Raw MCP protocol endpoint

**Integration Tests (3 tests)**
- Complete workflow from initialization to prediction
- Error recovery and handling
- Different model types (Random Forest, Linear Regression)

#### Test Results
```
28 tests passed
0 tests failed
78% code coverage
6 warnings (sklearn feature name warnings - non-critical)
```

#### New Features
1. **Package Setup**
   - Added setup.py for proper package installation
   - Defined console scripts for easy server launching
   - Added package metadata and dependencies

2. **Configuration**
   - Added pytest.ini for test configuration
   - Added .gitignore for clean repository
   - Added comprehensive README.md

3. **Sample Data**
   - Added sample CSV file for testing and examples
   - Includes realistic data for quick starts

#### Code Quality Improvements
1. **Better Error Handling**
   - Improved error messages and status codes
   - Better validation of inputs
   - Graceful handling of missing dependencies

2. **Documentation**
   - Comprehensive README with installation and usage instructions
   - API documentation for all endpoints
   - Development guidelines

3. **Testing Infrastructure**
   - Pytest configuration with coverage reporting
   - Fixtures for test data and server instances
   - Async test support
   - Proper test isolation and cleanup

### Migration Notes

#### For Users of Old Structure
- Old files remain in root directory for backward compatibility
- New organized structure is in `src/` directory
- Update your imports to use `from tonnage_mcp import MCPServer`
- Update config paths to use new structure

#### Running Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test suites
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src/tonnage_mcp
```

#### Installation
```bash
# Development installation
pip install -e ".[dev]"

# Production installation
pip install -e .
```

### Breaking Changes
None - old files are preserved for backward compatibility.

### Dependencies Updated
- Added: pytest>=7.0.0
- Added: pytest-asyncio>=0.21.0
- Added: pytest-cov>=4.0.0
- Added: pytest-mock>=3.10.0
- Added: black>=23.0.0
- Added: flake8>=6.0.0
- Added: mypy>=1.0.0

### Contributors
- Refactoring and testing by Claude Code
