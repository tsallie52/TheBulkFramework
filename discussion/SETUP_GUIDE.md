# 🛠️ Setup Guide: Running the LIGO Echo Search

This guide will help you set up your computer to run the LIGO echo search code, even if you've never used Python before.

---

## ⚡ Quick Start (For Experienced Users)

```bash
# Install dependencies
pip install gwpy numpy scipy matplotlib

# Run search
python ligo_echo_search.py --event GW150914

# Done!
```

---

## 📚 Complete Setup (For Beginners)

### Step 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

**Mac:**
```bash
# Using Homebrew (install from https://brew.sh if needed)
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Verify installation:**
```bash
python3 --version
# Should show: Python 3.x.x
```

---

### Step 2: Install Required Libraries

Open your terminal/command prompt and run:

```bash
pip install gwpy numpy scipy matplotlib
```

**This installs:**
- `gwpy` - LIGO data access and analysis tools
- `numpy` - Numerical computing
- `scipy` - Scientific computing (signal processing)
- `matplotlib` - Plotting and visualization

**Expected time:** 2-5 minutes

**If you see errors:**

**Error: "pip not found"**
- Try: `python3 -m pip install gwpy numpy scipy matplotlib`

**Error: "Permission denied"**
- Try: `pip install --user gwpy numpy scipy matplotlib`

**Error on Mac: "Command line tools not installed"**
- Run: `xcode-select --install`
- Then retry pip install

---

### Step 3: Download the Code

**Option A: Direct Download**
1. Go to: https://github.com/tsallie52/TheBulkFramework
2. Click green "Code" button → "Download ZIP"
3. Unzip the file
4. Navigate to the `code/` folder

**Option B: Git Clone** (if you have git)
```bash
git clone https://github.com/tsallie52/TheBulkFramework.git
cd TheBulkFramework/code
```

---

### Step 4: Test Your Setup

Run this simple test:

```bash
python ligo_echo_search.py --help
```

**Expected output:**
```
usage: ligo_echo_search.py [-h] [--event EVENT] [--detector {H1,L1,V1}]
                           [--delay-min DELAY_MIN] [--delay-max DELAY_MAX]
                           ...

Search for echoes in LIGO black hole merger events
```

**If you see this, you're ready!** ✅

---

### Step 5: Run Your First Search

**Basic search (uses defaults):**
```bash
python ligo_echo_search.py --event GW150914
```

**What happens:**
1. Downloads GW150914 data from LIGO (~30 seconds)
2. Applies bandpass filter
3. Extracts ringdown signal
4. Searches for echoes at 0.1-1.2 ms delays
5. Displays results and plots

**Expected runtime:** 1-3 minutes

**Expected output:**
```
======================================================================
LIGO BLACK HOLE ECHO SEARCH
BULK Framework Prediction Test
======================================================================

Downloading GW150914 data from H1...
✓ Data loaded: 131072 samples at 4096.0 Hz
Applying bandpass filter: 30-400 Hz...
✓ Filtering complete
Extracting ringdown signal...
  Auto-detected peak at GPS 1126259462.423
✓ Ringdown extracted: 410 samples, 100.0 ms duration

Searching for echoes from 0.10 ms to 1.20 ms...
  Step size: 0.010 ms

✓ Search complete!
  Peak correlation: 0.1234
  At delay: 0.543 ms
  Significance: 2.45 σ
  No significant echo found at this delay range

[Plot window opens]
```

---

## 🎯 Understanding the Output

### Correlation Values

**What it means:**
- **> 0.5:** Strong similarity (potential echo)
- **0.1 - 0.5:** Moderate similarity (investigate)
- **< 0.1:** Weak similarity (likely noise)

### Statistical Significance (σ)

**Interpretation:**
- **< 3σ:** Not significant (could be noise)
- **3-5σ:** Marginal detection (interesting, needs verification)
- **> 5σ:** Strong detection (potential discovery!)

**For reference:**
- Higgs boson discovered at 5σ
- LIGO's first GW detection: >5σ

---

## 🔧 Advanced Usage

### Search Different Event

```bash
python ligo_echo_search.py --event GW170814
```

**Available events:** See https://gwosc.org/eventapi/

### Use Different Detector

```bash
python ligo_echo_search.py --event GW150914 --detector L1
# Options: H1 (Hanford), L1 (Livingston), V1 (Virgo)
```

### Custom Delay Range

```bash
# Search 0.05 to 2.0 ms
python ligo_echo_search.py --event GW150914 --delay-min 0.00005 --delay-max 0.002
```

### Save Results

```bash
python ligo_echo_search.py --event GW150914 \
  --save-plot results_GW150914.png \
  --save-report results_GW150914.txt
```

### High-Resolution Search

```bash
# Finer step size (slower but more precise)
python ligo_echo_search.py --event GW150914 --delay-step 0.000001
# 0.001 ms steps instead of 0.01 ms
```

---

## 📊 Interpreting Results

### The Plot Shows:

**Top Panel: Correlation vs. Delay**
- X-axis: Echo delay time (milliseconds)
- Y-axis: Cross-correlation strength
- Red dashed line: 1σ noise level (expected random fluctuation)
- Orange dashed line: 3σ threshold (significance cutoff)
- Red dot: Peak correlation

**Bottom Panel: Ringdown Template**
- Shows the actual gravitational wave ringdown signal
- This is what we're searching for a delayed copy of

### What to Look For:

**Potential Echo Detected:**
- Sharp peak above 3σ line
- Peak within 0.1-1.2 ms range (BULK prediction)
- Consistent across multiple detectors
- Repeats in similar events

**No Echo:**
- All correlations below 3σ
- Random scatter around zero
- No coherent peak structure

---

## 🐛 Troubleshooting

### "No module named 'gwpy'"
**Fix:**
```bash
pip install gwpy
# Or: python3 -m pip install gwpy
```

### "Event not found" Error
**Fix:**
- Check event name spelling (case-sensitive!)
- Verify event exists: https://gwosc.org/eventapi/
- Try a different event from the list

### Code runs but no plot appears
**Fix (Mac):**
```bash
# Install GUI backend
pip install pyqt5
```

**Fix (Linux):**
```bash
sudo apt install python3-tk
```

### Download is slow
**Normal:** LIGO data files are large (100+ MB)
**First download:** May take 1-2 minutes
**Subsequent runs:** Much faster (data cached)

### Memory Error
**Fix:** Close other programs
**Or:** Use shorter ringdown window:
```bash
python ligo_echo_search.py --ringdown-duration 0.05
```

---

## 💾 Data Storage

**Where data is stored:**
- **Windows:** `C:\Users\[YourName]\.gwpy\cache`
- **Mac/Linux:** `~/.gwpy/cache`

**To clear cache:**
Delete the `.gwpy` folder in your home directory

**Disk space needed:** ~500 MB for several events

---

## 🚀 Next Steps

### After Running First Search:

1. **Test multiple events:**
   - GW150914 (first detection, high SNR)
   - GW170814 (triple detector)
   - GW190521 (massive black holes)

2. **Compare detectors:**
   - Run same event on H1, L1, V1
   - Do they show consistent results?

3. **Document findings:**
   - Save plots and reports
   - Note any patterns
   - Compare to BULK predictions

### If You Find Something Interesting:

1. **Verify it's real:**
   - Run on multiple events
   - Test different parameter ranges
   - Check for systematic errors

2. **Report it:**
   - Email: tsallie@gmail.com
   - Open GitHub issue
   - Share methodology and results

3. **Consider publication:**
   - Even null results are valuable
   - Contact gravitational wave researchers
   - Suggest collaboration

---

## 📖 Learning Resources

### Understanding Gravitational Waves:
- LIGO website: https://www.ligo.caltech.edu
- GW Open Science: https://gwosc.org
- "Black Holes and Time Warps" by Kip Thorne (book)

### Python Tutorials:
- Python.org official tutorial
- Real Python (https://realpython.com)
- Coursera: Python for Everybody

### Signal Processing:
- GWOSC tutorials: https://gwosc.org/tutorials/
- SciPy documentation: https://docs.scipy.org

---

## 🤝 Getting Help

**Code Issues:**
- Open issue on GitHub: https://github.com/tsallie52/TheBulkFramework/issues
- Include: Error message, Python version, operating system

**Physics Questions:**
- Read TESTABLE_PREDICTIONS.md in the repo
- Physics Stack Exchange: https://physics.stackexchange.com

**General Questions:**
- Email: tsallie@gmail.com
- Be specific about what you're trying to do

---

## ✅ Success Checklist

Before running serious searches, verify:

- [ ] Python 3.7+ installed
- [ ] All libraries installed (gwpy, numpy, scipy, matplotlib)
- [ ] Test search completes successfully
- [ ] Plots display correctly
- [ ] Results save to files
- [ ] You understand how to interpret σ values
- [ ] You've read TESTABLE_PREDICTIONS.md

**If all checked: You're ready to search for echoes!**

---

## 🎓 For Educators/Students

This code can be used for:
- Physics undergraduate projects
- Data analysis tutorials
- Scientific computing examples
- Gravitational wave education
- Hypothesis testing demonstrations

**License:** MIT (free to use, modify, share)

---

## 📧 Contact

**Author:** Tom Sallie  
**Email:** tsallie@gmail.com  
**Project:** https://github.com/tsallie52/TheBulkFramework

**Contributions welcome!**
- Bug fixes
- Documentation improvements
- Additional analysis features
- Educational materials

---

**Remember:** The goal is to find truth, not prove a hypothesis. Whether you find echoes or don't find echoes, both results teach us something about how black holes really work.

Good luck, and happy searching! 🔭
