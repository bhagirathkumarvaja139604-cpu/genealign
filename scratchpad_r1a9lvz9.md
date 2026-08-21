# Test Plan for GeneAlign

- [x] Open index.html and verify load. (FAILED)
    - Attempted to open `file:///c:/Users/ASUS/Desktop/CD%20Project/index.html` - BLOCKED by tool policy (access to file URL is blocked).
    - Tried `http://localhost:[80, 3000, 5173, 5500, 8000, 8080, 8081, 9000]/` - all REFUSED connection (no local server running).
    - Tried IPv6 `http://[::1]:8000/` - REFUSED connection.
    - Result: Cannot test the website as local files cannot be opened in the browser and no server is serving the file.
- [ ] Test 1: Global Alignment (Needleman-Wunsch)
    - Sequence 1: GATTACA
    - Sequence 2: GCATGCU
    - Match: 1, Mismatch: -1, Gap: -2
    - Expected Score: -1
    - Verify traceback matrix.
- [ ] Test 2: Local Alignment (Smith-Waterman)
    - Same inputs.
    - Expected Score: 2
    - Verify traceback starts/stops at correct cells.
- [ ] Test 3: Step-by-Step Visualization
    - Enable step mode.
    - Verify step controls and explanations.
    - Click "Finish" and compare with non-step mode.
- [ ] Test 4: Export and Reset functionality.




