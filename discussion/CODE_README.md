# 🔬 LIGO Echo Search Code

This folder contains everything you need to test the BULK Framework prediction that black hole mergers should show gravitational wave echoes at 0.1-1.2 milliseconds after ringdown.

---

## 📁 What's Here

| File | Purpose |
|------|---------|
| `ligo_echo_search.py` | Main Python script - complete analysis tool |
| `ligo_echo_tutorial.ipynb` | Jupyter notebook - interactive step-by-step tutorial |
| `SETUP_GUIDE.md` | Installation instructions and troubleshooting |

---

## ⚡ Quick Start

### Option 1: Run the Script (Fastest)

```bash
# Install dependencies
pip install gwpy numpy scipy matplotlib

# Run search on GW150914
python ligo_echo_search.py --event GW150914

# Done! Results will display.
```

### Option 2: Use the Notebook (Best for Learning)

```bash
# Install Jupyter
pip install jupyter

# Launch notebook
jupyter notebook ligo_echo_tutorial.ipynb

# Follow along step-by-step
```

---

## 🎯 What This Does

**The code:**
1. Downloads gravitational wave data from LIGO/Virgo (public, free)
2. Filters to ringdown frequency range (30-400 Hz)
3. Extracts the ringdown "template"
4. Searches for delayed replicas (echoes) at 0.1-1.2 ms
5. Calculates statistical significance
6. Generates plots and reports

**Output:**
- Peak correlation value
- Delay timing of peak
- Statistical significance (σ)
- Detailed plots
- Text report

---

## 📊 Understanding Results

### Statistical Significance:

- **< 3σ**: Not significant (likely noise)
- **3-5σ**: Marginal (interesting, needs verification)
- **> 5σ**: Strong detection (potential discovery!)

### What to Look For:

**Echo detected if:**
- Peak correlation > 3σ threshold
- Peak within 0.1-1.2 ms range
- Consistent across multiple detectors
- Repeats in similar events

---

## 🔧 Customization

### Search Different Event:

```bash
python ligo_echo_search.py --event GW170814
```

Available events: https://gwosc.org/eventapi/

### Use Different Detector:

```bash
python ligo_echo_search.py --detector L1  # Livingston
python ligo_echo_search.py --detector V1  # Virgo
```

### Custom Delay Range:

```bash
# Search 0.05 to 2.0 ms
python ligo_echo_search.py --delay-min 0.00005 --delay-max 0.002
```

### Save Results:

```bash
python ligo_echo_search.py \
  --event GW150914 \
  --save-plot results.png \
  --save-report results.txt
```

### All Options:

```bash
python ligo_echo_search.py --help
```

---

## 📖 Detailed Documentation

- **Complete setup instructions:** See `SETUP_GUIDE.md`
- **Physics background:** See `../concept_paper/TESTABLE_PREDICTIONS.md`
- **Author story:** See `../concept_paper/AUTHOR_PERSPECTIVE.md`
- **FAQ:** See `../concept_paper/FAQ.md`

---

## 🐛 Troubleshooting

### "No module named 'gwpy'"

```bash
pip install gwpy
```

### "Event not found"

- Check spelling (case-sensitive!)
- Verify at https://gwosc.org/eventapi/

### No plot appears (Mac)

```bash
pip install pyqt5
```

### No plot appears (Linux)

```bash
sudo apt install python3-tk
```

### More help:

See `SETUP_GUIDE.md` for complete troubleshooting.

---

## 🎓 Educational Use

**Perfect for:**
- Undergraduate physics projects
- Data analysis courses
- Python programming examples
- Scientific method demonstrations
- Gravitational wave education

**Students:** Feel free to use this code for coursework. Just cite the source!

---

## 🤝 Contributing

**Ways to help:**

1. **Run the search** - Test on multiple events
2. **Improve the code** - Add features, fix bugs
3. **Add tests** - Unit tests, validation
4. **Documentation** - Clarify, expand, translate
5. **Share results** - Found something? Let us know!

**Open an issue or pull request on GitHub:**  
https://github.com/tsallie52/TheBulkFramework

---

## 📊 Expected Performance

**Typical run (GW150914):**
- Download: 30-60 seconds (first time, then cached)
- Analysis: 1-2 minutes
- Total: ~3 minutes

**Memory usage:** ~500 MB

**Disk space:** ~1 GB for several events (cached data)

---

## 🔬 Scientific Rigor

**This code implements standard signal processing:**
- Cross-correlation (well-established method)
- Bandpass filtering (standard practice)
- Statistical significance testing (proper thresholds)
- Null hypothesis framework (falsifiable)

**Not included (but should be for publication):**
- Bootstrap resampling
- False alarm probability calculation
- Systematic error analysis
- Multiple testing correction

**If you find something significant:**
Contact professional gravitational wave researchers for peer review and validation.

---

## ⚖️ License

**MIT License** - Free to use, modify, and share.

**Attribution appreciated but not required.**

**If this helps your research, consider citing:**

Tom Sallie (2025). BULK Framework: LIGO Echo Search Tools.  
https://github.com/tsallie52/TheBulkFramework

---

## 📧 Contact

**Questions? Results? Ideas?**

- Email: tsallie@gmail.com
- GitHub Issues: https://github.com/tsallie52/TheBulkFramework/issues

**We want to hear from you:**
- Found echoes? (Exciting!)
- Found nothing? (Also valuable!)
- Improved the code? (Appreciated!)
- Found bugs? (Thanks!)

---

## 🎯 The Goal

**This isn't about proving the BULK hypothesis right.**

**It's about testing a prediction honestly and rigorously.**

**The data will tell us the answer.**

**All we have to do is look.**

---

**Good luck, and happy searching! 🔭**

*Remember: The best outcome is the true outcome, whatever it may be.*
