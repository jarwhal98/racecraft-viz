# racecraft-viz 🏎️📊

**racecraft-viz** is an experimental data visualization project that brings Formula 1 race data to life. It pulls real telemetry and timing data using [FastF1](https://theoehrly.github.io/Fast-F1/) and explores driver performance through visualizations, comparisons, and eventually—AI-generated storytelling.

This is a learning lab, a creative outlet, and a bit of a love letter to the complexity of F1.

---

## 🚀 Current Capabilities

- Pulls qualifying and race session data from real F1 events
- Prints fastest laps per driver and full race lap logs
- Sets up a clean, reproducible dev environment (GitHub + VS Code)
- Prepares the data foundation for future visual and narrative layers

---

## 🧭 Roadmap

This project is evolving slowly and intentionally. Here's where it's headed:

- [ ] Interactive lap time charts (per driver, per stint)
- [ ] Race pace and tire strategy visualizations
- [ ] AI-generated summaries (e.g., "How Verstappen pulled off the undercut")
- [ ] Experimental telemetry-based visual art ("F1 as Art" module)
- [ ] Narrative race breakdowns (starting with "The Anatomy of a Comeback")

---

## 🛠️ Getting Started

To run locally:

```bash
git clone https://github.com/your-username/racecraft-viz.git
cd racecraft-viz
mkdir cache  # required for FastF1 caching
pip install fastf1
python app.py